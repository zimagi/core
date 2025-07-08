import re
import copy
import logging

from systems.commands.index import BaseCommand
from utility.data import normalize_value, load_json, flatten_dict
from utility.validation import validate_flattened_dict
from utility.display import format_traceback, format_exception_info


logger = logging.getLogger(__name__)


class CellError(Exception):
    pass


class Cell(BaseCommand("cell")):

    def __init__(self, name, parent=None):
        super().__init__(name, parent)
        if self.agent_user:
            self._user.set_active_user(self.get_instance(self._user, self.agent_user, required=True))

        self.channels = self.get_channels()

        self._set_sensor(self.agent_sensor)
        logger.debug(f"Set sensor to: {self.sensor_name}")

    def get_state_key(self):
        return f"cell:state:{self.agent_user}:{".".join(self.get_full_name().split(" ")[1:])}"

    def get_sensor_key(self):
        return self.agent_user

    def exec(self):
        #
        # Listen (sensor) - listen
        # Translate (message) - load_message
        # Perform Action (llm / agent) - perform_action
        # Translate (message) - format_message
        # Transmit (transmitter) - send
        # Evaluate Outcome (llm / agent) - refine_state
        #
        state_key = self.get_state_key()
        sensor_key = self.get_sensor_key()
        logger.info(f"Cell starting with state key: {state_key}")

        try:
            state = self.get_state(
                state_key,
                {"goal": self.agent_goal, "rules": self.agent_rules, "tools": self.agent_tools},
            )
            logger.debug(f"Loaded agent state: {state}")

            logger.debug(f"Starting to listen for {self.sensor_name} with key: {sensor_key}")
            for package in self.listen(self.sensor_name, state_key=sensor_key):
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
                        self.handle_error(error, package)
                        raise error

                    channel = package.sender if self.channel == "sender" else self.channel
                    message = self._format_message(
                        {
                            "self": self.service_id,
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
            logger.info(f"Sending error data to channel error:{self.channel}: {error}")
            self.send(
                f"error:{self.channel}",
                {
                    "self": self.service_id,
                    "sensor": self.sensor_name,
                    "sender": package.sender,
                    "message": package.message,
                    "error": str(error),
                    "traceback": "\n".join([item.strip() for item in format_traceback()]),
                    "info": "\n".join([item.strip() for item in format_exception_info()]),
                },
            )
        finally:
            self.set_state(state_key, self.refine_state(state))
            logger.debug("Cell cycle complete")

    def process_sensory_message(self, message, state):
        model = self.get_provider("language_model", self.agent_model_provider, **self.agent_model_options)
        prompts = self._render_prompts(
            {
                **state,
                "message": message,
                "field_labels": self.agent_message_field_labels,
                "tools": self.mcp.list_tools(state["tools"]),
            }
        )
        system_message = {"role": "system", "message": prompts["system"]}
        request_prompt = "\n\n".join([prompts["request"], prompts["tools"]])
        request_message = {"role": "user", "message": request_prompt}
        request_tokens = model.get_token_count([system_message, request_message])

        logger.info(f"Cell using model: {model}")
        logger.info(f"Cell system prompt:\n{prompts["system"]}")
        logger.info(f"Cell request prompt:\n{request_prompt}")
        logger.info(f"Cell core token count: {request_tokens}")

        # STOP HERE FOR NOW!!!
        self.sleep(60)
        # for exec_try in range(5):
        #     response = model.exec(
        #         [
        #             system_message,
        #             *self.load_memories(message),
        #             request_message,
        #         ]
        #     )

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
        if channel not in self.channels:
            self.error(f"Channel {channel} does not exist ot you do not have access")

        self.sensor_name = channel
        self.sensor_spec = self.manager.get_channel_spec(self.sensor_name)
        if not self.sensor_spec:
            self.error(f"Channel name {self.sensor_name} is not a valid sensory channel")

    def _load_message(self, package):
        message = package.message
        data_type = None

        sensor_spec_name = self.sensor_spec.name.split(":")
        data_type_index = next((index for index, item in enumerate(sensor_spec_name) if item == "{data_type}"), None)

        if data_type_index is not None:
            data_type = self.sensor_name.split(":")[data_type_index]
        elif self.agent_sensor_data:
            data_type = self.agent_sensor_data

        if data_type:
            facade = self.facade(data_type)
            if isinstance(message, (str, int)):
                instances = facade.values(*self.agent_message_fields, id=message, **self.agent_sensor_filters)
                message = instances[0] if len(instances) > 0 else None
            else:
                instances = facade.values(
                    *self.agent_message_fields, id=message[self.agent_sensor_data_id], **self.agent_sensor_filters
                )
                message = instances[0] if len(instances) > 0 else None

        elif isinstance(message, dict):
            message = validate_flattened_dict(
                flatten_dict(normalize_value(message), self.agent_message_fields),
                self.agent_sensor_filters,
            )
        else:
            if self.agent_message_fields and "message" not in self.agent_message_fields:
                self.error("Message field message of scalar channel value it not specified")

            message = validate_flattened_dict({"message": normalize_value(message)}, self.agent_sensor_filters)

        return message

    def _format_message(self, message):
        # Override in subclasses if needed
        return message

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

    def get_memory_index(self, message):
        try:
            if self.agent_chat_key == "global":
                return self.agent_sensor_key
            return f"{self.agent_sensor_key}:{message[self.agent_chat_key]}"
        except KeyError:
            raise CellError(
                f"Memory index chat key {self.agent_chat_key} is not global and does not exist in message: {message}"
            )

    def get_chat(self, message):
        if not getattr(self, "_chat_index", None):
            self._chat_index = {}

        memory_index = self.get_memory_index(message)
        if memory_index not in self._chat_index:
            self._chat_index[memory_index] = self._chat.retrieve(None, user=self.active_user, name=memory_index)

        return self._chat_index[memory_index]

    def load_memories(self, message):
        return self._chat_message.set_order("created").values("role", "content", chat=self.get_chat(message))

    def save_memories(self, message, *memories):
        for memory in memories:
            self.save_memory(message, memory)

    def save_memory(self, message, memory):
        self.save_instance(
            self._chat_message,
            None,
            fields={**memory, "chat": self.get_chat(message)},
        )

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
