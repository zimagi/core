# System Instructions

## Objective

<{goal}>

## Request Received

This is a message we just received that needs to be acted upon.

#%- for field, value in message.items() %#
#% if '\n' in value %#

- <{field}>:
  <{value}>

#%- else %#

- <{field}>: <{value}>

#%- endif %#
#%- endfor %#

Once you have completed running any actions or calling available tools
needed then wrap up by summarizing the findings or results.
