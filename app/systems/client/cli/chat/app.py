from textual import on, work
from textual.app import App
from textual.containers import ScrollableContainer, Vertical, Horizontal
from textual.widgets import Input, Button
from textual.reactive import reactive

from .widgets import MessageDisplay


class ChatApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Toggle dark mode")]

    CSS = """
        Screen {
            layout: vertical;
        }

        #chat-area {
            height: 1fr;
            width: 100%;
            overflow-y: scroll;
            background: $panel;
        }

        .message-display {
            padding: 1;
            margin: 2 0;
            border: solid $primary;
            border-title-align: center;
        }

        .sender-label {
            background: $primary;
            color: $text;
            padding: 0 1;
            margin-bottom: 1;
        }

        .message-content {
            padding: 0 1;
        }

        #input-area {
            height: auto;
            dock: bottom;
            padding: 1;
            background: $boost;
            width: 100%;
        }

        Input {
            width: 80%;
        }

        Button {
            width: 18%;
            margin-left: 2;
        }
    """

    current_chat = reactive([])

    def __init__(self, command, **kwargs):
        super().__init__(**kwargs)
        self.command = command

    def compose(self):
        with Vertical(id="main-container"):
            with ScrollableContainer(id="chat-area"):
                # Initial messages load here dynamically
                pass

            with Horizontal(id="input-area"):
                yield Input(placeholder="Type your message...", id="message-input")
                yield Button("Send", id="send-button", variant="primary")

    async def on_mount(self):
        self.title = "Zimagi Chat"
        self.sub_title = "Press Ctrl+C to exit"
        self.server_listener = self.listen_for_messages()

    @work(exclusive=False, thread=True)
    async def listen_for_messages(self):
        while True:
            try:
                self.command.client.execute("chat listen", chat_name=self.command.chat_name)
            except Exception as e:
                self.log.error(f"Server error: {e}")

    def add_message(self, sender, content):
        new_message = MessageDisplay(sender, content)
        self.query_one("#chat-area").mount(new_message)
        self.current_chat.append((sender, content))
        self.query_one("#chat-area").scroll_end(animate=True)

    def add_server_message(self, sender, content):
        def callback():
            self.add_message(sender, content)
            self.query_one("#chat-area").scroll_end(animate=False)

        self.call_from_thread(callback)

    @on(Button.Pressed, "#send-button")
    @on(Input.Submitted, "#message-input")
    def submit_message(self):
        input = self.query_one("#message-input")
        if text := input.value.strip():
            self.add_message("You", text)
            input.value = ""
            self.handle_message_send(text)

    def handle_message_send(self, text):
        self.log(f"Sending message: {text}")
        self.command.client.execute("chat send", chat_name=self.command.chat_name, chat_message=text)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
