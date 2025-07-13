#%- if tools %#
Once you have completed running any actions or calling available tools needed
then wrap up by summarizing the findings or results to either ellicit new
information or signal completion.

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

The following tool list is available in YAML format...

```yaml
tools:
#%- for tool in tools %#
  - name: <{tool.schema.name}>@<{tool.server}>
    description: |-
      <{tool.schema.description | indent(6)}>
#%- if "properties" in tool.schema.inputSchema and tool.schema.inputSchema["properties"] %#
    parameters:
#%- for param_name, param_info in tool.schema.inputSchema["properties"].items() %#
      <{param_name}>:
        description: <{param_info.get("description", "No description")}>
        type: <{param_info.get("type", "unknown")}>
        required: #%- if param_name in tool.schema.inputSchema.get("required", []) %# true#%- else %# false#%- endif %#
#%- endfor %#
#%- endif %#
#% endfor %#
```
#%- endif %#
