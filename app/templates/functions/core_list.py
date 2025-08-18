from utility import data

#
# List processing functions
#


def ensure_list(value):
    return data.ensure_list(value)

def comma_separated_value(value):
    if isinstance(value, (list, tuple)):
        return ", ".join(value)
    return str(value)
