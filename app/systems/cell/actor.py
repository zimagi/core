import logging
import re

from systems.cell.prompt import PromptEngine
from utility.data import dump_json, load_json, load_yaml
from utility.display import format_exception_info, format_traceback
from utility.text import interpolate

logger = logging.getLogger(__name__)


class EmbeddedData:
    def __init__(self, data, identifier=None):
        self.identifier = identifier
        self.data = data

    def __str__(self):
        data_str = dump_json(self.data, indent=2)
        return f"{self.identifier}: {data_str}" if self.identifier else data_str


class Response:
    def __init__(self, memory_manager, mcp):
        self.memory_manager = memory_manager
        self.mcp = mcp

        self.messages = []
        self.data = {}
        self.data_index = 1
        self.references = {}
        self.reference_index = 1

    def __str__(self):
        return (
            f"{self.get_message()}:\n\n"
            f"# Data:\n\n```json\n{dump_json(self.data, indent=2)}\n```\n\n"
            f"# References:\n\n```json\n{dump_json(self.references, indent=2)}\n```"
        )

    def get_message(self):
        return "\n\n".join([f"# Message:\n\n{message["content"]}" for message in self.messages])

    def add_message(self, message, role="assistant"):
        tool_calls = self._parse_message(message)
        message = {"role": role, "content": message}

        self.memory_manager.add(message)
        if role == "assistant":
            self.messages.append(message)
        return tool_calls

    def add_data(self, identifier, data):
        if identifier:
            if identifier in self.data:
                if isinstance(self.data[identifier], (list, tuple)):
                    self.data[identifier].append(data)
                else:
                    self.data[identifier] = [self.data[identifier], data]
            else:
                self.data[identifier] = data
        else:
            self.data[f"data-{self.data_index}"] = data
            self.data_index += 1

    def add_reference(self, identifier, reference):
        if identifier:
            self.references[identifier] = reference
        else:
            self.references[f"[{self.reference_index}]"] = reference
            self.reference_index += 1

    def export(self):
        return {
            "message": self.get_message(),
            "data": self.data,
            "references": self.references,
        }

    def _parse_message(self, message_text):
        tool_calls = []

        for data_object in self._parse_data_objects(message_text):
            if self._validate_tool(data_object.data):
                tool_calls.append(data_object.data)
            elif self._validate_reference(data_object.data):
                self.add_reference(data_object.identifier, data_object.data)
            else:
                self.add_data(data_object.identifier, data_object.data)

        return tool_calls

    def _parse_data_objects(self, markdown_text):
        return self._parse_markdown_json(markdown_text) + self._parse_markdown_yaml(markdown_text)

    def _parse_markdown_json(self, markdown_text):
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

    def _parse_markdown_yaml(self, markdown_text):
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

    def _validate_reference(self, reference_data):
        if not isinstance(reference_data, dict) or len(reference_data.keys()) != 2:
            return False
        if "location" not in reference_data or not reference_data["location"]:
            return False
        if "type" not in reference_data or not reference_data["type"] or reference_data["type"] not in ["file", "web"]:
            return False
        if reference_data["type"] == "file" and ("library" not in reference_data or not reference_data["library"]):
            return False
        return True

    def _validate_tool(self, tool_data):
        if not tool_data or "tool" not in tool_data or not tool_data["tool"]:
            return False

        fields = self.mcp.get_tool_fields(tool_data["tool"])
        if fields.index and ("parameters" not in tool_data or not tool_data["parameters"]):
            return False

        for required_field in fields.required:
            if required_field not in tool_data["parameters"]:
                return False

        for input_field in tool_data["parameters"].keys():
            if input_field not in fields.index:
                return False
        return True


class Actor:

    def __init__(self, command, prompts, search_limit=1000, search_min_score=0.3, keep_previous=5):
        self.command = command
        self.state_manager = self.command.get_state_manager()
        self.memory_manager = self.command.get_memory_manager(
            search_limit=search_limit, search_min_score=search_min_score, keep_previous=keep_previous
        )
        self.prompt_engine = PromptEngine(command, **prompts)

    @property
    def mcp(self):
        return self.command.mcp

    def get_max_cycles(self):
        return 10

    def get_completion_token(self):
        return "<<DONE>>"

    def _set_memory(self, message, name):
        self.memory_manager.set_sequence(interpolate(name, message))

    def _start_messages(self, prompts, user, text):
        if "tools" in prompts:
            self.memory_manager.set_tools(prompts["tools"])
        if "system" in prompts:
            self.memory_manager.add_system({"role": "system", "content": prompts["system"]})
        if "request" in prompts:
            self.memory_manager.add({"role": "user", "content": prompts["request"], "sender": user})

        self.memory_manager.search(text)

    def respond(self, event, memory_sequence, search_field, field_labels=None):
        response = Response(self.memory_manager, self.mcp)
        tools = self.mcp.list_tools(self.state_manager["tools"]) if self.state_manager["tools"] else []
        max_cycles = self.get_max_cycles()
        completion_token = self.get_completion_token()

        self._set_memory(event.message, memory_sequence)
        self._start_messages(
            self.prompt_engine.render(
                {
                    **self.state_manager.export(),
                    "max_cycles": max_cycles,
                    "completion_token": completion_token,
                    "user": self.memory_manager.user.name,
                    "message": event.message,
                    "field_labels": field_labels or {},
                    "tools": tools,
                }
            ),
            event.package.user,
            event.message[search_field],
        )
        for cycle in range(max_cycles):
            try:
                text = self._instruct(self.memory_manager.load()).text
                is_complete = completion_token in text
                text = text.replace(completion_token, "").strip()

                tool_results = self.command.run_list(response.add_message(text), self._exec_tool)
                for index, value in enumerate(tool_results.data):
                    response.add_message(value.result, "tool")

                if is_complete:
                    break

            except Exception as error:
                logger.error("Actor response generation failed")
                logger.debug(f"Internal actor traceback: {format_traceback()}")
                return self._handle_error(error)

        return response.export()

    def memorize(self):
        self.memory_manager.save()

    def refine_state(self):
        pass

    def _instruct(self, messages):
        if self.command.manager.runtime.debug():
            logger.info(f"Context messages: {dump_json(messages, indent=2)}")

        model_response = self.command.instruct(
            self.memory_manager.user,
            messages,
        )
        logger.info(f"Response success: {model_response.text}")
        return model_response

    def _exec_tool(self, tool_data):
        if self.command.manager.runtime.debug():
            logger.info(f"Executing tool: {dump_json(tool_data, indent=2)}")

        response_text = self.mcp.exec_tool(tool_data["tool"], tool_data.get("parameters", {}))
        return (
            f"## Tool executed:\n\n```json\n{dump_json(tool_data, indent=2)}\n```\n\n"
            f"## Tool response:\n\n{response_text}"
        )

    def _handle_error(self, error):
        logger.error(f"Actor encountered error: {error}")
        logger.error("\n".join([item.strip() for item in format_exception_info()]))
        return {
            "error": str(error),
            "traceback": format_traceback(),
            "info": format_exception_info(),
        }
