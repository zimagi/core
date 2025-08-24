import re

import mcp.types as types
from django.conf import settings
from django.core.management.base import CommandError


def get_type(method, type):
    if method == "fields":
        type = "dict"
    elif method == "variables":
        type = "list"

    if type == "str":
        return "string"
    elif type == "int":
        return "integer"
    elif type == "float":
        return "number"
    elif type == "bool":
        return "boolean"
    elif type == "list":
        return "array"
    elif type == "dict":
        return "object"
    else:
        raise CommandError(f"Unsupported MCP field type: {type}")


def index_tools(user, server):
    from systems.commands import action, messages, router
    from systems.commands.index import find_command
    from utility.data import dump_json

    async def tools_list_handler(request):
        tools = []

        def index_commands(command):
            for subcommand in command.get_subcommands():
                if isinstance(subcommand, router.RouterCommand):
                    index_commands(subcommand)

                elif isinstance(subcommand, action.ActionCommand) and subcommand.mcp_enabled():
                    if subcommand.check_execute(user):
                        subcommand.parse_base()

                        name = subcommand.get_full_name()
                        required_fields = []
                        command_fields = {}

                        for field_name, field in subcommand.schema.items():
                            if "mcp" in field.tags:
                                field_type = get_type(field.method, field.type)
                                command_fields[field_name] = {
                                    "type": field_type,
                                    "description": f"{field.description[0].upper()}{field.description[1:]}",
                                }
                                if field.required:
                                    required_fields.append(field_name)

                        tools.append(
                            types.Tool(
                                name=":".join(name.split(" ")),
                                description=re.sub(r"\n+", "\n", subcommand.get_description().strip()),
                                inputSchema={
                                    "type": "object",
                                    "required": required_fields,
                                    "properties": command_fields,
                                },
                            )
                        )

        index_commands(settings.MANAGER.index.command_tree)
        return types.ServerResult(types.ListToolsResult(tools=tools))

    async def tool_call_handler(request):
        try:
            command = find_command(" ".join(request.params.name.split(":")))
            has_errors = False
            output = []
            options = {}

            if not command.check_execute(user):
                raise Exception("Access denied")

            if request.params.arguments:
                options = command.format_fields(request.params.arguments)

            command.bootstrap(options)
            for response in command.handle_api(options, package=False):
                if not response.system and not response.silent:
                    if (
                        isinstance(
                            response,
                            (
                                messages.InfoMessage,
                                messages.NoticeMessage,
                                messages.SuccessMessage,
                            ),
                        )
                        and response.message
                    ):
                        output.append(types.TextContent(type="text", text=response.message))

                    elif isinstance(response, messages.DataMessage) and response.data:
                        response_message = f"{response.message}\n" if response.message else ""
                        response_id = f"json:{response.name}" if response.name else "json"
                        output.append(
                            types.TextContent(
                                type="text",
                                text=f"{response_message}```{response_id}\n{dump_json(response.data, indent=2)}\n```",
                            )
                        )

                    elif isinstance(response, messages.TableMessage) and response.message:
                        response_id = f"json:{response.name}" if response.name else "json"
                        output.append(
                            types.TextContent(
                                type="text", text=f"```{response_id}\n{dump_json(response.message, indent=2)}\n```"
                            )
                        )

                    elif isinstance(response, messages.ImageMessage) and response.data:
                        output.append(types.ImageContent(type="image", data=response.data, mimeType=response.mimetype))

                    elif isinstance(response, messages.ErrorMessage) and response.message:
                        output.append(types.TextContent(type="text", text=response.message))
                        has_errors = True

            return types.ServerResult(types.CallToolResult(content=output, isError=has_errors))

        except Exception as error:
            return types.ServerResult(
                types.CallToolResult(
                    content=[types.TextContent(type="text", text=str(error))],
                    isError=True,
                )
            )

    server.request_handlers[types.ListToolsRequest] = tools_list_handler
    server.request_handlers[types.CallToolRequest] = tool_call_handler
