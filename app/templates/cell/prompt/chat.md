## Incoming Message

#% for field, value in message.items() %#
#%- if value is string and '\n' in value %#
<{field_labels.get(field, field)}>:

<{value | indent(2, true)}>

#% else %#
<{field_labels.get(field, field)}>: <{comma_separated_value(value)}>
#%- endif %#
#%- endfor %#

## IMPORTANT Reminder

When you have completed processing, be sure to call the "chat:send@local" tool with a response to the user.  This tool call must come in the same message as the completion token <{completion_token}> or in a previous response message.