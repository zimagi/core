from systems.plugins.index import BaseProvider

from .base import ChannelTokenParseError


class Provider(BaseProvider("channel_token", "data_type")):

    def __init__(self, type, name, command, **config):
        super().__init__(type, name, command, **config)
        if self.field_value not in self.command.manager.index.get_facade_index():
            raise ChannelTokenParseError(f"Data type {self.field_value} does not exist")

        self.facade = self.command.facade(self.field_value, False)

    def load(self, message):
        if isinstance(message, (str, int)):
            instances = self.facade.values(*self.field_fields, id=message, **self.field_filters)
            message = instances[0] if len(instances) > 0 else None
        else:
            instances = self.facade.values(*self.field_fields, id=message[self.field_id_field], **self.field_filters)
            message = instances[0] if len(instances) > 0 else None
        return message
