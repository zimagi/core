from django.conf import settings
from utility.data import dump_json, flatten_dict, normalize_value
from utility.display import format_exception_info, format_traceback
from utility.validation import validate_flattened_dict
from utility.runtime import debug


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

        debug(self.sensor_name, "Communication sensor name")
        debug(self.sensor_spec, "Communication sensor spec")
        debug(self._sensor_tokens, "Communication sensor tokens")

    def listen(self, filters, fields):
        debug(f"Starting to listen at {self.sensor_name} with {self.sensor_key} sensor key")
        debug(filters, "Sensory filters")
        debug(fields, "Sensory message fields")

        for package in self.command.listen(self.sensor_name, state_key=self.sensor_key):
            try:
                self.command.notice(f"Received new event: {package}")
                message = self._load_message(package, filters, fields)
                if message:
                    debug("Processing sensory message")
                    yield SensoryEvent(package, message)
            except Exception as error:
                self.send_error(self.sensor_name, error, package)
                # self.send(self.sensor_name, package.message, package.sender)
                raise
        self.command.notice("Execution cycle complete")

    def send(self, channel, event, response, field_map):
        channel = event.package.sender if channel == "sender" else channel
        variables = {
            "self": self.command.service_id,
            "user": self.user if self.user else settings.ADMIN_USER,
            "time": self.command.time.now_string,
            "sensor": self.sensor_name,
            "sender": event.package.sender,
            "message": event.message,
            "response": response.result,
            "duration": response.time,
            "memory": response.memory,
        }
        message = self._translate_message(variables, field_map)

        debug(channel, "Communication channel")
        debug(variables, "Communication variables")
        debug(field_map, "Communication fieldmapping")
        debug(message, "Communication send message")

        self.command.send(channel, message)

    def send_error(self, channel, error, package=None):
        variables = {
            "time": self.command.time.now_string,
            "self": self.command.service_id,
            "user": self.user if self.user else settings.ADMIN_USER,
            "sensor": self.sensor_name,
            "sender": package.sender if package else None,
            "message": package.message if package else None,
            "error": str(error),
            "traceback": format_traceback(),
            "info": format_exception_info(),
        }
        debug(f"error:{channel}", "Communication error channel")
        debug(variables, "Communication error variables")

        self.command.send(f"error:{channel}", variables)

    def _load_message(self, package, filters, fields):
        message_filters = self.command.manager.index.get_plugin_providers("message_filter")
        message = package.message
        plugin_filters = {}
        query_filters = {}

        debug("Loading communication message received")
        debug(message_filters, "Message filters")
        debug(message, "Initial message received")

        for filter_name, filter_value in filters.items():
            if filter_name in message_filters:
                plugin_filters[filter_name] = filter_value
            else:
                query_filters[filter_name] = filter_value

        debug(plugin_filters, "Plugin filters")
        debug(query_filters, "Query filters")

        if self._sensor_tokens:
            debug("Processing sensor tokens")
            for token, token_value in self._sensor_tokens.items():
                token_parser = self.command.get_provider(
                    "channel_token",
                    token,
                    value=token.value,
                    fields=fields,
                    filters=query_filters,
                    id_field=token.field,
                )
                message = token_parser.load(message)

        elif isinstance(message, dict):
            debug("Processing query filters")
            message = validate_flattened_dict(
                flatten_dict(normalize_value(message), fields),
                query_filters,
            )
        else:
            debug("Processing message field")
            if fields and "message" not in fields:
                self.command.error("Message field message of scalar channel value it not specified")

            message = validate_flattened_dict({"message": normalize_value(message)}, query_filters)

        if plugin_filters:
            debug("Processing plugin filters")
            for filter_name, provider in plugin_filters.items():
                message_filter = self.command.get_provider("message_filter", filter_name)
                message = message_filter.filter(message, filter_value)
                if not message:
                    break

        debug(message, "Final processed message")
        return message

    def _translate_message(self, message, field_map):
        flattened_message = flatten_dict(normalize_value(message))
        translation = {}

        debug(flattened_message, "Flattened message")

        if field_map:
            for field, flattened_field in field_map.items():
                if flattened_field in flattened_message:
                    translation[field] = flattened_message[flattened_field]
                else:
                    translation[field] = flattened_field
        else:
            translation = message

        debug(translation, "Translated message")
        return translation
