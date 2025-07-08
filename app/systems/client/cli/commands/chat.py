from django.conf import settings

from .base import BaseExecutable
from ..chat.app import ChatApp


class ChatCommand(BaseExecutable):

    def passthrough(self):
        return True

    def exec(self):
        self.app = ChatApp(self, css_path=os.path.join(settings.APP_DIR, "systems/client/cli/chat/style.tcss"))
        self.app.run()

    def handle_message(self, message):
        if not message.system:
            # self.app.add_server_message("Server", message.format())
            self.app.add_message(chat_name, content, time=None, sender=None, is_user=False)
