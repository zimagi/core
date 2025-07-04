from .base import BaseExecutable
from ..chat.app import ChatApp


class ChatCommand(BaseExecutable):

    def exec(self):
        self.app = ChatApp(self)
        self.app.run()

    def handle_message(self, message):
        if not message.system:
            self.app.add_server_message("Server", message.format())
