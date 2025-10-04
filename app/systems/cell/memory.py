from utility.data import dump_json
from utility.runtime import debug


class DialogResult:
    def __init__(self, score, scores, messages=None):
        self.score = score
        self.scores = scores
        self.messages = messages or []

    def __str__(self):
        return (
            f"Score: {self.score}\n"
            f"Scores: {", ".join([str(score) for score in self.scores])}\n"
            f"Messages: {", ".join(self.messages)}"
        )

    def __repr__(self):
        return self.__str__()


class Experience:

    def __init__(self, command, language_model, memory, search_results, keep_previous=5):
        self.command = command
        self.language_model = language_model
        self.memory = memory
        self.search_results = search_results

        self.dialogs = {}
        self.messages = {}
        self.tokens = {}

        debug("Initializing experience")
        self._load(keep_previous)

    def _load(self, keep_previous):
        message_ids = []

        debug("Loading experience")

        for dialog_id in (
            self.command._memory_dialog.set_order("-created").set_limit(keep_previous).field_values("id", memory=self.memory)
        ):
            debug(dialog_id, "Adding dialog")
            self.dialogs[dialog_id] = DialogResult(score=1, scores=[1])

        debug(self.dialogs, "Recent dialogs")

        for sentence_results in self.search_results:
            for scored_point in sentence_results:
                dialog_id = scored_point.payload["dialog_id"]
                score = scored_point.score

                debug(dialog_id, f"Adding dialog [ {score} ]")

                if dialog_id not in self.dialogs:
                    self.dialogs[dialog_id] = DialogResult(score=score, scores=[score])
                else:
                    self.dialogs[dialog_id].scores.append(score)
                    self.dialogs[dialog_id].score = max(self.dialogs[dialog_id].score, score)

        debug(self.dialogs, "Matching dialogs")

        for dialog_id, dialog_result in self.dialogs.items():
            self.dialogs[dialog_id].messages = self.command._memory_message.field_values("id", dialog_id=dialog_id)
            message_ids.extend(self.dialogs[dialog_id].messages)

        debug(self.dialogs, "Full dialogs with messages")
        debug(message_ids, "Context message IDs")

        for instance in self.command._memory_message.filter(id__in=message_ids):
            self.messages[instance.id] = instance
            self.tokens[instance.id] = self.language_model.get_token_count(
                {"role": instance.role, "content": instance.content}
            )
        debug(self.dialogs, "Final dialogs")


