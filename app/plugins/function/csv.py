from systems.plugins.index import BaseProvider


class Provider(BaseProvider("function", "csv")):
    def exec(self, values_str, sep=","):
        if isinstance(values_str, (list, tuple)):
            return list(values_str)
        return [value.strip() for value in values_str.split(sep)]
