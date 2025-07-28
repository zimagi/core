from systems.commands.index import Command


class Search(Command("web.search")):

    def exec(self):
        self.info(self.library_name)
        self.info(self.search_text)
        self.info(self.max_results)
        self.success("We are successful")
