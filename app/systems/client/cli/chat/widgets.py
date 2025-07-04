from textual.widgets import Static
from textual.reactive import reactive
from rich.markdown import Markdown
from datetime import datetime


class MessageDisplay(Static):

    def __init__(self, sender, content, **kwargs):
        super().__init__(**kwargs)
        self.sender = sender
        self.content = content

    def compose(self):
        yield Label(f"[b]{self.sender}[/b] @ {datetime.now().strftime('%H:%M:%S')}", classes="sender-label")
        yield Static(Markdown(self.content), classes="message-content")

    def on_mount(self):
        self.add_class("message-display")
