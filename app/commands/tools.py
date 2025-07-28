from systems.commands.index import Command


class Tools(Command("tools")):

    def exec(self):
        tool_index = {}

        for tool in self.mcp.list_tools():
            if not self.servers or tool.server in self.servers:
                if tool.server not in tool_index:
                    tool_index[tool.server] = {}

                tool_index[tool.server][f"{tool.schema.name}@{tool.server}"] = {
                    "description": tool.schema.description,
                    "parameters": tool.schema.inputSchema,
                }

        self.data("MCP Tool Inventory", tool_index)
