from systems.commands.index import Command


class Send(Command("chat.send")):

    def exec(self):
        if self.chat_text:
            time = self.time.now_string
            self.send(
                "chat:message",
                {
                    "user": self.active_user.name,
                    "name": self.chat_name,
                    "message": self.chat_text,
                    "time": time,
                },
            )
            self.save_user_message(self.chat_name, self.chat_text, time=time)
