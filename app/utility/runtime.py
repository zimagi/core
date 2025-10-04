import copy
import shutil
import threading
import inspect

from django.conf import settings

from .data import dump_json


def debug(message, label=None):
    if settings.MANAGER.runtime.debug():
        caller_frame = inspect.currentframe().f_back
        filename = caller_frame.f_code.co_filename.removeprefix(f"{settings.APP_DIR}/").removeprefix(
            f"{settings.ROOT_LIB_DIR}/"
        )
        filename = settings.MANAGER.prefix_color(filename)
        line_number = settings.MANAGER.prefix_color(caller_frame.f_lineno)
        message_prefix = f"{filename}:{line_number}"

        if isinstance(message, (dict, list, tuple)):
            message = dump_json(message, indent=2)
        message = settings.MANAGER.value_color(message)

        if label:
            label = settings.MANAGER.key_color(label)
            message = f"{label}: {message}"

        settings.MANAGER.print(f"{message_prefix} {message}")


class Runtime:
    def __init__(self, config=None):
        self.lock = threading.Lock()
        self.config = config if isinstance(config, dict) else {}

    def clone(self):
        return Runtime(copy.deepcopy(self.config))

    def save(self, name, value):
        with self.lock:
            self.config[name] = value
            return self.config[name]

    def get(self, name, default=None):
        with self.lock:
            if name not in self.config:
                return default
            else:
                return self.config[name]

    def get_or_set(self, name, value=None, default=None):
        if value is not None:
            return self.save(name, value)
        return self.get(name, default)

    def debug(self, value=None):
        return self.get_or_set("debug", value, settings.DEBUG)

    def parallel(self, value=None):
        return self.get_or_set("parallel", value, settings.PARALLEL)

    def color(self, value=None):
        return self.get_or_set("color", value, settings.DISPLAY_COLOR)

    def width(self, value=None):
        columns, rows = shutil.get_terminal_size(fallback=(settings.DISPLAY_WIDTH, 25))
        return self.get_or_set("width", value, columns)

    def admin_user(self, value=None):
        return self.get_or_set("admin_user", value)

    def active_user(self, value=None):
        return self.get_or_set("active_user", value)
