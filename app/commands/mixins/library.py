import os

import requests
from systems.commands.index import CommandMixin
from utility.filesystem import load_file, save_file


class LibraryMixin(CommandMixin("library")):

    def get_library_path(self, library_name):
        """Get the base path for a library"""
        return os.path.join(self.manager.file_storage_path, self.active_user.name, library_name)

    # File operations
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

    # Web operations
    def fetch_web_content(self, url, content_type="text"):
        """Fetch content from a web URL"""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        if content_type == "json":
            return response.json()
        else:
            return response.text

    def search_web(self, query, search_engine="google", max_results=10):
        """Search the web using a search engine"""
        # This is a simplified implementation
        # In practice, you might use a search API like Google Custom Search API
        search_urls = {
            "google": f"https://www.google.com/search?q={query}",
            "duckduckgo": f"https://duckduckgo.com/html/?q={query}",
        }

        # For demonstration, we'll return mock results
        # In a real implementation, you'd parse search results
        mock_results = []
        for i in range(min(max_results, 5)):
            mock_results.append(
                {
                    "title": f"Search Result {i+1} for {query}",
                    "url": f"https://example.com/result{i+1}",
                    "snippet": f"This is a sample snippet for search result {i+1}",
                }
            )

        return mock_results

    def extract_text_from_html(self, html_content):
        """Extract text content from HTML"""
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            return soup.get_text()
        except ImportError:
            # Fallback if BeautifulSoup is not available
            import re

            # Simple regex to remove HTML tags
            clean = re.compile("<.*?>")
            return re.sub(clean, "", html_content)
