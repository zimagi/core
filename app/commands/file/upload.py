from systems.commands.index import Command


class Upload(Command("file.upload")):

    def exec(self):
        file_path = self.upload_file(self.library_name, self.file_path, self.file_content)
        self.success(f"File uploaded successfully to {file_path}")
