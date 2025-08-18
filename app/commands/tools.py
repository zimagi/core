from systems.commands.index import Command


class Tools(Command("tools")):

    def exec(self):
        if self.tool_user:
            with self.run_as(self.tool_user) as user:
                tool_index = self._get_tool_index()
        else:
            tool_index = self._get_tool_index()

        self.data("MCP Tool Inventory", tool_index)

    def _get_tool_index(self):
        tool_index = {}
        for tool in self.mcp.list_tools():
            if not self.servers or tool.server in self.servers:
                if tool.server not in tool_index:
                    tool_index[tool.server] = {}

                tool_index[tool.server][f"{tool.schema.name}@{tool.server}"] = {
                    "description": tool.schema.description,
                    "parameters": tool.schema.inputSchema,
                }
        return tool_index
