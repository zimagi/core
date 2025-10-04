import asyncio
from contextlib import asynccontextmanager
from copy import deepcopy

import mcp.types as types
from django.conf import settings
from django.utils.timezone import now
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from utility.data import Collection, create_token, flatten
from utility.runtime import debug


@asynccontextmanager
async def connect(url, token):
    async with streamablehttp_client(url=url, headers={"Authorization": f"Bearer {token}"}) as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            yield session


def format_tool_message(message):
    if isinstance(message, types.TextContent):
        return message.text
    elif isinstance(message, types.ImageContent):
        return f"Base64 encoded {message.mimeType} image: {message.data}"
    else:
        raise RuntimeError(f"Message type {type(message)} not supported")


class MCPClient:

    def __init__(self, command):
        self.command = command
        self.user = command.active_user
        self.servers = {}

        debug("Initializing MCP servers")

        if settings.KUBERNETES_NAMESPACE:
            self.servers[settings.MCP_LOCAL_SERVER_NAME] = MCPLocalServer(
                self, f"http://{settings.MCP_SERVICE_NAME}.{settings.KUBERNETES_NAMESPACE}"
            )
        elif settings.MCP_SERVICE_NAME:
            self.servers[settings.MCP_LOCAL_SERVER_NAME] = MCPLocalServer(self, f"http://{settings.MCP_SERVICE_NAME}:5000")

        for name, config in command.manager.get_spec("mcp").items():
            url = config.get("url", None)
            token_variable = config.get("token", None)

            if not url or not token_variable:
                self.command.error(f"MCP requires url and token (variable) configurations for server {name}")

            token = getattr(settings, token_variable, None)
            if not token:
                self.command.error(f"MCP token setting {token_variable} does not exist for server {name}")

            self.add_server(name, url, token)

    def add_server(self, name, url, token):
        debug("Adding MCP server")
        debug(name, "MCP server name")
        debug(url, "MCP server URL")
        debug(token, "MCP server token")
        self.servers[name] = MCPServer(self, name, url, token)

    def list_tools(self, allowed_tools=None):
        tool_list = flatten([server.list_tools(allowed_tools) for server in self.servers.values()])
        debug("Listing MCP server tools")
        debug(tool_list, "Tool list")
        return tool_list

    def get_tool_fields(self, name):
        (tool_name, server_name) = self._get_name(name)
        tool = self.servers[server_name].index["tools"][tool_name]
        tool_fields = Collection(
            index=(
                tool.inputSchema["properties"] if "properties" in tool.inputSchema and tool.inputSchema["properties"] else {}
            ),
            required=tool.inputSchema.get("required", []),
        )
        debug("Getting tool fields")
        debug(server_name, "Server name")
        debug(tool_name, "Tool name")
        debug(tool_fields, "Tool fields")
        return tool_fields

    def exec_tool(self, name, arguments=None):
        (tool_name, server_name) = self._get_name(name)
        self._verify_server(server_name)
        return self.servers[server_name].exec_tool(tool_name, arguments)

    def _verify_server(self, server_name):
        if server_name not in self.servers:
            self.command.error(f"Server {server_name} not found in available MCP servers")

    def _get_name(self, name):
        try:
            (resource_name, server_name) = name.split("@")
        except ValueError:
            resource_name = name
            server_name = settings.MCP_LOCAL_SERVER_NAME

        debug("Getting MCP server name")
        debug(name, "MCP tool identifier")
        debug(resource_name, "MCP resource name")
        debug(server_name, "MCP server name")

        return (resource_name, server_name)


class MCPServer:

    def __init__(self, client, name, url, token):
        self.client = client
        self.name = name
        self.url = url
        self.token = token
        self.index = {}

    def initialize(self, reload_index=False):
        if reload_index or not self.index:
            debug("Initializing MCP server")
            debug(self.url, "MCP server URL")
            debug(self.token, "MCP server token")

            async def _run_operation():
                async with connect(self.url, self.token) as session:
                    self.index["tools"] = {}

                    tools = await session.list_tools()
                    for tool in tools.tools:
                        self.index["tools"][tool.name] = tool

                    debug(self.index["tools"], "MCP server tools")

            self._preconnect()
            asyncio.run(_run_operation())

    def _preconnect(self):
        # Override in subclass if needed
        pass

    def get_index(self, reload_index=False):
        self.initialize(reload_index)
        return deepcopy(self.index)

    def list_tools(self, allowed_tools=None):
        self.initialize()
        tool_list = [
            Collection(server=self.name, schema=tool)
            for tool in self.index["tools"].values()
            if allowed_tools is None or f"{tool.name}@{self.name}" in allowed_tools
        ]
        debug("Listing MCP server tools")
        debug(tool_list, "Tool list")
        return tool_list

    def exec_tool(self, name, arguments=None):
        tool_name = name.split("@")[0]

        debug("Executing MCP tool")
        debug(name, "MCP tool identifier")
        debug(tool_name, "MCP tool name")

        if arguments is None:
            arguments = {}

        self.initialize()

        if tool_name not in self.index["tools"]:
            raise RuntimeError(f"Tool {tool_name} not found in MCP server {self.name}")

        async def _run_operation():
            async with connect(self.url, self.token) as session:
                messages = []

                debug(self.url, "MCP server URL")
                debug(self.token, "MCP server token")
                debug(tool_name, "MCP tool name")
                debug(arguments, "MCP tool arguments")

                tool = await session.call_tool(tool_name, arguments=arguments)
                debug(tool, "MCP tool response")

                for message in tool.content:
                    debug(message, "MCP tool response message")
                    messages.append(format_tool_message(message))

                tool_response = "\n\n".join(messages)
                debug(tool_response, "Final tool response")
                return tool_response

        self._preconnect()
        return asyncio.run(_run_operation())


class MCPLocalServer(MCPServer):

    def __init__(self, client, url):
        super().__init__(client, settings.MCP_LOCAL_SERVER_NAME, url, None)

    def _preconnect(self):
        self.token = f"{self.client.user.name} {self._get_temp_token()}"

        debug("Running local MCP server preconnect")
        debug(self.token, "Temporary MCP token authentication")

    def _get_temp_token(self):
        def _get_token():
            if (
                not self.client.user.temp_token
                or (now() - self.client.user.temp_token_time).total_seconds() > settings.TEMP_TOKEN_EXPIRATION
            ):
                self.client.user.temp_token = create_token(64)
                self.client.user.temp_token_time = now()
                self.client.user.save()

            return self.client.user.temp_token

        return self.client.command.run_exclusive(f"mcp_temp_token_{self.client.user.name}", _get_token)
