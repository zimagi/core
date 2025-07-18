import threading
from datetime import datetime

from django.conf import settings
from textual import on
from textual.app import App
from textual.containers import Container, ScrollableContainer
from textual.widgets import Button, Footer, Input, Static

from zimagi.parallel import Parallel

from .data import ChatMessage
from .widgets import ChatItemDisplay, ChatMessageDisplay, ChatNameInput, MessageInput


class ChatApp(App):

    lock = threading.Lock()

    def __init__(self, command, chat_name=None, **kwargs):
        self.command = command
        self.command_client = command.command_client
        self.data_client = command.data_client

        self.initial_chat_name = chat_name
        self.start_time = datetime.now().strftime("%Y-%m-%d+%H:%M:%S")

        self._chat_messages = {}
        self._unread_chats = set()

        super().__init__(**kwargs)

    def compose(self):
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

    def on_mount(self):
        self.query_one("#message-input").focus()
        history = self.query_one("#chat-history")
        history.scroll_end(animate=False)

        self.chats = self.data_client.values("chat", "name", user__name=settings.API_USER).results
        self.current_chat = (
            self.initial_chat_name if self.initial_chat_name and self.initial_chat_name in self.chats else self.chats[0]
        )
        self._listener_running = True

        self.load_chat_selector()
        self.run_worker(self._listener_thread(), thread=True)

        for chat_name in self.chats:
            self.add_message(chat_name, self.get_welcome_message(chat_name), sender="system", is_user=False)

        history = self.query_one("#chat-history")
        history.remove_children()
        for message in self._chat_messages[self.current_chat]:
            history.mount(ChatMessageDisplay(message))

        history.refresh()
        history.scroll_end(animate=False)

    def on_unmount(self):
        self._listener_running = False

        try:
            history = self.query_one("#chat-history")
            if history:
                history.remove_children()
        except Exception:
            pass

    def get_welcome_message(self, chat_name):
        return f"### Welcome to the {chat_name} chat!\n\nThis is a persistent chat session."

    def get_separator(self):
        return Static("─── New Messages ───", classes="unread-separator")

    def load_chat_selector(self):
        selector = self.query_one("#chat-selector")
        selector.remove_children()

        filter_text = self.query_one("#new-chat-name", Input).value.strip().lower()
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

        ordered_chats[1:] = sorted(ordered_chats[1:], key=lambda name: self._get_last_message_time(name), reverse=True)
        ordered_chats.extend(sorted(other_chats))

        selector.mount(
            *[
                ChatItemDisplay(name, selected=(name == self.current_chat), unread=(name in self._unread_chats))
                for name in ordered_chats
            ]
        )
        selector.refresh()

    def _get_last_message_time(self, chat_name):
        if chat_name not in self._chat_messages or not self._chat_messages[chat_name]:
            return datetime.min
        return self._chat_messages[chat_name][-1].time

    def create_new_chat(self, name):
        if not name:
            self.notify("Chat name cannot be empty!", severity="error")
            return

        if name in self.chats:
            self.notify("Chat name already exists!", severity="error")
            return

        chat = self.data_client.create("chat", user=settings.API_USER, name=name)
        self.chats.append(chat.name)
        self.current_chat = chat.name

        self._chat_messages[chat.name] = [
            self.add_message(chat.name, self.get_welcome_message(chat.name), sender="system", is_user=False)
        ]
        self.load_chat_selector()

        for item in self.query(".chat-item"):
            if item.name == chat.name:
                for other_item in self.query(".chat-item"):
                    other_item.deselect()

                item.select()
                item.post_message(ChatItemDisplay.Clicked(item))

                self.call_next(self.load_chat_messages)
                break

        self.query_one("#add-chat-button", Button).disabled = True

    def add_new_chat(self):
        name_input = self.query_one("#new-chat-name", Input)
        new_name = name_input.value.strip()
        self.create_new_chat(new_name)

        name_input.value = ""
        self.query_one("#message-input").focus()

    async def load_chat_messages(self):
        with self.lock:
            history = self.query_one("#chat-history")
            history.remove_children()

            chat_messages = self._chat_messages.get(self.current_chat, [])
            for index, message in enumerate(chat_messages):
                history.mount(ChatMessageDisplay(message))

            history.scroll_end(animate=False)
            history.refresh()

    @on(Input.Changed, "#new-chat-name")
    def on_name_changed(self, event: Input.Changed):
        button = self.query_one("#add-chat-button", Button)
        button.disabled = not event.value.strip()
        self.load_chat_selector()

    @on(Button.Pressed, "#add-chat-button")
    def handle_add_chat(self):
        self.add_new_chat()

    @on(Button.Pressed, "#submit-button")
    def handle_button_submission(self):
        self.submit_message()

    @on(ChatItemDisplay.Clicked)
    def on_chat_item_clicked(self, event):
        prev_chat = self.current_chat
        new_chat = event.item.name

        if prev_chat in self._chat_messages:
            history = self.query_one("#chat-history")
            for separator in history.query(".unread-separator"):
                separator.remove()

        self.current_chat = new_chat
        event.item.select()

        if new_chat in self._unread_chats:
            self._unread_chats.remove(new_chat)
            event.item.unread = False
        self.load_chat_selector()

        self.call_next(self.load_chat_messages)

    def get_message(self, content, time=None, sender=None, is_user=False):
        return ChatMessage(content=content, time=time, sender=sender, is_user=is_user)

    def add_message(self, chat_name, content, time=None, sender=None, is_user=False):
        message = self.get_message(content=content, time=time, sender=sender, is_user=is_user)

        if chat_name not in self._chat_messages:
            self._chat_messages[chat_name] = []
        self._chat_messages[chat_name].append(message)

        return message

    def render_message(self, chat_name, content, time=None, sender=None, is_user=False):
        message = self.add_message(chat_name, content=content, time=time, sender=sender, is_user=is_user)

        history = self.query_one("#chat-history")
        if message.is_user or chat_name == self.current_chat:
            history.mount(ChatMessageDisplay(message))

            if message.is_user:
                history.scroll_end(animate=False)
        else:
            self._unread_chats.add(chat_name)
            self.load_chat_selector()

    def submit_message(self):
        input_widget = self.query_one("#message-input", MessageInput)
        if text := input_widget.text.strip():
            self.command_client.execute("chat send", chat_name=self.current_chat, chat_message=text)
            input_widget.text = ""
            input_widget.focus()

    async def _listener_thread(self):
        while self._listener_running:

            def process_message(message):
                with self.lock:
                    if message.name and message.name == "message":
                        self.call_from_thread(
                            self.render_message,
                            message.data["name"],
                            message.data["message"],
                            time=None,
                            sender=message.data["user"],
                            is_user=(True if message.data["user"] == settings.API_USER else False),
                        )

            def listen_to_chat(chat_name):
                command_client = self.command_client.clone(process_message)
                command_client.execute(
                    "chat listen",
                    chat_name=chat_name,
                    listen_timeout=60,
                )

            Parallel.list(self.chats, listen_to_chat, thread_count=len(self.chats))
