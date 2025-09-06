import os
import io
import hashlib
import logging

from dateutil import parser as dateparser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
from django.conf import settings

from systems.plugins.index import BaseProvider
from utility.filesystem import save_file
from utility.data import dump_json


logger = logging.getLogger(__name__)


SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

GOOGLE_EXPORT_MAP = {
    "application/vnd.google-apps.document": (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".docx",
    ),
    "application/vnd.google-apps.spreadsheet": (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xlsx",
    ),
    "application/vnd.google-apps.presentation": (
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".pptx",
    ),
}


class Provider(BaseProvider("document_source", "google_drive")):

    def _save_credential_file(self):
        service_account_json_path = os.path.join(settings.DATA_DIR, "google.drive.json")
        credential_json = dump_json(
            {
                "type": "service_account",
                "project_id": settings.GOOGLE_DRIVE_PROJECT_ID,
                "private_key_id": settings.GOOGLE_DRIVE_PRIVATE_KEY_ID,
                "private_key": settings.GOOGLE_DRIVE_PRIVATE_KEY,
                "client_email": settings.GOOGLE_DRIVE_CLIENT_EMAIL,
                "client_id": settings.GOOGLE_DRIVE_CLIENT_ID,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{settings.GOOGLE_DRIVE_CLIENT_EMAIL}",
                "universe_domain": "googleapis.com",
            },
            indent=2,
        )
        save_file(service_account_json_path, credential_json.replace("\\\\n", "\\n"))
        return service_account_json_path

    def download(self, folders, root_directory):
        service_account_json_path = self._save_credential_file()
        credentials = service_account.Credentials.from_service_account_file(service_account_json_path, scopes=SCOPES)
        credentials = credentials.with_subject(settings.GOOGLE_DRIVE_EMAIL)

        for directory, folder_id in folders.items():
            folder = self._get_file(credentials, folder_id, fields="id,name,mimeType,trashed")
            if not folder or folder.get("trashed") or folder.get("mimeType") != "application/vnd.google-apps.folder":
                raise ValueError(
                    "Provided folder_id is invalid, trashed, or not a folder, or the service account has no access."
                )
            if directory == "<name>":
                directory = folder["name"]

            if directory == ".":
                base_local = root_directory
            else:
                base_local = os.path.join(root_directory, directory)

            os.makedirs(base_local, exist_ok=True)
            self._download_folder_recursive(credentials, folder_id, base_local)

    def _download_folder_recursive(self, credentials, folder_id, local_dir):
        os.makedirs(local_dir, exist_ok=True)
        for item in self._list_children(credentials, folder_id):
            if item.get("trashed"):
                continue
            name = item["name"]
            if item["mimeType"] == "application/vnd.google-apps.folder":
                sub_local = os.path.join(local_dir, name)
                self._download_folder_recursive(credentials, item["id"], sub_local)
            else:
                self._download_file_item(credentials, item, local_dir)

    def _download_file_item(self, credentials, item, local_dir):
        mime = item.get("mimeType", "")
        is_google_native = mime.startswith("application/vnd.google-apps")
        export = GOOGLE_EXPORT_MAP.get(mime)

        if is_google_native and not export:
            logger.debug("Skipping unsupported Google file: %s (%s)", item["name"], mime)
            return

        if is_google_native:
            export_mime, ext = export
            local_path = self._ensure_extension(os.path.join(local_dir, item["name"]), ext)
        else:
            local_path = os.path.join(local_dir, item["name"])

        need = False
        if not os.path.exists(local_path):
            need = True
        else:
            if not is_google_native and item.get("md5Checksum"):
                local_md5 = self._md5(local_path)
                if local_md5 != item["md5Checksum"]:
                    need = True
            else:
                remote_ts = dateparser.isoparse(item["modifiedTime"]).timestamp()
                local_ts = os.path.getmtime(local_path)
                if remote_ts > local_ts + 1:
                    need = True

        if not need:
            return

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        if is_google_native:
            self._export_file(credentials, item["id"], export_mime, local_path)
        else:
            self._download_binary(credentials, item["id"], local_path)

        self._apply_remote_mtime(local_path, item["modifiedTime"])
        logger.info(f"Saved: {local_path}")

        file_text = self._parse_file(local_path)
        if file_text:
            save_file(f"{local_path}.md", file_text)

    def _list_children(self, credentials, folder_id):
        service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        q = f"'{folder_id}' in parents and trashed = false"
        fields = "nextPageToken, files(id,name,mimeType,md5Checksum,modifiedTime,trashed)"
        page_token = None

        while True:
            resp = (
                service.files()
                .list(
                    q=q,
                    fields=fields,
                    pageSize=1000,
                    pageToken=page_token,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                )
                .execute()
            )
            for f in resp.get("files", []):
                yield f
            page_token = resp.get("nextPageToken")
            if not page_token:
                break

    def _get_file(self, credentials, file_id, fields):
        service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        return service.files().get(fileId=file_id, fields=fields, supportsAllDrives=True).execute()

    def _download_binary(self, credentials, file_id, local_path):
        self.command.info(f"Downloading file: {local_path}")
        service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
        with io.FileIO(local_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)
            done = False
            while not done:
                status, done = downloader.next_chunk()

    def _export_file(self, credentials, file_id, export_mime, local_path):
        self.command.info(f"Downloading file: {local_path}")
        service = build("drive", "v3", credentials=credentials, cache_discovery=False)
        request = service.files().export_media(fileId=file_id, mimeType=export_mime)
        with io.FileIO(local_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)
            done = False
            while not done:
                status, done = downloader.next_chunk()

    def _ensure_extension(self, path, desired_ext):
        base, ext = os.path.splitext(path)
        if ext.lower() != desired_ext.lower():
            return base + desired_ext
        return path

    def _md5(self, path):
        h = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _apply_remote_mtime(self, local_path, iso_modified):
        ts = dateparser.isoparse(iso_modified).timestamp()
        os.utime(local_path, (ts, ts))
