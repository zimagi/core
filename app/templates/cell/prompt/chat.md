# Chat Instructions

## Goals

<{goal}>

## Request Received

#% for field, value in message.items() %#
#%- if value is string and '\n' in value %#
<{field_labels.get(field, field)}>:

<{value | indent(2, true)}>

#% else %#
<{field_labels.get(field, field)}>: <{comma_separated_value(value)}>
#%- endif %#
#%- endfor %#

Once you have completed running any actions or calling available tools
needed then wrap up by summarizing the findings or results to either
ellicit new information or signal completion.
