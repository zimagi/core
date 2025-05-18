from django.conf import settings


class RoleAccessError(Exception):
    pass


class MetaRoles(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = settings.MANAGER.index.roles

    def __getattr__(self, name):
        name = name.replace("_", "-")

        if name in self.index:
            return name
        else:
            raise RoleAccessError(f"Role {name} does not exist")

    def get_index(self):
        return self.index

    def get_help(self, name):
        return self.index[name]


class Roles(metaclass=MetaRoles):
    pass
