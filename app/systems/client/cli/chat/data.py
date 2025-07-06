from datetime import datetime


class ChatMessage:
    def __init__(self, content, time=None, sender="system", is_user=False):
        self.content = content
        self.sender = sender
        self.is_user = is_user
        self.time = time if time else datetime.now()
