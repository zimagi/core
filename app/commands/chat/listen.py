import math

from systems.commands.index import Command


class Listen(Command("chat.listen")):

    def exec(self):
        for package in self.listen(
            "chat:message",
            state_key=self.listen_state_key if self.listen_state_key else f"core_chat_{self.active_user.name}",
            timeout=self.listen_timeout,
            block_sec=math.ceil(self.listen_timeout / 2),
        ):
            chat_names = self._chat.field_values("name", user=self.active_user)
            message = package.message

            if message["name"] in chat_names:
                self.data("Message", message, "message")
                if message["user"] != self.active_user.name:
                    self.save_user_message(
                        message["name"], message["message"], time=message["time"], user=message["user"], role="assistant"
                    )
