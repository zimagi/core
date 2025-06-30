import re
import copy

from systems.commands.index import BaseCommand
from utility.data import Collection, normalize_value, load_json, dump_json


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
            self.channel,
            {
                "sender": package.sender,
                "message": message,
                "response": response.result,
                "time": response.time,
                "memory": response.memory,
            },
        )

    def _process_message(self, message, state):
        model = self.get_provider("language_model", self.model_provider, **self.model_options)
        prompts = self._render_prompts({**state, "message": message, "tools": self.mcp.list_tools(state["tools"])})

        for exec_try in range(5):
            request = "\n\n".join([prompts["request"], prompts["tools"]])
            response = model.exec(
                [
                    {"role": "system", "message": prompts["system"]},
                    *self.load_memories(message, prompts["request"]),
                    {"role": "user", "message": request},
                ]
            )

            tool_call = re.search(r"```json([^`])```", response.text)
            if tool_call:
                tool_data = load_json(tool_call.group(1).strip())
                if self.validate_exec(tool_data):
                    response = self.mcp.exec_tool(tool_data["tool"], tool_data["parameters"])
            else:
                return {"comment": response.text}

    def refine_state(self, package, message, state):
        return state

    def get_sensor_key(self):
        return self.sensor_key if self.sensor_key else self.channel

    def load_message(self, message):
        if self.sensor.startswith("data:save:"):
            data_type = self.sensor.split(":")[2]
            return self.facade(data_type).values(*self.message_fields, id=message)[0]
        elif isinstance(message, dict):
            return {name: value for name, value in message.items() if not self.message_fields or name in self.message_fields}
        return message

    def _check_message(self, message):
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
        return {
            "system": f"cell/prompt/{self.system_template}.md",
            "tools": f"cell/prompt/{self.tools_template}.md",
            "request": f"cell/prompt/{self.template}.md",
        }

    def load_memories(self, message, request_prompt):
        return []

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
