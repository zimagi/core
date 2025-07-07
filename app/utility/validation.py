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
