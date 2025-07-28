from systems.commands.index import Command


class Fetch(Command("web.fetch")):

    def exec(self):
        self.info(self.library_name)
        self.info(self.file_path)
        self.info(self.file_type)
        self.info(self.file_url)
        self.success("We are successful")
