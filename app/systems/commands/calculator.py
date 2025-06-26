from systems.commands.processor import Processor


class Calculator(Processor):
    def __init__(self, command, display_only=False, reset=False, disable_save=False):
        super().__init__(command, "calculation", display_only=display_only, disable_save=disable_save)
        self.reset = reset

    def provider_process(self, name, spec):
        self.command.get_provider(self.plugin_key, spec[self.plugin_key], name, spec).process(self.reset)
