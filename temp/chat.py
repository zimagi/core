from datetime import datetime
import random
from rich import box
from rich.markdown import Markdown as RichMarkdown
from rich.console import Group
from rich.text import Text
from rich.panel import Panel
from rich.style import Style
from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import Container, ScrollableContainer
from textual.widgets import Footer, Markdown, TextArea, Button, Static
from textual.message import Message


def generate_random_markdown():
    """Generate random markdown content"""
    markdown_types = [
        lambda: f"# Heading\n\nRandom content at {datetime.now().strftime('%H:%M:%S')}",
        lambda: f"**Important** update:\n\n- Item 1\n- Item 2\n- Item 3",
        lambda: f"```python\n# Code sample\ndef hello():\n    print('Hello at {datetime.now().strftime('%H:%M:%S')}')\n```",
        lambda: f"> Quote of the moment\n>\n> Random wisdom here",
        lambda: f"Here's a table:\n\n| Header 1 | Header 2 |\n|----------|----------|\n| Cell A   | Cell B   |\n| Cell C   | Cell D   |",
    ]
    return random.choice(markdown_types)()


class MessageInput(TextArea):
    """Custom text area for chat messages"""

    class SubmitRequest(Message):
        """Event to request message submission"""

    def action_paste(self) -> None:
        """Handle paste from clipboard"""
        try:
            import pyperclip

            text = pyperclip.paste()
            if text:
                self.insert(text)
        except ImportError:
            self.notify("pyperclip package required for paste functionality", severity="error")

    def on_paste(self, event) -> None:
        """Handle paste events"""
        self.insert(event.text)

    def _create_right_click_menu(self):
        from textual.widgets import MenuItem

        menu = super()._create_right_click_menu()
        # Add paste at top of context menu with keyboard shortcut
        menu.items.insert(0, MenuItem("Paste", "action_paste", "Ctrl+V"))
        return menu

    async def on_mount(self) -> None:
        """Initialize widget"""
        self.app.set_focus(self)

    def key_ctrl_v(self) -> None:
        """Handle paste with Ctrl+V"""
        self.action_paste()

    def _on_key(self, event) -> None:
        """Handle key events"""
        super()._on_key(event)

    def key_enter(self) -> None:
        """Allow Enter key to create newlines"""
        if not self.has_focus or not self.has_composition:
            self.insert_text("\n")


class ChatMessage(Static):
    """Custom widget for chat messages with natural height"""

    def __init__(self, content: str, is_user: bool = False) -> None:
        super().__init__()
        self.content = content
        self.is_user = is_user

    def compose(self) -> ComposeResult:
        """Compose the message with header and content"""
        timestamp = datetime.now().strftime("%H:%M")
        sender = "You" if self.is_user else "Server"

        # Custom markdown styles
        markdown = RichMarkdown(self.content, style=Style(color="white"), code_theme="monokai", hyperlinks=False)

        # Header with timestamp
        header = Text.from_markup(f"[b]{timestamp} {sender}[/b]", style=Style(color="bright_black"))

        # Combine header and content
        content = Group(header, markdown)

        # Panel styling
        border_style = Style(color="bright_blue" if self.is_user else "bright_green")
        yield Static(
            Panel(content, border_style=border_style, box=box.ROUNDED, padding=(1, 2), style=Style(bgcolor="black")),
            classes="user-message" if self.is_user else "bot-message",
        )


class ChatApp(App):
    """Chat application with multi-line input and Markdown rendering."""

    CSS = """
    Screen {
        layout: vertical;
        overflow: hidden;
    }
    #chat-container {
        height: 1fr;
        overflow: hidden;
        layout: vertical;
    }
    #chat-history {
        height: 100%;
        overflow-y: auto;
        scrollbar-color: $accent;
        scrollbar-color-hover: $accent-lighten-1;
    }
    .user-message {
        margin: 1 0;
        width: 100%;
        height: auto;
    }
    .bot-message {
        margin: 1 0;
        width: 100%;
        height: auto;
    }
    /* Basic message styling */
    .message-content {
        margin: 1 0;
    }

    /* Rich Markdown styling is handled via the Rich renderer's built-in styles */
    #input-area {
        layout: horizontal;
        height: auto;
        border-top: solid $primary;
        padding: 1;
        background: $surface;
        margin: 1 0 0 0;
    }
    #message-input {
        width: 1fr;
        height: auto;
        min-height: 5;
        max-height: 20;
        overflow-y: auto;
        scrollbar-color: $accent;
        scrollbar-color-hover: $accent-lighten-1;
        border: none !important;
    }
    #message-input:focus {
        border: none;
    }
    #paste-button {
        width: 8;
        min-width: 8;
        margin: 1;
    }

    #submit-button {
        width: 12;
        min-width: 12;
        margin: 1;
    }
    .message-header {
        padding: 1;
        text-style: bold;
        color: $text-muted;
    }
    .message-content {
        padding: 1;
    }
    #chat-history {
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Container(id="chat-container"):
            yield ScrollableContainer(id="chat-history")
        with Container(id="input-area"):
            yield MessageInput(id="message-input", language="markdown", show_line_numbers=False, tab_behavior="indent")
            yield Button("Paste", id="paste-button", variant="default")
            yield Button("Submit", id="submit-button", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Setup app on startup."""
        self.query_one("#message-input").focus()
        history = self.query_one("#chat-history")
        history.scroll_end(animate=False)

        # Add initial welcome message
        self.add_message(
            "### Welcome to Terminal Chat!\n\n"
            "Type your message below and click Submit.\n"
            "Use **Markdown** formatting and multi-line messages!\n\n"
            "Random system messages will appear periodically.",
            is_user=False,
        )

        # Start periodic system messages
        self.send_periodic_messages()

    def add_message(self, content: str, is_user: bool = False) -> None:
        """Add a message to the chat history."""
        history = self.query_one("#chat-history")
        message = ChatMessage(content, is_user)
        history.mount(message)
        # Allow Textual to compute new layout
        self.call_after_refresh(history.scroll_end, animate=True)

    def send_periodic_messages(self) -> None:
        """Send periodic system messages"""

        def send_message():
            self.add_message(generate_random_markdown(), is_user=False)

        # Schedule message every 30 seconds
        self.set_interval(30, send_message)

    def add_mock_server_message(self) -> None:
        """Add a simulated server message"""
        self.add_message(
            "### Server Message\nThis is an **automated** response.\n"
            "You're chatting in a terminal application "
            f"at {datetime.now().strftime('%H:%M:%S')}. This is a "
            "persistent scrollable chat window.\n\n"
            "Messages maintain their natural height and the scrollbar "
            "works to navigate older messages.\n\n"
            "Random messages will appear every 30 seconds.",
            is_user=False,
        )

    @on(Button.Pressed, "#paste-button")
    def handle_paste(self) -> None:
        """Handle paste button press."""
        input_widget = self.query_one("#message-input", MessageInput)
        input_widget.action_paste()
        input_widget.focus()

    @on(Button.Pressed, "#submit-button")
    @on(MessageInput.SubmitRequest)
    def handle_submission(self) -> None:
        """Handle message submission."""
        self.submit_message()

    def submit_message(self) -> None:
        """Process message submission."""
        input_widget = self.query_one("#message-input", MessageInput)
        if text := input_widget.text.strip():
            self.add_message(text, is_user=True)
            input_widget.text = ""
            input_widget.focus()


if __name__ == "__main__":
    ChatApp().run()
