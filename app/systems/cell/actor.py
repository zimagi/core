import logging
import re
import math

from systems.cell.prompt import PromptEngine
from utility.data import load_json, dump_json, load_yaml, ensure_list
from utility.display import format_traceback, format_exception_info

logger = logging.getLogger(__name__)


class EmbeddedData:
    def __init__(self, data, identifier=None):
        self.identifier = identifier
        self.data = data

    def __str__(self):
        data_str = dump_json(self.data, indent=2)
        return f"{self.identifier}: {data_str}" if self.identifier else data_str


class Response:
    def __init__(self, messages=None, data=None):
        self.messages = messages or []
        self.data = data or {}

    def __str__(self):
        return f"{"\n\n".join(messages)}: {dump_json(self.data, indent=2)}"

    def add_message(self, message):
        self.messages.append(message)

    def add_data(self, identifier, data):
        self.data[identifier] = data


class Actor:

    def __init__(self, command, language_model, language_model_options=None, prompts=None, output_token_percent=0.35):
        if language_model_options is None:
            language_model_options = {}
        if prompts is None:
            prompts = {}

        self.command = command
        self.state_manager = self.command.get_state_manager(self)
        self.memory_manager = self.command.get_memory_manager(self)

        self.language_model = self.command.get_provider("language_model", language_model, **language_model_options)
        self.max_tokens = self.language_model.get_max_tokens()
        self.output_token_percent = output_token_percent
        self.max_new_tokens = math.floor(self.max_tokens * self.output_token_percent)
        self.available_tokens = self.max_tokens - self.max_new_tokens

        self.prompt_engine = PromptEngine(command, **prompts)

    @property
    def mcp(self):
        return self.command.mcp

    def get_max_cycles(self):
        return 3

    def get_token_count(self, messages):
        return self.language_model.get_token_count(ensure_list(messages))

    def _get_message_sequence(self, message, field_labels=None):
        if field_labels is None:
            field_labels = {}

        prompts = self.prompt_engine.render(
            {
                **self.state_manager.export(),
                "message": message,
                "field_labels": field_labels,
                "tools": self.mcp.list_tools(self.state_manager["tools"]) if self.state_manager["tools"] else [],
            }
        )
        system_message = {"role": "system", "message": prompts["system"]}
        request_prompt = "\n\n".join([prompts["request"], prompts["tools"]])
        request_message = {"role": "user", "message": request_prompt}
        extra_messages = []
        for prompt_name, prompt_text in prompts.items():
            if prompt_name not in ["system", "tools", "request"]:
                extra_messages.append({"role": "user", "message": prompt_text})

        request_tokens = self.get_token_count([system_message, request_message, *extra_messages])
        return [
            system_message,
            *self.memory_manager.load_memories(message, (self.available_tokens - request_tokens)),
            *extra_messages,
            request_message,
        ]

    def respond(self, message, field_labels=None):
        response = Response()

        for cycle in range(self.get_max_cycles()):
            try:

                response = self.language_model.exec(self._get_message_sequence(message, field_labels))
                logger.debug(f"Response success: {response.text}")

                data_objects = []
                tool_calls = []
                for data_object in self._parse_data_objects(response.text):
                    if self._validate_tool(data_object):
                        tool_calls.append(data_object)
                    else:
                        data_objects.append(data_object)

                if data_objects:
                    for data_object in data_objects:
                        response.add_data(data_object.identifier, data_object.data)

                if tool_calls:
                    results = self.command.run_list(tool_calls, self._exec_tool)
                else:
                    response.add_message({"role": "assistant", "content": response.text})
                    break

            except Exception as error:
                logger.error("Actor response generation failed")
                logger.debug(f"Internal actor traceback: {format_traceback()}")
                return self._handle_error(error)

        return response

    def refine_state(self):
        pass

    def _validate_tool(self, tool_data):
        if not tool_data or "tool" not in tool_data or not tool_data["tool"]:
            return False

        fields = self.command.mcp.get_tool_fields(tool_data["tool"])

        if fields.index and ("parameters" not in tool_data or not tool_data["parameters"]):
            return False

        for required_field in fields.required:
            if required_field not in tool_data["parameters"]:
                return False

        for input_field in tool_data["parameters"].keys():
            if input_field not in fields.index:
                return False

        return True

    def _exec_tool(self, tool_data):
        logger.info(f"Executing tool: {tool_data['tool']}")
        parameters = tool_data.get("parameters", {})
        result = self.command.mcp.exec_tool(tool_data["tool"], parameters)
        return {"role": "assistant", "content": f"Tool executed: {tool_data['tool']}", "result": result}

    def _handle_error(self, error):
        logger.warning(f"Actor encountered error: {error}")
        traceback = "\n".join([item.strip() for item in format_traceback()])
        logger.debug(traceback)
        return {
            "error": str(error),
            "traceback": traceback,
            "info": "\n".join([item.strip() for item in format_exception_info()]),
        }

    def _parse_data_objects(self, markdown_text):
        return self._parse_markdown_json(markdown_text) + self._parse_markdown_yaml(markdown_text)

    def _parse_markdown_json(markdown_text):
        pattern = r"```json(?::(\w+))?\s*\n(.*?)\n```"
        results = []

        for match in re.finditer(pattern, markdown_text, re.DOTALL | re.IGNORECASE):
            identifier = match.group(1)
            json_str = match.group(2).strip()
            try:
                results.append(EmbeddedData(load_json(json_str), identifier))
            except Exception:
                logger.debug(f"JSON parse failed: {json_str}")
                continue  # Skip invalid JSON

        return results

    def _parse_markdown_yaml(markdown_text):
        pattern = r"```yaml(?::(\w+))?\s*\n(.*?)\n```"
        results = []

        for match in re.finditer(pattern, markdown_text, re.DOTALL | re.IGNORECASE):
            identifier = match.group(1)
            yaml_str = match.group(2).strip()
            try:
                results.append(EmbeddedData(load_yaml(yaml_str), identifier))
            except Exception:
                logger.debug(f"YAML parse failed: {yaml_str}")
                continue  # Skip invalid YAML

        return results
