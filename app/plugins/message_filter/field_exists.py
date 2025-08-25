from systems.plugins.index import BaseProvider


class Provider(BaseProvider("message_filter", "field_exists")):

    def filter(self, message, value):
        if value in message and message[value] is not None:
            return message
        return None
