from systems.commands.index import Agent
from utility.data import Collection


class Librarian(Agent("librarian")):

    def exec(self):
        file_types = list(self.manager.index.get_plugin_providers("file_parser").keys())

        for package in self.listen("library:index", state_key="librarian"):
            message = Collection(**package.message)
            with self.run_as(message.user) as user:
                file_info = self.get_file_info(message.library, message.path)

                if file_info.file_type and file_info.file_type in file_types:
                    file_parser = self.get_provider("file_parser", file_info.file_type)
                    file_text = file_parser.parse(file_info.full_file_path)
