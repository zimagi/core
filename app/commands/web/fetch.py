from systems.commands.index import Command


class Fetch(Command("web.fetch")):

    def exec(self):
        content = self.fetch_web_content(self.file_url)

        if self.library_name and self.file_path:
            file_path = self.upload_file(self.library_name, self.file_path, content.source, self.file_type)
            self.success(f"Web content fetched and saved to {file_path}")
        else:
            self.success("Web content fetched successfully")
            self.data("Page content", content, "content")
