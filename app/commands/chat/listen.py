from systems.commands.index import Command


class Listen(Command("chat.listen")):

    def exec(self):
        for package in self.listen(
            "chat:message",
            state_key=self.listen_state_key if self.listen_state_key else f"core_chat_{self.active_user.name}",
            timeout=self.listen_timeout,
            block_sec=self.listen_timeout,
        ):
            self.data("Message", package.message, "message")
