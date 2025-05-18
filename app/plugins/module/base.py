import copy
import glob
import os
import pathlib
import re

import yaml
from systems.commands import profile
from systems.plugins.index import BasePlugin
from utility.data import deep_merge, ensure_list
from utility.filesystem import load_file, save_file


class BaseProvider(BasePlugin("module")):
    def __init__(self, type, name, command, instance=None):
        super().__init__(type, name, command, instance)
        self._module_config = None

    def check_module(self):
        if self.manager.index.validate_module_version(self.module_config()):
            return True
        return False

    def get_remote(self, instance):
        return instance.remote

    def check_dirty(self):
        # Override in subclasses if needed
        return False

    def initialize_instance(self, instance, created):
        if created and instance.name is None:
            instance.name = self.get_module_name(instance)

    def prepare_instance(self, instance, created):
        if instance.name != "core":
            self.module_path(instance.name)
            self.manager.index.save_module_config(
                instance.name, {"remote": self.get_remote(instance), "reference": instance.reference}
            )

    def get_module_name(self, instance):
        return instance.get_id()

    def module_path(self, name, ensure=True):
        path = os.path.join(self.command.base_path, name)
        if ensure:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def module_config(self, force=False):
        if not self._module_config or force:
            self._module_config = self.load_yaml("zimagi.yml") if self.instance.name != "core" else {}
        return self._module_config

    def load_parents(self, completed_index=None):
        if completed_index is None:
            completed_index = {}

        def get_module(provider, remote):
            modules = list(
                self.command.search_instances(
                    self.command._module, [f"provider_type={provider}", f"remote={remote}"], error_on_empty=False
                )
            )
            return modules[0] if len(modules) else None

        config = self.module_config()
        if config and "modules" in config:
            for fields in ensure_list(config["modules"]):
                if fields:
                    fields = copy.deepcopy(fields)
                    remote = fields.pop("remote")
                    provider = fields.pop("provider", "git")
                    module = get_module(provider, remote)

                    if not module or module.name not in completed_index:
                        self.command.exec_local(
                            "module add",
                            {"module_provider_name": provider, "remote": remote, "module_fields": fields, "local": True},
                        )
                        if not module:
                            module = get_module(provider, remote)
                        completed_index[module.name] = True

                    module.provider.load_parents(completed_index)

    def get_profile_class(self):
        return profile.CommandProfile

    def get_profile(self, profile_name, show_options=True):
        instance = self.check_instance("module get profile")
        config = self.module_config()

        if config is None or not isinstance(config, dict):
            config = {}

        config.setdefault("profiles", "profiles")
        module_path = self.module_path(instance.name)
        profile_data = None
        profile_names = []

        if config["profiles"]:
            base_path = "{}/{}".format(module_path, config["profiles"])
            for file in glob.glob(f"{base_path}/**/*.yml", recursive=True):
                profile_names.append(re.sub(r"^\/([^\.]+)\.yml$", r"\1", file[len(base_path) :]))

            if not profile_data:
                profile_data = self.load_yaml("{}/{}.yml".format(config["profiles"], profile_name))

        if profile_name == "list" or not profile_data:
            if show_options:
                self.command.info("Available profiles in this module:\n")
                for name in sorted(profile_names):
                    self.command.info(f" * {self.command.header_color(name)}")

                if profile_name == "list":
                    self.command.error("")
                else:
                    self.command.error(f"Profile {profile_name} not found in module {self.instance.name}")
            else:
                return None

        return self.get_profile_class()(self, profile_name, profile_data)

    def run_profile(self, profile_name, config=None, components=None, display_only=False, test=False, ignore_missing=False):
        if not config:
            config = {}
        if not components:
            components = []

        self.check_instance("module run profile")
        profile = self.get_profile(profile_name, show_options=not ignore_missing)
        if profile:
            profile.run(components, config=config, display_only=display_only, test=test)

    def destroy_profile(self, profile_name, config=None, components=None, display_only=False, ignore_missing=False):
        if not config:
            config = {}
        if not components:
            components = []

        self.check_instance("module destroy profile")
        profile = self.get_profile(profile_name, show_options=not ignore_missing)
        if profile:
            profile.destroy(components, config=config, display_only=display_only)

    def import_tasks(self, tasks_path):
        tasks = {}
        for file_name in self.get_file_names(tasks_path, "yml"):
            task_file = os.path.join(tasks_path, file_name)
            for name, config in self.load_yaml(task_file).items():
                if not name.startswith("_"):
                    tasks[name] = config
        return tasks

    def get_task(self, task_name, show_options=True):
        instance = self.check_instance("module get task")
        module_config = self.module_config()
        tasks = {}

        module_config.setdefault("tasks", "tasks")

        if module_config["tasks"]:
            module_path = self.module_path(instance.name)
            tasks_path = os.path.join(module_path, module_config["tasks"])
            tasks = self.import_tasks(tasks_path)

        if task_name == "list" or task_name not in tasks:
            if show_options:
                self.command.info("Available tasks in this module:\n")
                for name in sorted(tasks.keys()):
                    task = self.command.get_provider("task", tasks[name]["provider"], self, tasks[name])
                    fields = deep_merge(task.get_fields(), {"provider": "<required>"})
                    self.command.info(f" * {self.command.header_color(name)}\n")
                    self.command.notice(yaml.dump(deep_merge(fields, tasks[name])))

            if task_name == "list":
                self.command.error("")
            else:
                self.command.error(f"Task {task_name} not found in module {self.instance.name} zimagi.yml")

        config = tasks[task_name]
        provider = config.pop("provider", "command")

        return self.command.get_provider("task", provider, self, config)

    def exec_task(self, task_name, params=None):
        if not params:
            params = {}

        task = self.get_task(task_name)
        task.exec(params)

    def get_file_names(self, base_path, *extensions):
        files = []
        for filename in os.listdir(base_path):
            if extensions:
                for ext in extensions:
                    if filename.endswith(f".{ext}"):
                        files.append(filename)
            else:
                files.append(filename)
        return files

    def load_file(self, file_name, binary=False, instance=None):
        if not instance:
            instance = self.check_instance("module load file")

        module_path = self.module_path(instance.name)
        path = os.path.join(module_path, file_name)
        return load_file(path, binary)

    def load_yaml(self, file_name, instance=None):
        content = self.load_file(file_name, instance)
        if content:
            content = yaml.safe_load(content)
        return content if content else {}

    def save_file(self, file_name, content="", binary=False, instance=None):
        if not instance:
            instance = self.check_instance("module save file")

        module_path = self.module_path(instance.name)
        path = os.path.join(module_path, file_name)

        save_file(path, content, binary)
        return content

    def save_yaml(self, file_name, data=None):
        if not data:
            data = {}
        return self.save_file(file_name, yaml.dump(data))
