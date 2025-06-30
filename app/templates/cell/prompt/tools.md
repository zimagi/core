## Tools Available

You may choose from the following tools to achieve your goals.

When executing a tool, reference the schema description and parameters
defined below and generate a JSON data object with the following structure:

```json
{
  "tool": "example:tool_name@local",
  "parameters": {
    "example_param1": "some value",
    "example_param2": "another value"
  }
}
```

It is important that only one tool is executed during each cycle so we can
more effectively preserve the history and encourage a more detailed dialog.
Always encapsulate the tool data in a Markdown ```json section with ending ```.

### Tool Reference

#%- for tool in tools %#
tool: {tool.schema.name}@{tool.server}
description: {tool.schema.description}
#%- if "properties" in tool.schema.inputSchema and tool.schema.inputSchema["properties"] %#
parameters:
#%- for param_name, param_info in tool.schema.inputSchema["properties"].items() %#
 - <{param_name}>: <{param_info.get("description", "No description")}>
#%- if param_name in tool.schema.inputSchema.get("required", []) %#  <REQUIRED>#%- endif %#
#%- endfor %#
#%- endif %#
#%- endfor %#
