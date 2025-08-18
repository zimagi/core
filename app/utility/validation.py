import typing


class TypeValidator:
    TYPE_MAP = {
        "str": str,
        "string": str,
        "int": int,
        "integer": int,
        "bool": bool,
        "boolean": bool,
        "float": float,
        "double": float,
        "dict": dict,
        "dictionary": dict,
        "list": list,
        "tuple": tuple,
        "set": set,
        "bytes": bytes,
        "none": type(None),
        "null": type(None),
    }

    @classmethod
    def get_type(cls, type_name):
        # Handle optional types (e.g., "int?" becomes optional int)
        is_optional = type_name.endswith("?")
        if is_optional:
            type_name = type_name[:-1]

        # Look up in our type map
        py_type = cls.TYPE_MAP.get(type_name.lower())
        if py_type is None:
            raise ValueError(f"Unknown type identifier: {type_name}")

        # Wrap in Optional if needed
        if is_optional:
            return typing.Optional[py_type]
        return py_type

    @classmethod
    def is_instance(cls, value, type_name):
        try:
            py_type = cls.get_type(type_name)
            # Special handling for Optional types
            if typing.get_origin(py_type) is typing.Union:
                return value is None or isinstance(value, typing.get_args(py_type)[0])
            return isinstance(value, py_type)
        except ValueError:
            return False


def validate_flattened_dict(flat_dict, filters=None):
    if not filters:
        return flat_dict

    for key, value in flat_dict.items():
        for filter_key, filter_value in filters.items():
            if "__" in filter_key:
                field, lookup = filter_key.rsplit("__", 1)
            else:
                field, lookup = filter_key, "exact"

            if not key.startswith(field + "__") and key != field:
                continue

            if lookup == "exact":
                if value != filter_value:
                    return None
            elif lookup == "iexact":
                if str(value).lower() != str(filter_value).lower():
                    return None
            elif lookup == "contains":
                if str(filter_value) not in str(value):
                    return None
            elif lookup == "icontains":
                if str(filter_value).lower() not in str(value).lower():
                    return None
            elif lookup == "startswith":
                if not str(value).startswith(str(filter_value)):
                    return None
            elif lookup == "istartswith":
                if not str(value).lower().startswith(str(filter_value).lower()):
                    return None
            elif lookup == "endswith":
                if not str(value).endswith(str(filter_value)):
                    return None
            elif lookup == "iendswith":
                if not str(value).lower().endswith(str(filter_value).lower()):
                    return None
            elif lookup == "isnull":
                if filter_value and value is not None:
                    return None
                if not filter_value and value is None:
                    return None
            elif lookup == "in":
                if value not in filter_value:
                    return None
            elif lookup == "gt":
                if not (value > filter_value):
                    return None
            elif lookup == "gte":
                if not (value >= filter_value):
                    return None
            elif lookup == "lt":
                if not (value < filter_value):
                    return None
            elif lookup == "lte":
                if not (value <= filter_value):
                    return None

    return flat_dict
