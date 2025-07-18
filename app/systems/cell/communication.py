import logging

from django.conf import settings
from utility.data import flatten_dict, normalize_value
from utility.display import format_exception_info, format_traceback
from utility.validation import validate_flattened_dict

logger = logging.getLogger(__name__)


class SensoryEvent:
    def __init__(self, package, message):
        self.package = package
        self.message = message


class CommunicationProcessor:
    def __init__(self, command, user, sensor_key):
        self.command = command
        self.user = user
        self.sensor_key = sensor_key
        self.sensor_name = None
        self.sensor_spec = None
        self._sensor_tokens = None

    def set_sensor(self, channel):
        self.sensor_name = channel
        self.sensor_spec = self.command.manager.get_channel_spec(self.sensor_name)
        if not self.sensor_spec:
            self.command.error(f"Channel name {self.sensor_name} is not a valid sensory channel")

        self._sensor_tokens = self.command.get_channel_tokens(self.sensor_name)
        logger.debug(f"Set sensor to: {self.sensor_name}")

    def listen(self, filters, fields, id_field=None):
        logger.debug(f"Starting to listen for {self.sensor_name}")
        for package in self.command.listen(self.sensor_name, state_key=self.sensor_key):
            try:
                message = self._load_message(package, filters, fields, id_field)
                if message:
                    yield SensoryEvent(package, message)
            except Exception as error:
                self.send_error(self.sensor_name, error, package)
                # self.send(self.sensor_name, package.message, package.sender)
                raise

    def send(self, channel, event, response):
        channel = event.package.sender if channel == "sender" else channel
        message = self._translate_message(
            {
                "self": self.command.service_id,
                "user": self.user if self.user else settings.ADMIN_USER,
                "sensor": self.sensor_name,
                "sender": event.package.sender,
                "message": event.message,
                "response": response.result,
                "time": response.time,
                "memory": response.memory,
            }
        )
        logger.info(f"Sending data to channel {channel}: {message}")
        self.command.send(channel, message)

    def send_error(self, channel, error, package=None):
        self.command.send(
            f"error:{channel}",
            {
                "time": self.command.time.now_string,
                "self": self.command.service_id,
                "user": self.user if self.user else settings.ADMIN_USER,
                "sensor": self.sensor_name,
                "sender": package.sender if package else None,
                "message": package.message if package else None,
                "error": str(error),
                "traceback": "\n".join([item.strip() for item in format_traceback()]),
                "info": "\n".join([item.strip() for item in format_exception_info()]),
            },
        )

    def _load_message(self, package, filters, fields, id_field=None):
        message_filters = self.command.manager.index.get_plugin_providers("message_filter")
        message = package.message
        plugin_filters = {}
        query_filters = {}

        for filter_name, filter_value in filters.items():
            if filter_name in message_filters:
                plugin_filters[filter_name] = filter_value
            else:
                query_filters[filter_name] = filter_value

        if self._sensor_tokens:
            for token, token_value in self._sensor_tokens.items():
                token_parser = self.command.get_provider(
                    "channel_token",
                    token,
                    value=token_value,
                    fields=fields,
                    filters=query_filters,
                    id_field=id_field,
                )
                message = token_parser.load(message)

        elif isinstance(message, dict):
            message = validate_flattened_dict(
                flatten_dict(normalize_value(message), fields),
                query_filters,
            )
        else:
            if fields and "message" not in fields:
                self.command.error("Message field message of scalar channel value it not specified")

            message = validate_flattened_dict({"message": normalize_value(message)}, query_filters)

        for filter_name, provider in plugin_filters.items():
            message_filter = self.command.get_provider("message_filter", filter_name)
            message = message_filter.filter(message, filter_value)
            if not message:
                break

        return message

    def _translate_message(self, message, field_map):
        flattened_message = flatten_dict(normalize_value(message))
        translation = {}

        if field_map:
            for field, flattened_field in field_map.items():
                translation[field] = flattened_message[flattened_field]
        else:
            translation = message

        return translation
