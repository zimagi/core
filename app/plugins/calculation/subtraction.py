from systems.plugins.index import BaseProvider


class Provider(BaseProvider("calculation", "subtraction")):
    def calc(self, p):
        return (p.b - p.a) if self.check(p.a, p.b) else None
