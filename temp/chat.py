import asyncio
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
from textual.widgets import Footer, Markdown, TextArea, Button, Static, Input
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

    BINDINGS = [
        ("ctrl+s", "submit", "Submit"),
        ("ctrl+c", "copy", "Copy"),
        ("ctrl+v", "paste", "Paste"),
    ]

    class SubmitRequest(Message):
        """Event to request message submission"""

    async def on_mount(self) -> None:
        """Initialize widget"""
        self.app.set_focus(self)

    def action_submit(self) -> None:
        """Handle message submission"""
        self.app.submit_message()

    def action_copy(self) -> None:
        """Copy selected text to clipboard"""
        try:
            import pyperclip

            selected_text = self.selected_text
            if selected_text:
                pyperclip.copy(selected_text)
        except ImportError:
            self.app.notify("pyperclip package required for copy functionality", severity="error")

    def action_paste(self) -> None:
        """Handle paste from clipboard"""
        try:
            import pyperclip

            text = pyperclip.paste()
            if text:
                self.insert(text)
        except ImportError:
            self.app.notify("pyperclip package required for paste functionality", severity="error")

    def _create_right_click_menu(self):
        from textual.widgets import MenuItem

        menu = super()._create_right_click_menu()
        # Add copy/paste at top of context menu with keyboard shortcuts
        menu.items.insert(0, MenuItem("Submit", "action_submit", "Ctrl+S"))
        menu.items.insert(1, MenuItem("Copy", "action_copy", "Ctrl+C"))
        menu.items.insert(2, MenuItem("Paste", "action_paste", "Ctrl+V"))
        return menu


class ChatNameInput(Input):
    """Custom input for chat names with enter-to-submit"""

    BINDINGS = [
        ("enter", "select_or_create_chat", "Select/Create Chat"),
    ]

    def action_select_or_create_chat(self) -> None:
        """Handle enter key press - select existing chat or create new one"""
        app = self.app
        if not isinstance(app, ChatApp):
            return

        name = self.value.strip()
        if not name:
            return

        if name in app.chats:
            # Find and click the matching chat item
            for item in app.query(".chat-item"):
                if item.name == name:
                    item.post_message(ChatItem.Clicked(item))
                    break
        else:
            # Create new chat (which will handle selection)
            app.create_new_chat(name)

        # Clear input and focus back to message input
        self.value = ""
        app.query_one("#message-input").focus()

    def _create_right_click_menu(self):
        from textual.widgets import MenuItem

        menu = super()._create_right_click_menu()
        # Add copy/paste at top of context menu with keyboard shortcuts
        menu.items.insert(0, MenuItem("Select / Create", "action_select_or_create_chat", "Enter"))
        return menu


class ChatItem(Static):
    """Widget representing a single chat in the sidebar"""

    def __init__(self, name: str, selected: bool = False, unread: bool = False) -> None:
        super().__init__()
        self._name = name
        self._selected = selected
        self._unread = unread
        self.add_class("chat-item")
        if selected:
            self.add_class("selected")
        if unread:
            self.add_class("unread")

    @property
    def unread(self) -> bool:
        """Get the unread state."""
        return self._unread

    @unread.setter
    def unread(self, value: bool) -> None:
        """Set the unread state."""
        self._unread = value
        if value:
            self.add_class("unread")
        else:
            self.remove_class("unread")

    class Clicked(Message):
        """Posted when a chat item is clicked."""

        def __init__(self, item: "ChatItem") -> None:
            self.item = item
            super().__init__()

    @property
    def name(self) -> str:
        """Get the chat name."""
        return self._name

    @property
    def selected(self) -> bool:
        """Get the selected state."""
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        """Set the selected state."""
        self._selected = value
        if value:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    def compose(self) -> ComposeResult:
        yield Static(self._name)

    def select(self) -> None:
        """Select this chat item"""
        self.selected = True

    def deselect(self) -> None:
        """Deselect this chat item"""
        self.selected = False

    def on_click(self) -> None:
        """Handle click events"""
        self.post_message(self.Clicked(self))


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

        # Static colors (dark mode always on)
        bg_color = "rgb(30,30,30)"  # Dark background
        text_color = "rgb(224,224,224)"  # Light text
        header_color = "bright_black"
        border_color = "bright_blue" if self.is_user else "bright_green"

        # Custom markdown styles with left alignment
        markdown = RichMarkdown(
            self.content, style=Style(color=text_color), code_theme="monokai", hyperlinks=False, justify="left"
        )

        # Header with timestamp (left aligned)
        header_text = Text.from_markup(f"[b]{timestamp} {sender}[/b]", justify="left", style=Style(color=header_color))

        # Combine header and content with vertical spacing
        content = Group(header_text, "", markdown)

        # Panel styling with left alignment
        border_style = Style(color=border_color)
        yield Static(
            Panel(
                content,
                border_style=border_style,
                box=box.ROUNDED,
                padding=(1, 2),
                style=Style(bgcolor=bg_color, color=text_color),
                subtitle_align="left",
                title_align="left",
            ),
            classes="user-message" if self.is_user else "bot-message",
        )


