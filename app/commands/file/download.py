from systems.commands.index import Command


class Download(Command("file.download")):

    def exec(self):
        file_path = self.download_file(self.library_name, self.file_path, self.file_url, self.file_type)
        self.success(f"File downloaded successfully to {file_path}")
