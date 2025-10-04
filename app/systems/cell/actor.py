import re

from systems.cell.prompt import PromptEngine
from utility.data import deep_merge, dump_json, load_json, load_yaml
from utility.display import format_exception_info, format_traceback
from utility.text import interpolate
from utility.runtime import debug


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
        debug("Adding response message")

        tool_calls = self._parse_message(message)
        message = {"role": role, "content": message}

        debug(tool_calls, "Response tool calls")
        debug(message, "Response message")

        self.memory_manager.add(message)
        if role == "assistant":
            debug("Adding response assistant message")
            self.messages.append(message)
        return tool_calls

    def add_data(self, identifier, data):
        debug("Adding response data")

        if identifier:
            if identifier in self.data:
                if isinstance(self.data[identifier], (list, tuple)):
                    self.data[identifier].append(data)
                else:
                    self.data[identifier] = [self.data[identifier], data]
            else:
                self.data[identifier] = data

            debug(self.data[identifier], f"Identified data structure: {identifier}")
        else:
            self.data[f"data-{self.data_index}"] = data
            self.data_index += 1

            debug(data, f"Indexed data structure: {self.data_index}")

    def add_reference(self, identifier, reference):
        debug("Adding response reference")

        if identifier:
            self.references[identifier] = reference

            debug(reference, f"Adding response reference: {identifier}")
        else:
            self.references[f"[{self.reference_index}]"] = reference
            self.reference_index += 1

            debug(reference, f"Indexed data structure: {self.reference_index}")

    def export(self):
        return {
            "message": self.get_message(),
            "data": self.data,
            "references": self.references,
        }

    def _parse_message(self, message_text):
        tool_calls = []

        debug("Parsing response message")
        debug(message_text, "Message text")

        for data_object in self._parse_data_objects(message_text):
            if self._validate_tool(data_object.data):
                tool_calls.append(data_object.data)
            elif self._validate_reference(data_object.data):
                self.add_reference(data_object.identifier, data_object.data)
            else:
                self.add_data(data_object.identifier, data_object.data)

        debug(tool_calls, "Tool calls")
        return tool_calls

    def _parse_data_objects(self, markdown_text):
        return self._parse_markdown_json(markdown_text) + self._parse_markdown_yaml(markdown_text)

    def _parse_markdown_json(self, markdown_text):
        pattern = r"```json(?::(\w+))?\s*\n(.*?)\n```"
        results = []

        debug("Parsing response markdown JSON")

        for match in re.finditer(pattern, markdown_text, re.DOTALL | re.IGNORECASE):
            identifier = match.group(1)
            json_str = match.group(2).strip()

            debug(identifier, "JSON identifier")
            debug(json_str, "JSON string")
            try:
                results.append(EmbeddedData(load_json(json_str), identifier))
            except Exception:
                logger.debug(f"JSON parse failed: {json_str}")
                continue  # Skip invalid JSON

        debug(results, "JSON parsed response data")
        return results

    def _parse_markdown_yaml(self, markdown_text):
        pattern = r"```yaml(?::(\w+))?\s*\n(.*?)\n```"
        results = []

        debug("Parsing response markdown YAML")

        for match in re.finditer(pattern, markdown_text, re.DOTALL | re.IGNORECASE):
            identifier = match.group(1)
            yaml_str = match.group(2).strip()

            debug(identifier, "YAML identifier")
            debug(yaml_str, "YAML string")
            try:
                results.append(EmbeddedData(load_yaml(yaml_str), identifier))
            except Exception:
                logger.debug(f"YAML parse failed: {yaml_str}")
                continue  # Skip invalid YAML

        debug(results, "YAML parsed response data")
        return results

    def _validate_reference(self, reference_data):
        debug("Validating response reference")
        debug(reference_data, "Reference data")

        if not isinstance(reference_data, dict) or len(reference_data.keys()) != 2:
            debug("Reference is malformed")
            return False
        if "location" not in reference_data or not reference_data["location"]:
            debug("Reference missing location")
            return False
        if "type" not in reference_data or not reference_data["type"] or reference_data["type"] not in ["file", "web"]:
            debug("Type is missing or is not valid")
            return False
        if reference_data["type"] == "file" and ("library" not in reference_data or not reference_data["library"]):
            debug("File type is missing library field")
            return False

        debug("Response reference is valid")
        return True

    def _validate_tool(self, tool_data):
        debug("Validating response tool call")
        debug(tool_data, "Tool data")

        if not tool_data or "tool" not in tool_data or not tool_data["tool"]:
            debug("Tool call is malformed")
            return False

        fields = self.mcp.get_tool_fields(tool_data["tool"])
        if fields.index and ("parameters" not in tool_data or not tool_data["parameters"]):
            debug("Tool call is missing parameters")
            return False

        for required_field in fields.required:
            if required_field not in tool_data["parameters"]:
                debug(required_field, "Tool call is missing required parameter")
                return False

        for input_field in tool_data["parameters"].keys():
            if input_field not in fields.index:
                debug(input_field, "Tool call has an unsupported parameter")
                return False

        debug("Response tool call is valid")
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
        debug("Setting memory sequence")
        debug(message, "Setting memory message")
        debug(name, "Setting memory name")
        self.memory_manager.set_sequence(interpolate(name, message))

    def _start_messages(self, prompts, user, text):
        debug("Starting response message generation")
        debug(prompts, "Actor prompts")
        debug(user, "Actor user")
        debug(text, "Actor search text")

        if "tools" in prompts:
            self.memory_manager.set_tools(prompts["tools"])
        if "system" in prompts:
            self.memory_manager.add_system({"role": "system", "content": prompts["system"]})
        if "request" in prompts:
            self.memory_manager.add({"role": "user", "content": prompts["request"], "sender": user})

        self.memory_manager.search(text)

    def respond(self, event, memory_sequence, search_field, field_labels=None):
        debug("Responding to thesensory event")

        response = Response(self.memory_manager, self.mcp)
        tools = self.mcp.list_tools(self.state_manager["tools"].keys()) if self.state_manager["tools"] else []
        max_cycles = self.get_max_cycles()
        completion_token = self.get_completion_token()
        prompt_variables = {
            **self.state_manager.export(),
            "max_cycles": max_cycles,
            "completion_token": completion_token,
            "user": self.memory_manager.user.name,
            "message": event.message,
            "field_labels": field_labels or {},
            "tools": tools,
        }

        debug(event.message, "Event message")
        debug(search_field, "Search field")
        debug(event.package.user, "Event message user")
        debug(memory_sequence, "Memory sequence")
        debug(tools, "Agent tools")
        debug(max_cycles, "Maximum cycles")
        debug(completion_token, "Completion token")
        debug(prompt_variables, "Prompt variables")

        self._set_memory(event.message, memory_sequence)
        self._start_messages(
            self.prompt_engine.render(prompt_variables),
            event.package.user,
            event.message[search_field],
        )
        for cycle in range(max_cycles):
            debug(cycle, "Executing agent cycle")
            try:
                text = self._instruct(self.memory_manager.load()).text
                is_complete = completion_token in text
                text = text.replace(completion_token, "").strip()

                debug(text, "AI response text")
                debug("Executing tool calls")

                tool_results = self.command.run_list(response.add_message(text), self._exec_tool, event.message)

                debug(tool_results, "AI tool calls")

                for index, value in enumerate(tool_results.data):
                    debug(value.result, "Adding tool result")
                    response.add_message(value.result, "tool")

                if is_complete:
                    debug("AI response complete")
                    break

            except Exception as error:
                debug(format_traceback(), f"Actor response generation failed: {error}")
                return self._handle_error(error)

        response_data = response.export()
        debug(response_data, "Final response data")
        return response_data

    def memorize(self):
        debug("Saving memories")
        self.memory_manager.save()

    def refine_state(self):
        debug("Refining agent state (TODO)")

    def _instruct(self, messages):
        debug("Executing AI model instruction")
        debug(messages, "Context messages")

        model_response = self.command.instruct(
            self.memory_manager.user,
            messages,
        )
        debug(model_response.text, "Response text")
        return model_response

    def _exec_tool(self, tool_data, message):
        debug("Executing AI tool call")

        tool_index = self.state_manager["tools"]
        tool_name = tool_data["tool"]

        debug(tool_data, "Tool call data")
        debug(message, "Message data")
        debug(tool_index, "Tool index")
        debug(tool_name, "Tool name")

        parameters = tool_data.get("parameters", {})
        if tool_index[tool_name] and isinstance(tool_index[tool_name], dict):
            parameters = deep_merge(parameters, interpolate(tool_index[tool_name], message))

        debug(parameters, "Tool parameters")

        response_text = self.mcp.exec_tool(tool_name, parameters)
        tool_response = (
            f"## Tool executed:\n\n```json\n{dump_json({"tool": tool_name, "parameters": parameters}, indent=2)}\n```\n\n"
            f"## Tool response:\n\n{response_text}"
        )
        debug(response_text, "Tool response text")
        debug(tool_response, "Formatted tool response")
        return tool_response

    def _handle_error(self, error):
        debug(format_exception_info(), f"Actor encountered error: {error}")
        return {
            "error": str(error),
            "traceback": format_traceback(),
            "info": format_exception_info(),
        }
