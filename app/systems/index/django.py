import importlib
import logging
import os
import sys
from functools import lru_cache

from django.apps import apps

logger = logging.getLogger(__name__)


class IndexerDjangoMixin:
    def __init__(self):
        super().__init__()

    def update_search_path(self):
        for lib_dir in self.get_module_dirs(None, False):
            sys.path.append(lib_dir)
        importlib.invalidate_caches()

    @lru_cache(maxsize=None)
    def get_settings_modules(self):
        modules = []
        for module_dir in self.get_module_dirs(None, False):
            settings_file = os.path.join(module_dir, "django.py")

            if os.path.isfile(settings_file):
                spec = importlib.util.spec_from_file_location("module.name", settings_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                modules.append(module)
        return modules

    @lru_cache(maxsize=None)
    def get_installed_apps(self):
        apps = []
        for module_dir in self.get_module_dirs():
            data_dir = os.path.join(module_dir, "data")

            if os.path.isdir(data_dir):
                for name in os.listdir(data_dir):
                    if name[0] != "_" and os.path.isdir(os.path.join(data_dir, name)) and name not in ("base", "mixins"):
                        apps.append(f"data.{name}")

        logger.debug(f"Installed Django applications: {apps}")
        return apps

    @lru_cache(maxsize=None)
    def get_installed_middleware(self):
        middleware = []
        for middleware_dir in self.get_module_dirs("middleware"):
            for name in os.listdir(middleware_dir):
                if name[0] != "_":
                    middleware.append(f"middleware.{name}.Middleware")

        logger.debug(f"Installed Django middleware: {middleware}")
        return middleware

    @lru_cache(maxsize=None)
    def get_models(self):
        models = []
        for model in apps.get_models():
            if getattr(model, "facade", None):
                models.append(model)
        return models
