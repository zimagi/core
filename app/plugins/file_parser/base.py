from systems.plugins.index import BasePlugin
from utility.filesystem import load_file


class BaseProvider(BasePlugin("file_parser")):

    def check_binary(self):
        return False

    def parse(self, file_path):
        try:
            return self.parse_file(file_path)
        except Exception as e:
            return ""

    def parse_file(self, file_path):
        return self.parse_content(load_file(file_path, self.check_binary()))

    def parse_content(self, content):
        # Override in subclass
        return content
