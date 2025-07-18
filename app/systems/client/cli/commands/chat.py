import os

from django.conf import settings

from ..chat.app import ChatApp
from .base import BaseExecutable


class ChatCommand(BaseExecutable):

    def passthrough(self):
        return True

    def exec(self):
        self.app = ChatApp(self, css_path=os.path.join(settings.APP_DIR, "systems/client/cli/chat/style.tcss"))
        self.app.run()
