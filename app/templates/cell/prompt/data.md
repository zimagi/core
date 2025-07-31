#%- if data %#
Below is a collection of datasets derived from the previous responses and tool call results.

## Datasets

#%- for identifier, values in data.items() %#
```json:<{identifier}>
<{json(values)}>
```
#% endfor %#
#%- endif %#
