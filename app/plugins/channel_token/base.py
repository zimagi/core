from systems.plugins.index import BasePlugin
from utility.data import normalize_value, flatten_dict
from utility.validation import validate_flattened_dict


class ChannelTokenParseError(Exception):
    pass


class BaseProvider(BasePlugin("channel_token")):

    def __init__(self, type, name, command, **config):
        super().__init__(type, name, command)
        self.import_config(config)

    def load(self, message):
        if isinstance(message, dict):
            message = validate_flattened_dict(
                flatten_dict(normalize_value(message), self.field_fields),
                self.field_filters,
            )
        return message
