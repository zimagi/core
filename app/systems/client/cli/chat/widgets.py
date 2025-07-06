import pyperclip

from textual.widgets import TextArea, Static, Input
from textual.message import Message
from rich import box
from rich.style import Style
from rich.panel import Panel
from rich.console import Group
from rich.text import Text
from rich.markdown import Markdown as RichMarkdown
from datetime import datetime


class MessageInput(TextArea):
    BINDINGS = [
        ("ctrl+s", "submit", "Submit"),
        ("ctrl+c", "copy", "Copy"),
        ("ctrl+v", "paste", "Paste"),
    ]

    async def on_mount(self):
        self.app.set_focus(self)

    def action_submit(self):
        self.app.submit_message()

    def action_copy(self):
        selected_text = self.selected_text
        if selected_text:
            pyperclip.copy(selected_text)

    def action_paste(self):
        text = pyperclip.paste()
        if text:
            self.insert(text)

    def _create_right_click_menu(self):
        from textual.widgets import MenuItem

        menu = super()._create_right_click_menu()
        menu.items.insert(0, MenuItem("Submit", "action_submit", "Ctrl+S"))
        menu.items.insert(1, MenuItem("Copy", "action_copy", "Ctrl+C"))
        menu.items.insert(2, MenuItem("Paste", "action_paste", "Ctrl+V"))
        return menu


class ChatNameInput(Input):
    BINDINGS = [
        ("enter", "select_or_create_chat", "Select/Create Chat"),
    ]

    def action_select_or_create_chat(self):
        app = self.app
        name = self.value.strip()
        if not name:
            return

        if name in app.chats:
            for item in app.query(".chat-item"):
                if item.name == name:
                    item.post_message(ChatItemDisplay.Clicked(item))
                    break
        else:
            app.create_new_chat(name)

        self.value = ""
        app.query_one("#message-input").focus()

    def _create_right_click_menu(self):
        from textual.widgets import MenuItem

        menu = super()._create_right_click_menu()
        menu.items.insert(0, MenuItem("Select / Create", "action_select_or_create_chat", "Enter"))
        return menu


class ChatItemDisplay(Static):
    def __init__(self, name, selected=False, unread=False):
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
    def unread(self):
        return self._unread

    @unread.setter
    def unread(self, value):
        self._unread = value
        if value:
            self.add_class("unread")
        else:
            self.remove_class("unread")

    class Clicked(Message):
        def __init__(self, item):
            self.item = item
            super().__init__()

    @property
    def name(self):
        return self._name

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value
        if value:
            self.add_class("selected")
        else:
            self.remove_class("selected")

    def compose(self):
        yield Static(self._name)

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def on_click(self):
        self.post_message(self.Clicked(self))


class ChatMessageDisplay(Static):

    def __init__(self, message):
        super().__init__()
        self.message = message

    def compose(self):
        timestamp = self.message.time.now
        sender = "You" if self.message.is_user else self.message.sender

        bg_color = "rgb(30,30,30)"  # Dark background
        text_color = "rgb(224,224,224)"  # Light text
        header_color = "bright_black"
        border_color = "bright_blue" if self.message.is_user else "bright_green"

        markdown = RichMarkdown(
            self.message.content, style=Style(color=text_color), code_theme="monokai", hyperlinks=False, justify="left"
        )

        header_text = Text.from_markup(f"[b]{timestamp} {sender}[/b]", justify="left", style=Style(color=header_color))
        content = Group(header_text, "", markdown)

        border_style = Style(color=border_color)
        yield Static(
            Panel(
                content,
                border_style=border_style,
                box=box.ROUNDED,
                padding=1,
                style=Style(bgcolor=bg_color, color=text_color),
                subtitle_align="left",
                title_align="left",
            ),
            classes="user-message" if self.message.is_user else "bot-message",
        )
