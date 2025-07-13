import re
import copy
import logging

from django.conf import settings
from systems.commands.index import BaseCommand
from utility.data import Collection, normalize_value, load_json, flatten_dict
from utility.validation import validate_flattened_dict
from utility.display import format_traceback, format_exception_info


logger = logging.getLogger(__name__)


class CellError(Exception):
    pass


class Cell(BaseCommand("cell")):

    def _initialize_cell(self):
        self.manager.load_templates()

        if self.agent_user:
            self._user.set_active_user(self.get_instance(self._user, self.agent_user, required=True))

        self.channels = self.get_channels()
        self._set_sensor(self.agent_sensor)
        logger.debug(f"Set sensor to: {self.sensor_name}")

        self.state_key = self.get_state_key()
        self.sensor_key = self.get_sensor_key()
        logger.info(f"State key: {self.state_key}")
        logger.info(f"Sensor key: {self.sensor_key}")

        self.text_splitter = self.get_provider("text_splitter", self.agent_message_splitter_provider)
        self.encoder = self.get_provider(
            "encoder", self.agent_embedding_model_provider, **self.agent_embedding_model_options
        )
        self.chat_embeddings = self.qdrant("chat")
        self.actor = self.get_provider(
            "language_model", self.agent_primary_model_provider, **self.agent_primary_model_options
        )
        self.initialize_cell()

    def initialize_cell(self):
        # Override in subclass if needed
        pass

    def get_state_key(self):
        return f"cell:state:{self.agent_user}:{".".join(self.get_full_name().split(" ")[1:])}"

    def get_sensor_key(self):
        return self.agent_user

    def exec(self):
        self._initialize_cell()
        try:
            state = self.get_state(
                self.state_key,
                {"goal": self.agent_goal, "rules": self.agent_rules, "tools": self.agent_tools},
            )
            logger.debug(f"Loaded agent state: {state}")

            logger.debug(f"Starting to listen for {self.sensor_name} with key: {self.sensor_key}")
            for package in self.listen(self.sensor_name, state_key=self.sensor_key):
                logger.info(f"Message sender: {package.sender}")
                logger.debug(f"Message received: {package.message}")

                message = self._load_message(package)
                if message:
                    logger.info(f"Message loaded: {message}")
                    try:
                        self.data("Received message from", package.sender)
                        response = self.profile(self.process_sensory_message, message, state)

                    except Exception as error:
                        logger.debug(f"Got an error performing action: {error}")
                        # self.handle_error(error, package)
                        raise error

                    channel = package.sender if self.agent_channel == "sender" else self.agent_channel
                    message = self._translate_message(
                        {
                            "self": self.service_id,
                            "user": self.agent_user if self.agent_user else settings.ADMIN_USER,
                            "sensor": self.sensor_name,
                            "sender": package.sender,
                            "message": message,
                            "response": response.result,
                            "time": response.time,
                            "memory": response.memory,
                        }
                    )
                    logger.info(f"Sending data to channel {channel}: {message}")
                    self.send(channel, message)

        except Exception as error:
            logger.info(f"Sending error data to channel error:{self.agent_channel}: {error}")
            self.send(
                f"error:{self.agent_channel}",
                {
                    "self": self.service_id,
                    "user": self.agent_user if self.agent_user else settings.ADMIN_USER,
                    "sensor": self.sensor_name,
                    "sender": package.sender,
                    "message": package.message,
                    "error": str(error),
                    "traceback": "\n".join([item.strip() for item in format_traceback()]),
                    "info": "\n".join([item.strip() for item in format_exception_info()]),
                },
            )
        finally:
            self.set_state(self.state_key, self.refine_state(state))
            logger.debug("Cell cycle complete")
            self.sleep(60)

    def process_sensory_message(self, message, state):
        prompts = self._render_prompts(
            {
                **state,
                "message": message,
                "field_labels": self.agent_message_field_labels,
                "tools": self.mcp.list_tools(state["tools"]) if state["tools"] else [],
            }
        )
        system_message = {"role": "system", "message": prompts["system"]}
        request_prompt = "\n\n".join([prompts["request"], prompts["tools"]])
        request_message = {"role": "user", "message": request_prompt}
        request_tokens = self.self.actor.get_token_count([system_message, request_message])
        memory_sequence = [
            system_message,
            *self.load_memories(message, request_tokens),
            request_message,
        ]

        logger.info(f"Cell using model: {self.actor}")
        logger.info(f"Cell system prompt:\n{prompts["system"]}")
        logger.info(f"Cell request prompt:\n{request_prompt}")
        logger.info(f"Cell core token count: {request_tokens}")

        import json

        print(json.dumps(memory_sequence, indent=2))

        # for exec_try in range(5):
        # response = self.actor.exec(memory_sequence)
        # print(json.dumps(response, indent=2))
        self.sleep(60)

        #     tool_call = re.search(r"```json([^`])```", response.text)
        #     if tool_call:
        #         tool_data = load_json(tool_call.group(1).strip())
        #         if self.validate_exec(tool_data):
        #             result = self.mcp.exec_tool(tool_data["tool"], tool_data["parameters"])
        #             self.save_memories(
        #                 message,
        #                 {"role": "assistant", "message": response.text},
        #                 {"role": "assistant", "message": result},
        #             )
        #     else:
        #         self.save_memories(
        #             message, {"role": "user", "message": prompts["request"]}, {"role": "assistant", "message": response.text}
        #         )
        #         return {"message": response.text}

        # raise CellError("Maximum amount of retries")

    def refine_state(self, state):
        return state

    def _set_sensor(self, channel):
        self.sensor_name = channel
        self.sensor_spec = self.manager.get_channel_spec(self.sensor_name)
        if not self.sensor_spec:
            self.error(f"Channel name {self.sensor_name} is not a valid sensory channel")

        self._sensor_tokens = self.get_channel_tokens(self.sensor_name)

    def _load_message(self, package):
        message_filters = self.manager.index.get_plugin_providers("message_filter")
        message = package.message
        query_filters = {}
        plugin_filters = {}

        for filter_name, filter_value in self.agent_sensor_filters.items():
            if filter_name in message_filters:
                plugin_filters[filter_name] = filter_value
            else:
                query_filters[filter_name] = filter_value

        if self._sensor_tokens:
            for token, token_value in self._sensor_tokens.items():
                token_parser = self.get_provider(
                    "channel_token",
                    token,
                    value=token_value,
                    fields=self.agent_message_fields,
                    filters=query_filters,
                    id_field=self.agent_sensor_id_field,
                )
                message = token_parser.load(message)

        elif isinstance(message, dict):
            message = validate_flattened_dict(
                flatten_dict(normalize_value(message), self.agent_message_fields),
                query_filters,
            )
        else:
            if self.agent_message_fields and "message" not in self.agent_message_fields:
                self.error("Message field message of scalar channel value it not specified")

            message = validate_flattened_dict({"message": normalize_value(message)}, query_filters)

        for filter_name, provider in plugin_filters.items():
            message_filter = self.get_provider("message_filter", filter_name)
            message = message_filter.filter(message, filter_value)
            if not message:
                break

        return message

    def _translate_message(self, message):
        flattened_message = flatten_dict(normalize_value(message))
        translation = {}

        if self.agent_channel_field_map:
            for field, flattened_field in self.agent_channel_field_map.items():
                translation[field] = flattened_message[flattened_field]
        else:
            translation = message

        return translation

    def _render_prompts(self, state):
        prompts = copy.deepcopy(self.get_prompts())
        for name, prompt_file in prompts.items():
            template = self.manager.template_engine.get_template(prompt_file)
            prompts[name] = template.render(**state)
        return prompts

    def get_prompts(self):
        prompt_base = "cell/prompt"
        return {
            "system": f"{prompt_base}/{self.agent_system_template}.md",
            "tools": f"{prompt_base}/{self.agent_tools_template}.md",
            "request": f"{prompt_base}/{self.agent_template}.md",
        }

    def _get_chat(self):
        if not getattr(self, "_chat_index", None):
            self._chat_index = {}

        if self.agent_chat_key not in self._chat_index:
            self._chat_index[self.agent_chat_key] = self._chat.retrieve(
                None, user=self.active_user, name=self.agent_chat_key
            )
        return self._chat_index[self.agent_chat_key]

    def load_memories(self, message, request_tokens):
        chat = self._get_chat()
        experience = self.search_experience(chat, message[field_name], limit=1000, min_score=0.3)
        return self.format_messages(experience, self.actor.get_max_tokens() - request_tokens)

    def search_experience(self, chat, content, limit=1000, min_score=0.3):
        dialogs = {}
        messages = {}
        tokens = {}
        message_ids = []

        sections = self.text_splitter.split(content)
        results = self.search_embeddings(
            "chat",
            self.encoder.encode(sections),
            fields=["dialog_id", "message_id"],
            limit=limit,
            min_score=min_score,
            filter_field="chat_id",
            filter_ids=chat.id,
        )
        for result in results:
            dialog_id = result.payload["dialog_id"]
            message_id = result.payload["message_id"]
            score = result.score

            if dialog_id not in dialogs:
                dialogs[dialog_id] = Collection(score=score, scores=[score], messages=[message_id])
            else:
                dialogs[dialog_id].messages.append(message_id)
                dialogs[dialog_id].scores.append(score)
                dialogs[dialog_id].score = max(dialogs[dialog_id].score, score)

            message_ids.append(message_id)

        for instance in self._chat_message.filter(id__in=message_ids):
            messages[instance.id] = instance
            tokens[instance.id] = self.actor.get_token_count([{"role": instance.role, "content": instance.content}])

        return Collection(dialogs=dialogs, messages=messages, tokens=tokens)

    def format_messages(self, experience, available_tokens):
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

    def save_memories(self, *memories):
        chat = self._get_chat()

        def _save_callback():
            chat_dialog = self._chat_dialog.set_order("-created").set_limit(1).filter(chat=chat)

            for memory in memories:
                if not chat_dialog or memory["role"] == "user" and chat_dialog.role == "assistant":
                    chat_dialog = self.save_instance(
                        self._chat_dialog, None, fields={"chat": chat, "previous": chat_dialog if chat_dialog else None}
                    )

                chat_message = self.save_instance(
                    self._chat_message,
                    None,
                    fields={**memory, "chat": chat, "dialog": chat_dialog},
                )
                sections = self.text_splitter.split(chat_message.content)
                embeddings = self.encoder.encode(sections)

                for index, text in enumerate(sections):
                    self.chat_embeddings.store(
                        chat_id=chat.id,
                        user_id=chat.user.id,
                        dialog_id=chat_dialog.id,
                        message_id=chat_message.id,
                        text=text,
                        embedding=embeddings[index],
                        role=chat_message.role,
                        order=index,
                    )

        self.run_exclusive(f"cell-save-messages-{chat.id}", _save_callback)

    def validate_tool(self, exec_data):
        if not exec_data or "tool" not in exec_data or not exec_data["tool"]:
            return False

        fields = self.mcp.get_tool_fields(exec_data["tool"])

        if fields.index and ("parameters" not in exec_data or not exec_data["parameters"]):
            return False

        for required_field in fields.required:
            if required_field not in exec_data["parameters"]:
                return False
        for input_field in exec_data["parameters"].keys():
            if input_field not in fields.index:
                return False

        return True

    def handle_error(self, error, package):
        # Repeat if failure so we don't lose the message
        self.send(self.sensor_name, package.message, package.sender)
