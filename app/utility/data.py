import codecs
import copy
import datetime
import hashlib
import itertools
import json
import pickle
import random
import re
import string
import threading
import uuid
from difflib import SequenceMatcher

import oyaml


class Collection:
    lock = threading.Lock()

    def __init__(self, **attributes):
        for key, value in copy.deepcopy(attributes).items():
            setattr(self, key, value)

    def __iter__(self):
        with self.lock:
            return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __contains__(self, name):
        return name in self.__dict__

    def __setitem__(self, name, value):
        with self.lock:
            self.__dict__[name] = value

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def set(self, name, value):
        self.__setitem__(name, value)

    def __delitem__(self, name):
        with self.lock:
            del self.__dict__[name]

    def __delattr__(self, name):
        self.__delitem__(name)

    def delete(self, name):
        self.__delitem__(name)

    def clear(self):
        with self.lock:
            self.__dict__.clear()

    def items(self):
        with self.lock:
            return self.__dict__.items()

    def __getitem__(self, name):
        if name not in self.__dict__:
            return None
        return self.__dict__[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def get(self, name, default=None):
        if name not in self.__dict__:
            return default
        return self.__dict__[name]

    def check(self, name):
        if name in self.__dict__:
            return True
        return False

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def export(self):
        return copy.deepcopy(self.__dict__)

    def __str__(self):
        return dump_json(self.__dict__, indent=2)

    def __repr__(self):
        return self.__str__()

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for key, value in self.__dict__.items():
            setattr(result, key, copy.deepcopy(value, memo))
        return result


class RecursiveCollection(Collection):
    def __init__(self, **attributes):
        for property, value in attributes.items():
            attributes[property] = self._create_collections(value)

        super().__init__(**attributes)

    def __str__(self):
        def generate_data(data):
            if isinstance(data, Collection):
                properties = {}
                for key, value in data.items():
                    properties[key] = generate_data(value)
                return properties

            elif isinstance(data, (list, tuple)):
                data_list = []
                for value in data:
                    data_list.append(generate_data(value))
                return data_list

            return data

        return dump_json(generate_data(self), indent=2)

    def _create_collections(self, data):
        conversion = data

        if isinstance(data, (list, tuple)):
            conversion = []
            for value in data:
                conversion.append(self._create_collections(value))

        elif isinstance(data, dict):
            conversion = RecursiveCollection(**data)

        return conversion


def ensure_list(data, preserve_null=False):
    if preserve_null and data is None:
        return None
    return list(data) if isinstance(data, (list, tuple)) else [data]


def intersection(data1, data2, ignore_if_empty=False):
    if ignore_if_empty and not data2:
        return data1
    return list(set(ensure_list(data1)) & set(ensure_list(data2)))


def deep_merge(data, override, merge_lists=False, merge_null=True):
    default_override = copy.deepcopy(override if merge_null or override is not None else data)

    if isinstance(data, dict):
        if isinstance(override, dict):
            data = copy.deepcopy(data)
            for key, value in data.items():
                if key in override:
                    data[key] = deep_merge(
                        value,
                        override[key],
                        merge_lists=merge_lists,
                        merge_null=merge_null,
                    )
            for key, value in override.items():
                if key not in data and (merge_null or value is not None):
                    data[key] = value
            return data
        return default_override

    if isinstance(data, (list, tuple)):
        if merge_lists and isinstance(override, (list, tuple)):
            data = copy.deepcopy(data)
            data_length = len(data)
            override_length = len(override)

            if data_length >= override_length:
                for index, value in enumerate(data):
                    if index < override_length:
                        data[index] = deep_merge(
                            value,
                            override[index],
                            merge_lists=merge_lists,
                            merge_null=merge_null,
                        )
            else:
                for index, value in enumerate(override):
                    if index < data_length:
                        data[index] = deep_merge(
                            data[index],
                            value,
                            merge_lists=merge_lists,
                            merge_null=merge_null,
                        )
                    elif merge_null or value is not None:
                        data[index].append(value)
            return data
        return default_override
    return default_override


def flatten(values):
    results = []
    for item in ensure_list(values):
        if isinstance(item, (tuple, list)):
            results.extend(item)
        else:
            results.append(item)
    return results


def chunk_list(data, chunk_size=10):
    data = list(data)
    return [data[index : index + chunk_size] for index in range(0, len(data), chunk_size)]


def clean_list(data, check_value=None):
    return [value for value in data if value is not check_value]


def clean_dict(data, check_value=None):
    return {key: value for key, value in data.items() if value is not check_value}


def sorted_keys(data, key=None, reverse=False):
    if key:
        return sorted(data, key=lambda x: (data[x][key]), reverse=reverse)
    else:
        return sorted(data, key=lambda x: (data[x]), reverse=reverse)


def env_value(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = env_value(value)
    elif isinstance(data, (list, tuple)):
        values = []
        for value in data:
            values.append(env_value(value))
        data = ",".join(values)
    else:
        data = str(data)
    return data


def normalize_value(value, strip_quotes=False, parse_json=False):
    if value is not None:
        if isinstance(value, str):
            if strip_quotes:
                value = value.lstrip("'\"").rstrip("'\"")

            if value:
                if re.match(r"^(NONE|None|none|NULL|Null|null)$", value):
                    value = None
                elif re.match(r"^(TRUE|True|true)$", value):
                    value = True
                elif re.match(r"^(FALSE|False|false)$", value):
                    value = False
                elif re.match(r"^\d+$", value):
                    value = int(value)
                elif re.match(r"^\d*\.\d+$", value):
                    value = float(value)
                elif parse_json and (value[0] == "[" and value[-1] == "]" or value[0] == "{" and value[-1] == "}"):
                    value = load_json(value)

        elif isinstance(value, (list, tuple)):
            value = list(value)
            for index, element in enumerate(value):
                value[index] = normalize_value(element, strip_quotes, parse_json)

        elif isinstance(value, dict):
            for key, element in value.items():
                value[key] = normalize_value(element, strip_quotes, parse_json)
    return value


def normalize_dict(data, process_func=None):
    normalized = {}

    for key, value in data.items():
        if process_func and callable(process_func):
            key, value = process_func(key, value)
        else:
            value = normalize_value(value)
        normalized[key] = value

    return normalized


def get_dict_combinations(data):
    fields = sorted(data)
    combos = []
    for combo_values in itertools.product(*(ensure_list(data[name]) for name in fields)):
        combo_data = {}
        for index, field in enumerate(fields):
            if isinstance(combo_values[index], dict):
                for inner_key, inner_value in combo_values[index].items():
                    combo_data[inner_key] = inner_value
            else:
                combo_data[field] = combo_values[index]
        combos.append(combo_data)
    return combos


def normalize_index(index):
    try:
        return int(index)
    except ValueError:
        return index


def number(data):
    try:
        return int(data)
    except ValueError:
        return float(data)


def format_value(type, value):
    if value is not None:
        if type == "dict":
            if isinstance(value, str):
                value = load_json(value) if value != "" else {}

        elif type == "list":
            if isinstance(value, str):
                value = [x.strip() for x in value.split(",")]
            else:
                value = list(value)

        elif type == "bool":
            if isinstance(value, str):
                if value == "" or re.match(r"^(false|no)$", value, re.IGNORECASE):
                    value = False
                else:
                    value = True
            else:
                value = bool(value)

        elif type == "int":
            value = int(value)

        elif type == "float":
            value = float(value)

    return value


def create_token(length=32, upper=True, lower=True, digits=True):
    chars = ""
    if upper:
        chars += string.ascii_uppercase
    if lower:
        chars += string.ascii_lowercase
    if digits:
        chars += string.digits

    return "t" + "".join(random.SystemRandom().choice(chars) for _ in range(length))


def serialized_token():
    return "<<serialized>>"


def serialize(data):
    return codecs.encode(pickle.dumps(data), "base64").decode().replace("\n", "")


def unserialize(data):
    if data is None:
        return data
    return pickle.loads(codecs.decode(data.encode(), "base64"))


def get_identifier(values):
    if isinstance(values, (list, tuple)):
        values = [str(item) for item in values]
    elif isinstance(values, dict):
        values = [f"{key}:{values[key]}" for key in sorted(values.keys())]
    else:
        values = [str(values)]

    return hashlib.sha256("-".join(sorted(values)).encode()).hexdigest()


def get_uuid(values):
    if isinstance(values, (list, tuple)):
        values = [str(item) for item in values]
    elif isinstance(values, dict):
        values = [f"{key}:{values[key]}" for key in sorted(values.keys())]
    else:
        values = [str(values)]

    hex_string = hashlib.md5("-".join(sorted(values)).encode("UTF-8")).hexdigest()
    return str(uuid.UUID(hex=hex_string))


def rank_similar(values, target, data=None, count=10):
    scores = {}
    for value in values:
        scores[value] = SequenceMatcher(None, target, value).ratio()

    similar = [value for value in dict(sorted(scores.items(), key=lambda item: item[1], reverse=True)).keys()]
    if data:
        return {key: data.get(key, None) for key in similar[0 : min(len(similar), count)]}

    return similar[0 : min(len(similar), count)]


def dependents(data, keys):
    dependents = {}

    def collect_dependents(list):
        for item in list:
            if item in data and isinstance(data[item], dict):
                dependents[item] = True

                requires = ensure_list(data[item].get("requires", None), True)
                if requires:
                    collect_dependents(flatten(requires))

    collect_dependents(keys)
    return list(dependents.keys())


def prioritize(data, keep_requires=False, requires_field="requires"):
    priority_map = {}
    priorities = {}
    dependents = {}

    for name, value in data.items():
        priorities[name] = 0
        if value is not None and isinstance(value, dict):
            if keep_requires:
                requires = ensure_list(value.get(requires_field, None), True)
            else:
                requires = ensure_list(value.pop(requires_field, None), True)

            if requires:
                dependents[name] = flatten(requires)

    while True:
        original_priorities = copy.deepcopy(priorities)

        for name in list(dependents.keys()):
            for require in dependents[name]:
                if require in priorities:
                    if name not in priorities:
                        priorities[name] = 0
                    priorities[name] = max(priorities[name], priorities[require] + 1)

        if original_priorities == priorities:
            break

    for name, priority in priorities.items():
        if priority not in priority_map:
            priority_map[priority] = []
        priority_map[priority].append(name)

    return priority_map


def dump_json(data, **options):
    def _parse(value):
        if isinstance(value, dict):
            for key, item in value.items():
                value[key] = _parse(item)
        elif isinstance(value, (list, tuple)):
            value = list(value)
            for index, item in enumerate(value):
                value[index] = _parse(item)
        elif isinstance(value, datetime.datetime):
            try:
                value = value.strftime("%Y-%m-%d %H:%M:%S %Z")
            except ValueError:
                value = None
        elif isinstance(value, datetime.date):
            try:
                value = value.strftime("%Y-%m-%d")
            except ValueError:
                value = None
        elif value is not None and not isinstance(value, (str, bool, int, float)):
            value = str(value)
        return value

    return json.dumps(_parse(copy.deepcopy(data)), **options)


def load_json(data, **options):
    def _parse(value):
        if isinstance(value, dict):
            for key, item in value.items():
                value[key] = _parse(item)
        elif isinstance(value, (list, tuple)):
            value = list(value)
            for index, item in enumerate(value):
                value[index] = _parse(item)
        elif isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S %Z")
            except ValueError:
                try:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    pass
        return value

    return _parse(json.loads(data, **options))


def dump_yaml(data):
    return oyaml.dump(data)


def load_yaml(yaml_str):
    if yaml_str:
        yaml_str = oyaml.safe_load(yaml_str)
    return yaml_str if yaml_str else {}
