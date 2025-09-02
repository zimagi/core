import os

from systems.commands.index import Agent


class FileParser(Agent("file_parser")):

    def exec(self):
        for package in self.listen("file:parse", state_key="file_parser"):
            file_path = package.message
            try:
                with self.run_as(package.user) as user:
                    file_text = self._process_file_parser_request(file_path)
                    self.success(f"Successfully parsed file: {file_path}")
                    self.send(package.sender, file_text)

            except Exception as error:
                self.error(f"File parser request for {file_text} failed with error: {error}")

    def _process_file_parser_request(self, file_path):
        extension = self._get_file_type(file_path)
        file_types = list(self.manager.index.get_plugin_providers("file_parser").keys())
        file_text = ""

        if extension and extension in file_types:
            file_parser = self.get_provider("file_parser", extension)
            file_text = file_parser.parse(file_path)
        return file_text

    def _get_file_type(self, file_path):
        _, ext = os.path.splitext(file_path)
        return ext.lower()[1:] if ext else None