class MemoryManager:

    def __init__(self, command, user, search_limit=None, search_min_score=None, keep_previous=5):
        self.command = command
        self.user = self._get_user(user)

        self.language_model = self.user.get_language_model(self.command)
        self.search_limit = self.user.get_search_limit(search_limit)
        self.search_min_score = self.user.get_search_min_score(search_min_score)
        self.keep_previous = keep_previous

        if not self.language_model:
            self.error(f"User {self.user.name} language model configurations required to use memory manager")

        self.embedding_db = self.user.get_qdrant_collection(self.command, "memory")
        self.reset()

    def _get_user(self, user):
        if isinstance(user, str):
            return self.command._user.retrieve(user)
        return user

    def _get_sequence(self, user, name):
        memory = self.command._memory.retrieve(None, user=user, name=name)
        if not memory:
            memory, created = self.command._memory.store(None, {"user": user, "name": name})

        debug("Getting memory sequence")
        debug(memory, "Memory sequence")
        return memory

    def set_sequence(self, name):
        debug("Setting memory sequence")
        debug(self.user, "Memory user")
        debug(name, "Memory sequence name")

        self.memory = self._get_sequence(self.user, name)
        return self

    def reset(self):
        self.experience = None
        self.system_messages = []
        self.new_messages = []
        self.tools = ""

    def set_tools(self, tool_prompt):
        self.tools = tool_prompt

        debug("Setting memory tool prompt")
        debug(self.tools, "Tool prompt")

    def add_system(self, *messages):
        debug("Adding system messages")

        def _add_list(message_list):
            for message in message_list:
                if isinstance(message, (list, tuple)):
                    _add_list(message)
                else:
                    debug(message, "Adding system message")
                    self.system_messages.append(message)

        _add_list(messages)
        return self

    def add(self, *messages):
        debug("Adding messages")

        def _add_list(message_list):
            for message in message_list:
                if isinstance(message, (list, tuple)):
                    _add_list(message)
                else:
                    if "sender" not in message:
                        message["sender"] = self.user.name
                    debug(message, "Adding message")
                    self.new_messages.append(message)

        _add_list(messages)
        return self

    def load(self):
        available_tokens = self.language_model.get_max_tokens()
        messages = []

        debug("Loading memory")
        debug(available_tokens, "Available tokens")

        if self.system_messages:
            if self.tools:
                self.system_messages[0]["content"] = "\n\n".join([self.system_messages[0]["content"], self.tools])

            available_tokens -= self.language_model.get_token_count(self.system_messages)

            debug(self.system_messages, "System messages")
            debug(available_tokens, "Available tokens")
            messages.extend(self.system_messages)

        if self.new_messages:
            new_tokens = self.language_model.get_token_count(self.new_messages)

            debug(self.new_messages, "New messages")
            debug(new_tokens, "New tokens")

            if self.experience:
                available_tokens = available_tokens - new_tokens
                experience = self._trim_experience(self.experience, available_tokens)

                debug(experience, "Experience")
                debug(available_tokens, "Available tokens")
                messages.extend(experience)

            messages.extend(self.new_messages)

        elif self.experience:
            experience = self._trim_experience(self.experience, available_tokens)

            debug(experience, "Experience")
            debug(available_tokens, "Available tokens")
            messages.extend(experience)

        return messages

    def search(self, text):
        debug("Searching experience")
        debug(text, "Search text")
        debug(self.search_limit, "Search limit")
        debug(self.search_min_score, "Search minimum score")
        debug(self.memory.id, "Search memory ID (memory_id)")

        search_results = self.command.search_embeddings(
            self.user,
            self.embedding_db,
            text,
            fields=["dialog_id", "message_id"],
            limit=self.search_limit,
            min_score=self.search_min_score,
            filter_field="memory_id",
            filter_ids=self.memory.id,
        )

        debug(search_results, "Search results")
        debug(self.keep_previous, "Keep previous")

        self.experience = Experience(self.command, self.language_model, self.memory, search_results, self.keep_previous)

    def _trim_experience(self, experience, available_tokens):
        selected_messages = []
        selected_tokens = 0
        sorted_dialogs = sorted(experience.dialogs.items(), key=lambda x: x[1].score, reverse=True)

        debug("Trimming experience")
        debug(sorted_dialogs, "Sorted dialogs")

        for dialog_id, dialog_data in sorted_dialogs:
            dialog_messages = sorted(dialog_data.messages, key=lambda message_id: experience.messages[message_id].created)
            dialog_tokens = sum(experience.tokens[message_id] for message_id in dialog_messages)
            total_tokens = selected_tokens + dialog_tokens

            debug(dialog_messages, "Dialog messages")
            debug(dialog_tokens, "Dialog tokens")
            debug(available_tokens, "Available tokens")
            debug(selected_tokens, "Selected tokens")
            debug(dialog_tokens, "Dialog tokens")
            debug(total_tokens, "Total tokens")

            if total_tokens <= available_tokens:
                selected_messages.extend(dialog_messages)
                selected_tokens += dialog_tokens

                debug(selected_messages, "Selected messages")
                debug(selected_tokens, "Selected tokens")
            else:
                debug("Token limit reached")
                break
        return [
            {"role": experience.messages[message_id].role, "content": experience.messages[message_id].content}
            for message_id in sorted(selected_messages, key=lambda message_id: experience.messages[message_id].created)
        ]

    def save(self):
        def _save_callback():
            debug("Saving memory messages")

            memory_dialog = self.command._memory_dialog.set_order("-created").set_limit(1).filter(memory=self.memory)
            last_message = None

            if memory_dialog:
                memory_dialog = memory_dialog[0]
                last_message = self.command._memory_message.set_order("-created").set_limit(1).filter(dialog=memory_dialog)
                if last_message:
                    last_message = last_message[0]

            debug(memory_dialog, "Memory dialog")

            for memory in self.new_messages:
                debug(memory, "Saving memory")
                debug(last_message, "Last dialog message")

                if not memory_dialog or memory["role"] == "user":
                    if not last_message or last_message.role == "assistant":
                        memory_dialog = self.command.save_instance(
                            self.command._memory_dialog,
                            None,
                            fields={"memory": self.memory},
                        )

                memory_message = self.command.save_instance(
                    self.command._memory_message,
                    None,
                    fields={**memory, "memory": self.memory, "dialog": memory_dialog},
                )
                embedding_payload = {
                    "memory_id": self.memory.id,
                    "user_id": memory_message.sender,
                    "dialog_id": memory_dialog.id,
                    "message_id": memory_message.id,
                    "role": memory_message.role,
                }

                debug(memory_dialog, "Memory dialog")
                debug(memory_message, "Memory message")
                debug(embedding_payload, "Memory embedding payload")

                debug("Saving message embeddings")
                self.command.save_embeddings(
                    self.user,
                    self.embedding_db,
                    "memory_message",
                    memory_message.id,
                    "content",
                    payload=embedding_payload,
                )
                last_message = memory_message

        if self.new_messages:
            self.command.run_exclusive(f"save-memories-{self.memory.id}", _save_callback)
            self.new_messages = []

        return self
