import re
import copy

from systems.commands.index import BaseCommand
from utility.data import normalize_value, load_json


class CellError(Exception):
    pass


class Cell(BaseCommand("cell")):

    def exec(self):
        state_key = f"cell:state:{".".join(self.get_full_name().split(" "))}"

        self.manager.load_templates()
        for package in self.listen(self.sensor, state_key=self.get_sensor_key()):
            message = self.load_message(package.message)

            if self._check_message(message):
                state = self.get_state(state_key, {"goal": self.goal, "rules": self.rules, "tools": self.tools})
                self.perform_action(package, message, state)
                self.set_state(state_key, self.refine_state(package, message, state))

    def perform_action(self, package, message, state):
        try:
            self.data("Received message from", package.sender)
            response = self.profile(self._process_message, message, state)

        except Exception as error:
            self.handle_error(error, package)
            raise error

        self.send(
            package.sender if self.channel == "sender" else self.channel,
            self.format_message(
                {
                    "sensor": self.sensor,
                    "sender": package.sender,
                    "message": message,
                    "response": response.result,
                    "time": response.time,
                    "memory": response.memory,
                }
            ),
        )

    def _process_message(self, message, state):
        model = self.get_provider("language_model", self.model_provider, **self.model_options)
        prompts = self._render_prompts({**state, "message": message, "tools": self.mcp.list_tools(state["tools"])})

        for exec_try in range(5):
            request = "\n\n".join([prompts["request"], prompts["tools"]])
            response = model.exec(
                [
                    {"role": "system", "message": prompts["system"]},
                    *self.load_memories(message),
                    {"role": "user", "message": request},
                ]
            )

            tool_call = re.search(r"```json([^`])```", response.text)
            if tool_call:
                tool_data = load_json(tool_call.group(1).strip())
                if self.validate_exec(tool_data):
                    result = self.mcp.exec_tool(tool_data["tool"], tool_data["parameters"])
                    self.save_memories(
                        message,
                        {"role": "assistant", "message": response.text},
                        {"role": "assistant", "message": result},
                    )
            else:
                self.save_memories(
                    message, {"role": "user", "message": prompts["request"]}, {"role": "assistant", "message": response.text}
                )
                return {"comment": response.text}

        raise CellError("Maximum amount of retries")

    def refine_state(self, package, message, state):
        return state

    def get_sensor_key(self):
        return self.sensor_key if self.sensor_key else self.channel

    def load_message(self, message):
        self._sensor_data_type = None

        if self.sensor.startswith("data:save:"):
            self._sensor_data_type = self.sensor.split(":")[2]
        elif self.sensor_data:
            self._sensor_data_type = self.sensor_data

        if self._sensor_data_type:
            facade = self.facade(self._sensor_data_type)
            if isinstance(message, (str, int)):
                instances = facade.values(*self.message_fields, id=message, **self.sensor_filters)
                return instances[0] if len(instances) > 0 else None
            else:
                instances = facade.values(*self.message_fields, id=message[self.sensor_data_id], **self.sensor_filters)
                return instances[0] if len(instances) > 0 else None

        elif isinstance(message, dict):
            return {name: value for name, value in message.items() if not self.message_fields or name in self.message_fields}

        return message

    def format_message(self, message):
        # Override in subclasses if needed
        return message

    def _check_message(self, message):
        if not message:
            return False

        if not self._sensor_data_type:
            for field, value in self.sensor_filters.items():
                value = normalize_value(value)
                # Filter field doesn't exist
                if field not in message:
                    return False
                # Scalar message and filter values do not match
                elif normalize_value(message[field]) != value:
                    return False

        return self.validate_message(message)

    def validate_message(self, message):
        # Override in subclasses if needed
        return True

    def _render_prompts(self, state):
        prompts = copy.deepcopy(self.get_prompts())
        for name, prompt_file in prompts.items():
            template = self.manager.template_engine.get_template(prompt_file)
            prompts[name] = template.render(**state)
        return prompts

    def get_prompts(self):
        prompt_base = "cell/prompt"
        return {
            "system": f"{prompt_base}/{self.system_template}.md",
            "tools": f"{prompt_base}/{self.tools_template}.md",
            "request": f"{prompt_base}/{self.template}.md",
        }

    def get_memory_index(self, message):
        try:
            if self.chat_key == "global":
                return self.sensor_key
            return f"{self.sensor_key}:{message[self.chat_key]}"
        except KeyError:
            raise CellError(f"Memory index chat key {self.chat_key} is not global and does not exist in message: {message}")

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
        self.send(self.sensor, package.message, package.sender)
