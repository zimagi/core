import time

import redis
from django.conf import settings
from utility.data import Collection, dump_json, load_json
from utility.mutex import MutexError, MutexTimeoutError, check_mutex
from utility.time import Time


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


class ManagerCommunicationMixin:
    def communication_connection(self):
        if not getattr(self, "_communication_connection", None):
            if settings.REDIS_COMMUNICATION_URL:
                self._communication_connection = redis.from_url(
                    settings.REDIS_COMMUNICATION_URL, encoding="utf-8", decode_responses=True
                )
            else:
                self._communication_connection = None
        return self._communication_connection

    def cleanup_communication(self, key):
        if self.communication_connection():
            self._communication_connection.close()

    def listen(self, channel, timeout=0, block_sec=0.5, state_key=None, terminate_callback=None):
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
                    with check_mutex(f"manager-listen-{channel}", force_remove=True):
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
                        yield Collection(
                            time=Time().to_datetime(package["time"]),
                            sender=package["sender"],
                            message=load_json(package["message"]) if int(package["json"]) else package["message"],
                        )
                        start_time = time.time()

                    current_time = time.time()

                    if timeout and ((current_time - start_time) > timeout):
                        break

                except (MutexError, MutexTimeoutError):
                    continue

    def send(self, channel, message, sender=""):
        connection = self.communication_connection()
        if connection:
            try:
                if isinstance(message, Collection):
                    message = message.export()

                connection.xadd(
                    channel_communication_key(channel),
                    {
                        "time": Time().now_string,
                        "sender": sender,
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
