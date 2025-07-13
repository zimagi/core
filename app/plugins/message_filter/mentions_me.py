import re

from systems.plugins.index import BaseProvider
from .base import MessageFilterParseError


class Provider(BaseProvider("message_filter", "mentions_me")):

    def filter(self, message, value):
        try:
            agent_user = self.command.agent_user
        except Exception:
            raise MessageFilterParseError(
                f"Message Filter mentions_me requires the agent_user attribute (cell agent descendents)"
            )
        if value not in message:
            raise MessageFilterParseError(f"Message Filter value {value} not in message: {message}")

        if re.search(f"@{agent_user}", message[value]):
            return message
        return None
