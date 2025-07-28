import os

import requests
from systems.commands.index import CommandMixin
from utility.filesystem import load_file, save_file


class LibraryMixin(CommandMixin("library")):

    def get_library_path(self, library_name):
        """Get the base path for a library"""
        return os.path.join(self.manager.file_storage_path, self.active_user.name, library_name)

    def download_file(self, library_name, file_path, file_url, file_type=None):
        """Download a file from URL and save to library"""
        library_base_path = self.get_library_path(library_name)
        full_file_path = os.path.join(library_base_path, file_path)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Download file
        response = requests.get(file_url)
        response.raise_for_status()

        # Save file
        binary = file_type in ["binary", "image", "video", "audio"]
        save_file(full_file_path, response.content if binary else response.text, binary=binary)

        return full_file_path

    def upload_file(self, library_name, file_path, file_content=None, file_type=None):
        """Upload/save file content to library"""
        library_base_path = self.get_library_path(library_name)
        full_file_path = os.path.join(library_base_path, file_path)

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        # Save file content
        binary = file_type in ["binary", "image", "video", "audio"]
        content = file_content if file_content is not None else ""
        save_file(full_file_path, content, binary=binary)

        return full_file_path

    def search_files(self, library_name, search_text, max_results=10):
        """Search for files in library matching search text"""
        library_base_path = self.get_library_path(library_name)
        results = []

        if not os.path.exists(library_base_path):
            return results

        # Walk through library directory
        for root, dirs, files in os.walk(library_base_path):
            for file in files:
                if len(results) >= max_results:
                    break

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, library_base_path)

                # Check if search text matches filename or content
                if search_text.lower() in file.lower():
                    results.append({"path": relative_path, "name": file, "type": self._get_file_type(file_path)})
                else:
                    # Check file content (for text files)
                    try:
                        content = load_file(file_path, binary=False)
                        if search_text.lower() in content.lower():
                            results.append({"path": relative_path, "name": file, "type": self._get_file_type(file_path)})
                    except Exception:
                        # Skip binary files or files that can't be read as text
                        pass

        return results

    def _get_file_type(self, file_path):
        """Determine file type based on extension"""
        _, ext = os.path.splitext(file_path)
        return ext.lower()[1:] if ext else "unknown"