class ChatApp(App):
    # Class variable to store messages by chat name
    _chat_messages = {}

    def __init__(self):
        self._chat_lock = asyncio.Lock()  # Initialize lock before parent
        self._chat_intervals = {}
        self.current_chat = "General"
        self.chats = ["General", "Support", "Random", "Project A", "Project B"]
        self._unread_chats = set()  # Track chats with unread messages
        self._test_thread_running = True  # Flag to control test thread
        super().__init__()

    """Chat application with multi-line input and Markdown rendering."""

    CSS = """
    Screen {
        background: #1e1e1e;
        transition: background 0.3s;
    }

    Screen {
        background: #1e1e1e;
    }
    #sidebar {
        layout: vertical;
        background: #2e2e2e;
        transition: background 0.3s, border-color 0.3s;
    }
    #input-area {
        transition: background 0.3s, border-color 0.3s;
    }
    #chat-history {
        transition: background 0.3s;
    }
    .sidebar-header {
        layout: horizontal;
        height: auto;
        margin-bottom: 1;
    }
    .chat-name-input {
        width: 1fr;
        margin-right: 1;
        height: auto;
        min-height: 3;
    }
    #add-chat-button {
        width: auto;
        min-width: 5;
        margin-bottom: 1;
    }
    Screen {
        layout: vertical;
        overflow: hidden;
    }
    #chat-row {
        layout: horizontal;
        height: 1fr;
    }
    #sidebar {
        width: 25%;
        height: 100%;
        border-right: solid $primary;
        padding: 1;
        background: $surface;
    }
    #chat-selector {
        height: 100%;
        overflow-y: auto;
        scrollbar-gutter: stable;
        padding-bottom: 4;
        box-sizing: border-box;
    }
    #chat-selector > * {
        min-height: 0;
        padding-bottom: 1;
    }
    .chat-selector-container {
        height: 100%;
        min-height: 0;
    }
    #chat-selector > * {
        width: 100%;
        min-height: 0;
    }
    .chat-item {
        padding: 1;
    }
    .chat-item.selected {
        background: $accent;
        color: $text;
        padding: 1;
    }
    .chat-item.unread {
        border: round purple;
    }
    .chat-item > Static {
        padding: 1;
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
    .message-header {
        color: $text-muted;
        text-style: bold;
        padding-bottom: 1;
    }

    .message-spacer {
        height: 1;
    }

    .message-content {
        padding: 0 0 1 0;
    }

    /* Rich Markdown styling is handled via the Rich renderer's built-in styles */
    #input-area {
        layout: horizontal;
        height: auto;
        border-top: solid $primary;
        padding: 1;
        background: $surface;
        margin: 0;
        width: 100%;
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
        with Container(id="chat-row"):
            with Container(id="sidebar"):
                with Container(classes="sidebar-header"):
                    yield ChatNameInput(placeholder="Filter chats...", id="new-chat-name", classes="chat-name-input")
                    yield Button("+ Add", id="add-chat-button", variant="success", disabled=True)
                yield ScrollableContainer(id="chat-selector", classes="chat-selector-container")

            with Container(id="chat-container"):
                yield ScrollableContainer(id="chat-history")

        with Container(id="input-area"):
            yield MessageInput(id="message-input", language="markdown", show_line_numbers=False, tab_behavior="indent")
            yield Button("Submit", id="submit-button", variant="primary")
        yield Footer()

    def on_mount(self) -> None:
        """Setup app on startup."""
        self.query_one("#message-input").focus()
        history = self.query_one("#chat-history")
        history.scroll_end(animate=False)

        # Initialize chat selector with default chats
        self.chats = ["General", "Support", "Random", "Project A", "Project B"]
        self.load_chat_selector()

        # Set current chat after initializing chats
        self.current_chat = "General"

        # Start test thread for notification testing
        self._test_thread_running = True
        self.run_worker(self._test_notification_thread(), thread=True)

        # Initialize all chats with welcome messages
        for chat_name in self.chats:
            if chat_name not in self._chat_messages:
                self._chat_messages[chat_name] = []
                welcome_msg = f"### Welcome to {chat_name} Chat!\n\nThis is a persistent chat session."
                self._chat_messages[chat_name].append((welcome_msg, False))

        # Force load messages for current chat immediately
        history = self.query_one("#chat-history")
        history.remove_children()
        for content, is_user in self._chat_messages[self.current_chat]:
            message = ChatMessage(content, is_user)
            history.mount(message)

        history.refresh()
        history.scroll_end(animate=False)

    def on_unmount(self) -> None:
        """Cleanup on app exit."""
        # Cancel any running intervals
        for interval in self._chat_intervals.values():
            interval.stop()

        # Stop test thread
        self._test_thread_running = False

        # Skip UI updates if chat-history is already gone
        try:
            history = self.query_one("#chat-history")
            if history:
                history.remove_children()
                for content, is_user in self._chat_messages[self.current_chat]:
                    message = ChatMessage(content, is_user)
                    history.mount(message)

                history.refresh()
                history.scroll_end(animate=False)
        except Exception:
            pass  # UI elements already destroyed

    def load_chat_selector(self) -> None:
        """Populate the chat selector sidebar with filtered and ordered chats"""
        selector = self.query_one("#chat-selector")
        selector.remove_children()

        # Get filter text if any
        filter_text = self.query_one("#new-chat-name", Input).value.strip().lower()

        # Filter chats based on input
        filtered_chats = [name for name in self.chats if not filter_text or filter_text in name.lower()]

        # Order chats:
        # 1. Current chat first
        # 2. Unread chats next (most recent first)
        # 3. Other chats alphabetically
        ordered_chats = []
        other_chats = []

        for name in filtered_chats:
            if name == self.current_chat:
                ordered_chats.insert(0, name)
            elif name in self._unread_chats:
                ordered_chats.append(name)
            else:
                other_chats.append(name)

        # Sort unread chats by most recent message timestamp
        ordered_chats[1:] = sorted(ordered_chats[1:], key=lambda name: self._get_last_message_time(name), reverse=True)

        # Add remaining chats alphabetically
        ordered_chats.extend(sorted(other_chats))

        selector.mount(
            *[
                ChatItem(name, selected=(name == self.current_chat), unread=(name in self._unread_chats))
                for name in ordered_chats
            ]
        )
        selector.refresh()

    def _get_last_message_time(self, chat_name: str) -> datetime:
        """Get timestamp of last message in a chat"""
        if chat_name not in self._chat_messages or not self._chat_messages[chat_name]:
            return datetime.min
        # Return time of last message (content, is_user) tuple
        last_msg = self._chat_messages[chat_name][-1]
        # Extract timestamp from message content if possible
        for line in last_msg[0].split("\n"):
            if line.strip().startswith("###"):
                continue
            if "at " in line:
                time_str = line.split("at ")[-1].split()[0]
                try:
                    return datetime.strptime(time_str, "%H:%M:%S")
                except ValueError:
                    continue
        return datetime.now()  # Fallback to current time if no timestamp found

    def create_new_chat(self, name: str) -> None:
        """Shared method to create a new chat session"""
        if not name:
            self.notify("Chat name cannot be empty!", severity="error")
            return

        if name in self.chats:
            self.notify("Chat name already exists!", severity="error")
            return

        self.chats.append(name)
        self.current_chat = name

        # Initialize chat messages storage
        self._chat_messages[name] = []
        welcome_msg = f"### Welcome to {name} Chat!\n\nThis is a persistent chat session."
        self._chat_messages[name].append((welcome_msg, False))

        # Update UI components
        self.load_chat_selector()

        # Find and select the new chat item
        for item in self.query(".chat-item"):
            if item.name == name:
                # Deselect all other chats first
                for other_item in self.query(".chat-item"):
                    other_item.deselect()

                # Select the new chat
                item.select()
                item.post_message(ChatItem.Clicked(item))

                # Force immediate message load
                self.call_next(self.load_chat_messages)
                break

        # Update button state
        self.query_one("#add-chat-button", Button).disabled = True

    def add_new_chat(self) -> None:
        """Handle add chat button press"""
        name_input = self.query_one("#new-chat-name", Input)
        new_name = name_input.value.strip()
        self.create_new_chat(new_name)

        # Clear input and focus back to message input
        name_input.value = ""
        self.query_one("#message-input").focus()

    async def load_chat_messages(self) -> None:
        """Load messages for the current chat"""
        # Clear existing messages
        history = self.query_one("#chat-history")
        history.remove_children()

        # Cancel any existing periodic messages
        if hasattr(self, "_chat_intervals"):
            for interval in self._chat_intervals.values():
                interval.stop()
            self._chat_intervals.clear()

        # Ensure chat exists in storage
        if self.current_chat not in self._chat_messages:
            self._chat_messages[self.current_chat] = []
            welcome_msg = f"### Welcome to {self.current_chat} Chat!\n\nThis is a persistent chat session."
            self._chat_messages[self.current_chat].append((welcome_msg, False))

        # Mount messages synchronously first
        history = self.query_one("#chat-history")
        for content, is_user in self._chat_messages[self.current_chat]:
            message = ChatMessage(content, is_user)
            history.mount(message)

        # Force immediate UI update
        history.refresh()
        history.scroll_end(animate=False)

        # Then setup async components
        async with self._chat_lock:
            pass  # Reserved for future async operations

    def add_message(self, content: str, is_user: bool = False) -> None:
        """Add a message to the chat history."""
        history = self.query_one("#chat-history")
        message = ChatMessage(content, is_user)
        history.mount(message)

        # Store message in persistent storage
        if self.current_chat not in self._chat_messages:
            self._chat_messages[self.current_chat] = []
        self._chat_messages[self.current_chat].append((content, is_user))

        # Mark as unread if not current chat
        if not is_user and self.query_one("#chat-history").has_focus is False:
            self._unread_chats.add(self.current_chat)
            self.load_chat_selector()

        # Scroll to bottom after message is fully rendered
        def scroll_to_bottom():
            history.scroll_end(animate=True, duration=0.3)

        # Use a small delay to ensure message is rendered
        self.set_timer(0.1, scroll_to_bottom)

    async def generate_server_response(self, user_message: str) -> None:
        """Generate a server response to a user message"""
        # Simulate processing time
        await asyncio.sleep(1.0)

        # Create response
        response_content = (
            f"### Response to your message\n\n"
            f"You wrote: *{user_message[:50]}...*\n\n"
            f"Here's a random markdown sample:\n{generate_random_markdown()}"
        )

        self.add_message(response_content, is_user=False)

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

    async def _test_notification_thread(self) -> None:
        """Test thread that randomly selects chats and sends messages"""
        while self._test_thread_running:
            await asyncio.sleep(10)  # Wait 10 seconds between messages

            # Randomly select a chat (may or may not be current)
            random_chat = random.choice(self.chats)
            was_current = random_chat == self.current_chat

            # Generate test message
            timestamp = datetime.now().strftime("%H:%M:%S")
            message = (
                f"### Test Notification\n"
                f"Random message in {random_chat} at {timestamp}\n"
                f"This chat was {'current' if was_current else 'not current'} when sent"
            )

            # Add message to the random chat
            if random_chat not in self._chat_messages:
                self._chat_messages[random_chat] = []
            self._chat_messages[random_chat].append((message, False))

            # Update UI
            if was_current:
                # If current chat, add message directly to view
                self.call_from_thread(self.add_message, message, False)
            else:
                # If background chat, mark as unread
                self._unread_chats.add(random_chat)
                self.call_from_thread(self.load_chat_selector)

    @on(Input.Changed, "#new-chat-name")
    def on_name_changed(self, event: Input.Changed) -> None:
        """Handle chat name input changes - filter chats and update add button state"""
        button = self.query_one("#add-chat-button", Button)
        button.disabled = not event.value.strip()
        self.load_chat_selector()

    @on(Button.Pressed, "#add-chat-button")
    def handle_add_chat(self) -> None:
        """Handle add chat button press"""
        self.add_new_chat()

    @on(Button.Pressed, "#submit-button")
    def handle_button_submission(self) -> None:
        """Handle submit button press."""
        self.submit_message()

    def on_chat_item_clicked(self, event: ChatItem.Clicked) -> None:
        """Handle chat item selection"""
        # Deselect all items first
        for item in self.query(".chat-item"):
            item.deselect()

        # Select clicked item
        event.item.select()
        prev_chat = self.current_chat
        self.current_chat = event.item.name

        # Mark chat as read
        if self.current_chat in self._unread_chats:
            self._unread_chats.remove(self.current_chat)
            event.item.unread = False

        # Refresh chat selector to update ordering
        self.load_chat_selector()

        # Only load messages if chat changed
        if prev_chat != self.current_chat:
            # Cancel any existing interval for previous chat
            if prev_chat in self._chat_intervals:
                self._chat_intervals[prev_chat].stop()

            # Schedule message loading through the event loop
            self.call_next(self.load_chat_messages)

    def submit_message(self) -> None:
        """Process message submission."""
        input_widget = self.query_one("#message-input", MessageInput)
        if text := input_widget.text.strip():
            self.add_message(text, is_user=True)
            input_widget.text = ""
            input_widget.focus()

            # Generate server response
            self.call_after_refresh(self.generate_server_response, text)


if __name__ == "__main__":
    ChatApp().run()
