from systems.plugins.index import BasePlugin


class BaseProvider(BasePlugin("sentence_parser")):

    def __init__(self, type, name, command, **options):
        super().__init__(type, name, command)
        self.import_config(options)
        self.initialize_model()

    def initialize_model(self):
        # Implement in subclasses if needed
        pass

    def split(self, text):
        raise NotImplementedError("Sentence Parser providers must implement split method")
