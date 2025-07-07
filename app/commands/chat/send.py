from systems.commands.index import Command


class Send(Command("chat.send")):

    def exec(self):
        if self.chat_message:
            self.send(
                "chat:message",
                {
                    "user": self.active_user.name,
                    "name": self.chat_name,
                    "message": self.chat_message,
                },
            )
