from django.conf import settings

from systems.plugins.index import BasePlugin


class BaseProvider(BasePlugin("document_source")):

    def download(self, folders, root_directory):
        raise NotImplementedError("Method download must be implemented by all document_source plugin providers")

    def _parse_file(self, file_path):
        return self.command.submit("file:parse", file_path)
