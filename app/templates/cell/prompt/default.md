# System Instructions

## Request Received

This is a message we just received that needs to be acted upon.

#%- for field, value in message.items() %#
#% if '\n' in value %#
 * <{field}>:
<{value}>
#%- else %#
 * <{field}>: <{value}>
#%- endif %#
#%- endfor %#
