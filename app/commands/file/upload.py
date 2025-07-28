from systems.commands.index import Command


class Upload(Command("file.upload")):

    def exec(self):
        self.info(self.library_name)
        self.info(self.file_path)
        self.info(self.file_type)
        self.info(self.file_content)
        self.success("We are successful")
