#%- if references %#
Below is a collection of file and website references derived from the previous responses and tool call results.

## External resource references

#%- for identifier, values in references.items() %#
```json:<{identifier}>
<{json(values)}>
```
#% endfor %#
#%- endif %#
