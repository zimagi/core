import re

from systems.plugins.index import BaseProvider
from utility.data import dump_json, normalize_index, normalize_value


class Provider(BaseProvider("parser", "reference")):
    reference_pattern = r"^\&\{?(?:\[([^\]]+)\])?(?:([\!\-\+]+))?([a-z][\_a-z]+)(?:\(([^\)\<\>]+)\))?\:(?:([^\:\<\>]*))?\:([^\[\}]+)(?:\[([^\]\<\>]+)\])?\}?$"  # noqa: E501
    reference_value_pattern = r"(?<!\&)\&\>?\{?((?:\[[^\]]+\])?(?:[\!\-\+]+)?[a-z][\_a-z]+(?:\([^\)\<\>]+\))?\:[^\:\<\>]*\:[^\[\s\}\'\"]+(?:\[[^\]\<\>]+\])?)[\}\s]?"  # noqa: E501

    def parse(self, value, config):
        if not isinstance(value, str) or "&" not in value:
            return value

        if re.search(self.reference_pattern, value):
            value = self.parse_reference(value)
        else:
            for ref_match in re.finditer(self.reference_value_pattern, value):
                reference_value = self.parse_reference(f"&{ref_match.group(1)}")
                if isinstance(reference_value, (list, tuple)):
                    reference_value = ",".join(reference_value)
                elif isinstance(reference_value, dict):
                    reference_value = dump_json(reference_value)

                if reference_value is not None:
                    value = value.replace(ref_match.group(0), reference_value)
                else:
                    value = None
        return value

    def parse_reference(self, value):
        ref_match = re.search(self.reference_pattern, value)
        reference_variable = ref_match.group(1)

        operations = ref_match.group(2)
        if operations:
            operations = operations.strip()
        else:
            operations = ""

        facade = self.command.facade(ref_match.group(3), False)

        scopes = ref_match.group(4)
        scope_filters = {}
        if scopes:
            for scope_filter in scopes.split(";"):
                scope_field, scope_value = scope_filter.split("=")
                scope_value = scope_value.strip()
                if "," in scope_value:
                    scope_value = [value.strip() for value in scope_value.split(",")]

                scope_filters[scope_field.strip()] = normalize_value(scope_value)

            facade.set_scope(scope_filters)

        names = ref_match.group(5)
        if names:
            search_names = names.replace(" ", "").split(",")
            names = []
            for name in search_names:
                if name == "*":
                    names.extend(set(facade.keys()))
                if name[-1] == "*":
                    keys = facade.keys(**{f"{facade.key()}__startswith": name[:-1]})
                    names.extend(set(keys))
                elif name[0] == "*":
                    keys = facade.keys(**{f"{facade.key()}__endswith": name[1:]})
                    names.extend(set(keys))
                else:
                    names.append(name)

        fields = re.split(r"\s*,\s*", ref_match.group(6))
        keys = ref_match.group(7)
        if keys and len(fields) == 1:
            keys = keys.replace(" ", "").split("][")

        def _get_instance_values():
            values = []
            filters = {}

            if names:
                filters[f"{facade.key()}__in"] = names

            query = facade.values(*fields, **filters)
            if "!" in operations:
                query = query.distinct()

            for data in list(query):
                if keys:
                    for field in fields:
                        instance_value = data.get(field, None)
                        if instance_value is not None:
                            if isinstance(instance_value, (dict, list, tuple)):

                                def _get_value(_data, key_list):
                                    if isinstance(_data, (dict, list, tuple)) and len(key_list):
                                        base_key = normalize_index(key_list.pop(0))
                                        try:
                                            return _get_value(_data[base_key], key_list)
                                        except Exception:
                                            return None
                                    return _data

                                data[field] = _get_value(instance_value, keys)

                if len(fields) == 1:
                    data = data[fields[0]]
                values.append(data)
            return values

        instance_values = _get_instance_values()

        if "!" in operations and len(fields) == 1:
            instance_values = list(set(instance_values))

        if "-" in operations or ("+" not in operations and names and len(names) == 1):
            if len(instance_values) == 1:
                instance_values = instance_values[0]
            elif not instance_values:
                instance_values = None

        if reference_variable:
            self.command.options.get_parser("config").set(reference_variable, instance_values)
        return instance_values
