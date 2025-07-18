import logging

logger = logging.getLogger(__name__)


class DialogResult:
    def __init__(self, score, scores, messages):
        self.score = score
        self.scores = scores
        self.messages = messages


class Experience:

    def __init__(self, command, language_model, search_results):
        self.command = command
        self.language_model = language_model
        self.search_results = search_results

        self.dialogs = {}
        self.messages = {}
        self.tokens = {}

        self.load()

    def load(self):
        message_ids = []

        for result in self.search_results:
            dialog_id = result.payload["dialog_id"]
            message_id = result.payload["message_id"]
            score = result.score

            if dialog_id not in self.dialogs:
                self.dialogs[dialog_id] = DialogResult(score=score, scores=[score], messages=[message_id])
            else:
                self.dialogs[dialog_id].messages.append(message_id)
                self.dialogs[dialog_id].scores.append(score)
                self.dialogs[dialog_id].score = max(self.dialogs[dialog_id].score, score)

            message_ids.append(message_id)

        for instance in self.command._chat_message.filter(id__in=message_ids):
            self.messages[instance.id] = instance
            self.tokens[instance.id] = self.language_model.get_token_count(
                {"role": instance.role, "content": instance.content}
            )


class MemoryManager:

    def __init__(
        self,
        command,
        user,
        search_limit=None,
        search_min_score=None,
    ):
        self.command = command
        self.user = self._get_user(user)

        self.language_model = self.user.get_language_model(self.command)
        self.text_splitter = self.user.get_text_splitter(self.command)
        self.encoder = self.user.get_encoder(self.command)
        self.search_limit = self.user.get_search_limit(search_limit)
        self.search_min_score = self.user.get_search_min_score(search_min_score)

        if not self.language_model or not self.text_splitter or not self.encoder:
            self.error(
                f"User {self.user.name} language model, text splitter, and encoder provider "
                "configurations required to use memory manager"
            )

        self.memory_collection = "chat"
        self.chat_embeddings = self.command.qdrant(self.memory_collection)

        self.new_messages = []

    def _get_user(self, user):
        if isinstance(user, str):
            return self._user.retrieve(user)
        return user

    def _get_chat(self, user, chat_key):
        return self.command._chat.retrieve(None, user=user, name=chat_key)

    def set_chat(self, chat_key):
        self.chat = self._get_chat(self.user, chat_key)
        return self

    def add(self, *messages):

        def _add_list(message_list):
            for message in message_list:
                if isinstance(message, (list, tuple)):
                    _add_list(message)
                else:
                    if "sender" not in message:
                        message["sender"] = self.user.name
                    self.new_messages.append(message)

        _add_list(messages)
        return self

    def load(self, text, available_tokens, search_limit=None, min_score=None):
        experience = self._search_experience(text, search_limit, min_score)
        if self.new_messages:
            new_tokens = self.language_model.get_token_count(self.new_messages)
            return self._trim_experience(experience, (available_tokens - new_tokens)) + self.new_messages
        return self._trim_experience(experience, available_tokens)

    def _search_experience(self, text, search_limit, min_score):
        sections = self.text_splitter.split(text)
        search_results = self.command.search_embeddings(
            self.memory_collection,
            self.encoder.encode(sections),
            fields=["dialog_id", "message_id"],
            limit=search_limit or self.search_limit,
            min_score=min_score or self.search_min_score,
            filter_field="chat_id",
            filter_ids=self.chat.id,
        )
        return Experience(self.language_model, search_results)

    def _trim_experience(self, experience, available_tokens):
        selected_messages = []
        selected_tokens = 0
        sorted_dialogs = sorted(experience.dialogs.items(), key=lambda x: x[1].score, reverse=True)

        for dialog_id, dialog_data in sorted_dialogs:
            dialog_messages = sorted(dialog_data.messages, key=lambda message_id: experience.messages[message_id].created)
            dialog_tokens = sum(experience.tokens[message_id] for message_id in dialog_messages)

            if selected_tokens + dialog_tokens <= available_tokens:
                selected_messages.extend(dialog_messages)
                selected_tokens += dialog_tokens
            else:
                break
        return [
            {"role": experience.messages[message_id].role, "content": experience.messages[message_id].content}
            for message_id in sorted(selected_messages, key=lambda message_id: experience.messages[message_id].created)
        ]

    def save(self):
        def _save_callback():
            chat_dialog = self.command._chat_dialog.set_order("-created").set_limit(1).filter(chat=self.chat)
            last_message = None

            if chat_dialog:
                chat_dialog = chat_dialog[0]
                last_message = self.command._chat_message.set_order("-created").set_limit(1).filter(dialog=chat_dialog)
                if last_message:
                    last_message = last_message[0]

            for memory in self.new_messages:
                if not chat_dialog or memory["role"] == "user":
                    if not last_message or last_message.role == "assistant":
                        chat_dialog = self.command.save_instance(
                            self.command._chat_dialog,
                            None,
                            fields={"chat": self.chat, "previous": chat_dialog if chat_dialog else None},
                        )

                chat_message = self.command.save_instance(
                    self.command._chat_message,
                    None,
                    fields={**memory, "chat": self.chat, "dialog": chat_dialog},
                )
                sections = self.text_splitter.split(chat_message.content)
                embeddings = self.encoder.encode(sections)

                for index, text in enumerate(sections):
                    self.chat_embeddings.store(
                        chat_id=self.chat.id,
                        user_id=self.chat.user.id,
                        dialog_id=chat_dialog.id,
                        message_id=chat_message.id,
                        text=text,
                        embedding=embeddings[index],
                        role=chat_message.role,
                        order=index,
                    )

                last_message = chat_message

        if self.new_messages:
            self.command.run_exclusive(f"save-memories-{self.chat.id}", _save_callback)
            self.new_messages = []

        return self
