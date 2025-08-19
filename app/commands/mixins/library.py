import os

import magic
import requests
from systems.commands.index import CommandMixin
from utility.data import Collection, check_base64, decode_base64
from utility.filesystem import save_file


class LibraryMixin(CommandMixin("library")):

    def get_library_path(self, library_name):
        return os.path.join(self.manager.file_storage_path, self.active_user.name, library_name)

    def get_file_info(self, library_name, file_path):
        library_base_path = self.get_library_path(library_name)
        info = Collection(
            library_base_path=library_base_path,
            file_path=file_path.removeprefix("/"),
            full_file_path=os.path.join(library_base_path, file_path),
            file_type=self._get_file_type(file_path),
        )
        os.makedirs(os.path.dirname(info.full_file_path), exist_ok=True)
        return info

    # File operations
    def download_file(self, library_name, file_path, file_url):
        file_info = self.get_file_info(library_name, file_path)

        response = requests.get(file_url)
        response.raise_for_status()

        binary = "binary" in magic.from_buffer(response.text.encode("utf-8"), mime=True)
        save_file(file_info.full_file_path, response.content if binary else response.text, binary=binary)
        if file_info.file_type and response.text:
            self.index_file(library_name, file_path)

        return file_info.full_file_path

    def upload_file(self, library_name, file_path, file_content=None):
        file_info = self.get_file_info(library_name, file_path)
        binary = False
        if file_content and check_base64(file_content):
            file_content = decode_base64(file_content)
            binary = True

        save_file(file_info.full_file_path, file_content if file_content else "", binary=binary)
        if file_info.file_type and file_content:
            self.index_file(library_name, file_path)

        return file_info.full_file_path

    def index_file(self, library, path):
        self.send("library:index", {"user": self.active_user.name, "library": library, "path": path})

    def search_files(self, library_name, search_text, max_results=100):
        sections = {}
        scores = {}
        results = []

        section_db = self.qdrant("section")
        search_results = self.search_embeddings(
            self.active_user,
            "library",
            search_text,
            fields=["library", "path", "section_id", "order"],
            limit=max_results,
            min_score=0.3,
            filter_field="library",
            filter_ids=library_name,
        )
        for sentence_results in search_results:
            for scored_point in sentence_results:
                path = scored_point.payload["path"]
                section_id = scored_point.payload["section_id"]
                score = scored_point.score

                if section_id not in scores:
                    scores[section_id] = Collection(score=score, scores=[score])
                else:
                    scores[section_id].scores.append(score)
                    scores[section_id].score = max(scores[section_id].scores)

        for section_embedding in section_db.filter("id", list(scores.keys(), fields=["path", "text", "order"])):
            sections[section_embedding.id] = {
                "path": section_embedding.payload["path"],
                "passage": section_embedding.payload["text"],
                "order": section_embedding.payload["order"],
            }

        for section_id, section_info in sorted(scores.items(), key=lambda item: item[1].score):
            results.append(sections[section_id])

        return results

    def _get_file_type(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()[1:] if ext else None

    # Web operations
    def search_web(self, query, provider="google", max_results=10):
        search_engine = self.get_provider("search_engine", provider)
        return search_engine.search(query, max_results)

    def fetch_web_content(self, url):
        return self.parse_webpage(url)
