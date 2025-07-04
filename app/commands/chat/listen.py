from systems.commands.index import Command


class Listen(Command("chat.listen")):

    def exec(self):
        for package in self.listen(
            "chat:response", state_key="core_chat", timeout=self.listen_timeout, block_sec=self.listen_timeout
        ):
            self.info(package.message)
