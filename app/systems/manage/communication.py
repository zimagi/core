import logging
import re
import time

import redis
from django.conf import settings
from utility.data import Collection, dump_json, load_json
from utility.mutex import MutexError, MutexTimeoutError, check_mutex
from utility.time import Time
from utility.validation import TypeValidator

logger = logging.getLogger(__name__)


def channel_communication_key(key):
    return f"channel:comm:{key}"


def channel_listen_base_state_key(key):
    return f"manager-listen-state-{key}"


def channel_listen_state_key(key, state_key=None):
    if state_key is None:
        state_key = "default"
    return f"{channel_listen_base_state_key(key)}:{state_key}"


class CommunicationError(Exception):
    pass


class ChannelValidationError(Exception):
    pass


class ManagerCommunicationMixin:
    def communication_connection(self):
        self._communication_connection = None
        if settings.REDIS_COMMUNICATION_URL:
            self._communication_connection = redis.from_url(
                settings.REDIS_COMMUNICATION_URL, encoding="utf-8", decode_responses=True
            )
            try:
                self._communication_connection.ping()
            except redis.exceptions.ConnectionError:
                self._communication_connection = None

        return self._communication_connection

    # def cleanup_communication(self, key):
    #     connection = self.communication_connection()
    #     if connection:
    #         connection.close()

    def listen(self, channel, timeout=0, block_sec=1, state_key=None, terminate_callback=None):
        communication_key = channel_communication_key(channel)
        state_key = channel_listen_state_key(channel, state_key)

        def _default_terminate_callback(channel):
            return False

        if terminate_callback is None or not callable(terminate_callback):
            terminate_callback = _default_terminate_callback

        connection = self.communication_connection()
        if connection:
            start_time = time.time()
            current_time = start_time

            if not connection.exists(state_key):
                connection.set(state_key, 0)

            while not terminate_callback(channel):
                try:
                    with check_mutex(f"manager-listen-{channel}-{state_key}", force_remove=True):
                        last_id = connection.get(state_key)
                        stream_data = connection.xread(
                            count=1, block=(block_sec * 1000), streams={communication_key: last_id if last_id else 0}
                        )
                        if stream_data:
                            message = stream_data[0][1][-1]
                            last_id = message[0]
                            package = message[1]

                            connection.set(state_key, last_id)

                    if stream_data:
                        try:
                            message = load_json(package["message"]) if int(package["json"]) else package["message"]
                            message = self._validate_channel_message(channel, message)
                            yield Collection(
                                time=Time().to_datetime(package["time"]),
                                sender=package["sender"],
                                user=package["user"],
                                message=message,
                            )
                            start_time = time.time()

                        except ChannelValidationError as error:
                            logger.error(f"Communication listener validation error: {error}")

                    current_time = time.time()

                    if timeout and ((current_time - start_time) > timeout):
                        break

                except (MutexError, MutexTimeoutError):
                    continue

    def send(self, channel, message, sender="", user=None):
        connection = self.communication_connection()
        if connection:
            try:
                if isinstance(message, Collection):
                    message = message.export()
                message = self._validate_channel_message(channel, message)

                connection.xadd(
                    channel_communication_key(channel),
                    {
                        "time": Time().now_string,
                        "sender": sender,
                        "user": user,
                        "message": dump_json(message) if isinstance(message, (list, tuple, dict)) else message,
                        "json": 1 if isinstance(message, (list, tuple, dict)) else 0,
                    },
                )
            except Exception as error:
                raise CommunicationError(f"Send to channel {channel} failed with error: {error}")

    def delete_stream(self, channel):
        connection = self.communication_connection()
        if connection:
            state_keys = connection.keys(f"{channel_listen_base_state_key(channel)}:*")
            try:
                connection.delete(channel_communication_key(channel))
                if state_keys:
                    connection.delete(*state_keys)
            except Exception as error:
                raise CommunicationError(f"Deletion of channel {channel} failed with error: {error}")

    def delete_stream_state(self, channel, state_key=None):
        connection = self.communication_connection()
        if connection:
            try:
                connection.delete(channel_listen_state_key(channel, state_key))
            except Exception as error:
                raise CommunicationError(f"Deletion of channel {channel} failed with error: {error}")

    def get_channel_spec(self, channel_name):
        for name, spec in self.get_spec("channels").items():
            pattern = "^" + re.sub(r"{[^}]+}", "[^:]+", name) + "$"
            if re.match(pattern, channel_name):
                return Collection(name=name, schema=spec)
        return None

    def _validate_channel_message(self, channel_name, message):
        channel_spec = self.get_channel_spec(channel_name)
        if not channel_spec:
            return message

        message_spec = channel_spec.schema.get("message", {})
        return self._validate_message_structure(message, message_spec, channel_name)

    def _validate_message_structure(self, message, spec, context):
        expected_type = spec.get("type")
        required = spec.get("required", False)
        default = spec.get("default", None)

        # Apply default if message is None and default is specified
        if message is None and default is not None:
            message = default

        # Check required fields (after applying default)
        if required and message is None:
            raise ChannelValidationError(f"Message is required for channel {context}")

        # Handle type validation if specified
        if expected_type:
            # Special case for lists
            if expected_type.startswith("list[") and expected_type.endswith("]"):
                if not isinstance(message, list):
                    raise ChannelValidationError(f"Expected list for channel {context}, got {type(message)}")

                # Extract item type from list[type] syntax
                item_type = expected_type[5:-1]
                self._validate_list_items(
                    message, item_type, spec.get("length"), spec.get("min_length"), spec.get("max_length"), context
                )
            else:
                # Standard type validation
                if not TypeValidator.is_instance(message, expected_type):
                    raise ChannelValidationError(
                        f"Expected type '{expected_type}' for channel {context}, got {type(message)}"
                    )

        # Handle dictionary validation
        if isinstance(message, dict):
            items_spec = spec.get("items", {})
            if items_spec:
                validated_dict = {}
                for field, field_spec in items_spec.items():
                    field_value = message.get(field, field_spec.get("default"))
                    try:
                        validated_dict[field] = self._validate_message_structure(
                            field_value, field_spec, f"{context}.{field}"
                        )
                    except ChannelValidationError as e:
                        if field_spec.get("required", False):
                            raise
                message = validated_dict

        return message

    def _validate_list_items(self, items, item_type, length=None, min_length=None, max_length=None, context=""):
        # Validate list length constraints
        if length is not None and len(items) != length:
            raise ChannelValidationError(f"Expected list length {length} for {context}, got {len(items)}")
        if min_length is not None and len(items) < min_length:
            raise ChannelValidationError(f"List length must be at least {min_length} for {context}, got {len(items)}")
        if max_length is not None and len(items) > max_length:
            raise ChannelValidationError(f"List length must be at most {max_length} for {context}, got {len(items)}")

        # Validate each item's type
        for index, item in enumerate(items):
            if not TypeValidator.is_instance(item, item_type):
                raise ChannelValidationError(
                    f"Expected type '{item_type}' for item {index} in list {context}, got {type(item)}"
                )
