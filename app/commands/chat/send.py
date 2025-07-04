from systems.commands.index import Command


class Send(Command("chat.send")):

    def exec(self):
        if self.chat_clear:
            chat = self._chat.retrieve(f"{self.active_user.name}:{self.chat_name}")
            chat.clear_messages()
        self.send("chat:request", {"user": self.active_user.name, "name": self.chat_name, "message": self.chat_message})
