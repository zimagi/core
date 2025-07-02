import mcp.types as types

from django.conf import settings
from django.core.management.base import CommandError


def get_type(type):
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
    from systems.commands.index import find_command
    from systems.commands import action, router, messages
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
                                field_type = get_type(field.type)
                                command_fields[field_name] = {
                                    "type": field_type,
                                    "description": f"{field.description[0].upper()}{field.description[1:]}",
                                }
                                if field.required:
                                    required_fields.append(field_name)

                        tools.append(
                            types.Tool(
                                name=":".join(name.split(" ")),
                                description=subcommand.get_description(),
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
                        if isinstance(response.data, (list, tuple, dict)):
                            data_text = f"{response.message} JSON: {dump_json(response.data)}"
                        else:
                            data_text = f"{response.message}: {response.data}"

                        output.append(types.TextContent(type="text", text=data_text))

                    elif isinstance(response, messages.TableMessage) and response.message:
                        output.append(types.TextContent(type="text", text=f"Table JSON: {dump_json(response.message)}"))

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
