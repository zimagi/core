from systems.commands.index import Command


class Listen(Command("chat.listen")):

    def exec(self):
        for package in self.listen(
            "chat:message",
            state_key=f"core_chat_{self.active_user.name}",
            timeout=self.listen_timeout,
            block_sec=self.listen_timeout,
        ):
            if package.message.get("user", None) and package.message["user"] != self.active_user.name:
                self.data("Message", package.message, "message")
