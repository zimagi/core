import re

from utility.data import dump_json, dump_yaml


#
# Text processing functions
#
def split_text(text, pattern):
    return re.split(pattern, text)


#
# Text rendering functions
#
def json(data):
    if isinstance(data, (int, float, str, bool)):
        return data
    return dump_json(data, indent=2)


def yaml(data):
    if isinstance(data, (int, float, str, bool)):
        return data
    return dump_yaml(data, indent=2)
