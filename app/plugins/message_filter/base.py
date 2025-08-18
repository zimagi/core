from systems.plugins.index import BasePlugin


class MessageFilterParseError(Exception):
    pass


class BaseProvider(BasePlugin("message_filter")):

    def filter(self, message, value):
        # Override in subclass.
        return message
