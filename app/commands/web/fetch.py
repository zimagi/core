from systems.commands.index import Command


class Fetch(Command("web.fetch")):

    def exec(self):
        # Fetch web content
        content = self.fetch_web_content(self.file_url)

        # Save to library if specified
        if self.library_name and self.file_path:
            file_path = self.upload_file(self.library_name, self.file_path, content, self.file_type)
            self.success(f"Web content fetched and saved to {file_path}")
        else:
            self.success("Web content fetched successfully")
            self.data("Page content", content, "content")
