import copy
import datetime
import glob
import logging
import os
import pathlib
import re
import subprocess
import time

from utility.data import Collection, dependents, dump_json, ensure_list, load_json, normalize_value, prioritize
from utility.filesystem import load_file, remove_file, save_file
from utility.parallel import Parallel
from utility.shell import Shell
from utility.text import interpolate

import docker

logger = logging.getLogger(__name__)


class ServiceError(Exception):
    pass


class ManagerServiceMixin:
    def __init__(self):
        super().__init__()

        self.client = None
        try:
            self.client = docker.from_env()
        except Exception as error:
            pass

    @property
    def container_id(self):
        for pattern in (
            r"/var/lib/docker/containers/([^\/]+)/hostname",
            r"/usr/lib/docker/containers/([^\/]+)/hostname",
            r"/lib/docker/containers/([^\/]+)/hostname",
            r"/docker/containers/([^\/]+)/hostname",
        ):
            matches = re.search(pattern, Shell.capture(("cat", "/proc/self/mountinfo")))
            if matches:
                return matches[1]

        raise ServiceError("Container id for service not found")

    def _service_container(self, id):
        if self.client:
            try:
                return self.client.containers.get(id)
            except docker.errors.NotFound:
                pass

        return None

    def generate_image_name(self, base_image, tag=None):
        image = base_image.split(":")[0]
        if tag is None:
            tag = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{image}:{tag}"

    def list_images(self):
        if self.client:
            return self.client.images.list()
        return []

    def create_image(self, id, image_name):
        container = self._service_container(id)
        if container:
            container.commit(image_name)

    def delete_image(self, image_name, force=True, noprune=False):
        if self.client:
            image = self.client.images.get(image_name)
            self.client.images.remove(image.id, force=force, noprune=noprune)

    def _get_network(self, name):
        if self.client:
            try:
                return self.client.networks.get(name)
            except docker.errors.NotFound:
                return self.client.networks.create(name, driver="bridge")
        return None

    def _get_volume(self, name):
        if self.client:
            try:
                return self.client.volumes.get(name)
            except docker.errors.NotFound:
                return self.client.volumes.create(name)
        return None

    def _normalize_name(self, name):
        def create_name(service_name):
            return f"{self.app_name}.{service_name}"

        if isinstance(name, (list, tuple)):
            return [create_name(item) for item in name]
        return create_name(name)

    def _split_name(self, name):
        components = name.split(".")
        return Collection(app_name=components[0], name=components[1])

    @property
    def service_directory(self):
        directory = os.path.join(self.data_dir, "run")
        pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
        return directory

    @property
    def service_names(self):
        services = self.get_spec("services")
        names = [name for name in services.keys() if not services[name].get("template", False)]

        for file in glob.glob(f"{self.service_directory}/*.data"):
            service_info = self._split_name(os.path.basename(file).removesuffix(".data"))
            if service_info.name not in names and service_info.name != "agent":
                names.append(service_info.name)

        return names

    def expand_service_names(self, names):
        all_services = self.service_names
        service_names = []

        if names:
            for name in ensure_list(names, True):
                for existing_name in all_services:
                    if name == existing_name or re.match(name, existing_name):
                        service_names.append(existing_name)
        else:
            service_names = all_services

        return service_names

    def get_service_spec(self, name, services=None):
        if services is None:
            services = self.get_spec("services")

        service_file = self._service_file(name)
        ports = None
        if os.path.isfile(service_file):
            data = load_json(load_file(service_file))
            if data["template"]:
                name = data["template"]
            ports = data["ports"]

        if name not in services:
            return None

        environment = {"ZIMAGI_APP_NAME": self.app_name, "ZIMAGI_CLI_EXEC": False}
        service = copy.deepcopy(services[name])
        service.pop("template", None)

        if ports:
            service["ports"] = ports
        else:
            port_map = {}
            for port_name in ensure_list(service.get("ports", [])):
                port_map[port_name] = None
            service["ports"] = port_map

        for env_name, value in dict(os.environ).items():
            if (env_name.startswith("KUBERNETES_") or env_name.startswith("ZIMAGI_")) and not env_name.endswith("_EXEC"):
                environment[env_name] = value

        service = normalize_value(interpolate(service, environment))
        inherit_environment = service.pop("inherit_environment", False)
        if inherit_environment:
            service["environment"] = {**environment, **service["environment"]}
        return service

    def initialize_services(self, names=None):
        if self.client and names:
            services = self.get_spec("services")
            names = dependents(services, ensure_list(names))

            def start_service(service_name):
                if service_name in names and not services[service_name].get("template", False):
                    service_spec = self.get_service_spec(service_name, services=services)
                    if not service_spec:
                        raise ServiceError(f"Service specification for '{service_name}' does not exist")

                    self.start_service(service_name, **service_spec)

            for priority, service_names in sorted(prioritize(services, False).items()):
                Parallel.list(service_names, start_service, error_cls=ServiceError)

    def _service_file(self, name):
        name = self._normalize_name(name)
        return os.path.join(self.service_directory, f"{name}.data")

    def _save_service(self, name, id, data=None):
        if not data:
            data = {}

        data["id"] = id
        save_file(self._service_file(name), dump_json(data, indent=2))

    def get_service(self, name, template=None, create=True):
        if not self.client:
            return None

        service_file = self._service_file(name)
        services = self.get_spec("services")

        for dependent in dependents(services, [name]):
            if dependent != name:
                dependent_data = self.get_service(dependent, create=create)
                if not dependent_data:
                    return None

        if os.path.isfile(service_file):
            data = load_json(load_file(service_file))
            service_spec = self.get_service_spec(name)
            if not service_spec:
                raise ServiceError(f"Service specification for '{name}' does not exist")

            service = self._service_container(data["id"])
            if not service and create:
                service_id = self.start_service(name, template=data["template"], **service_spec)
                service = self._service_container(service_id)
            if service:
                if service.status != "running":
                    if create:
                        self.print("{} {}".format(self.notice_color("Restarting Zimagi service"), self.key_color(name)))
                        service_id = self.start_service(name, template=data["template"], silent=True, **service_spec)
                        service = self._service_container(service_id)
                    else:
                        return None

                data["service"] = service
                data["ports"] = self._get_ports(service)
                return data

            elif create:
                raise ServiceError(f"Zimagi could not initialize and load service {name}")

        elif create:
            spec_name = template if template else name
            service_spec = self.get_service_spec(spec_name)
            if not service_spec:
                raise ServiceError(f"Service specification for '{spec_name}' does not exist")

            self.start_service(name, template=template, **service_spec)
            return self.get_service(name)
        return None

    def _check_service(self, name, service, template=None):
        spec_name = template if template else name
        spec = self.get_service_spec(spec_name)
        start_time = time.time()
        current_time = start_time
        success = True

        if not spec:
            raise ServiceError(f"Service specification for '{spec_name}' does not exist")

        while (current_time - start_time) <= spec.get("wait", 30):
            service = self.client.containers.get(service.id)
            if service.status != "running":
                success = False
                break

            time.sleep(0.1)
            current_time = time.time()

        return (success, service)

    def _delete_service(self, name):
        remove_file(self._service_file(name))

    def start_service(
        self,
        name,
        image,
        template=None,
        silent=False,
        ports=None,
        entrypoint=None,
        command=None,
        environment=None,
        network=None,
        volumes=None,
        memory=None,
        wait=30,
        **options,
    ):
        if not self.client:
            return

        if volumes is None:
            volumes = {}
        if environment is None:
            environment = {}

        for global_variable, global_value in self.get_spec("service.environment", {}).items():
            environment[global_variable] = global_value

        data = self.get_service(name, create=False)
        if data and self._service_container(data["id"]):
            return data["id"]

        if not silent:
            self.print("{} {}".format(self.notice_color("Launching Zimagi service"), self.key_color(name)))
        options = normalize_value(options)
        container_name = self._normalize_name(name)
        network = self._get_network(network if network else self.app_name)

        dns_map = {}
        for service_name in self.service_names:
            dns_map[self._normalize_name(service_name)] = service_name

        volume_info = {}
        for local_path, remote_config in volumes.items():
            if local_path:
                if local_path[0] != "/":
                    local_path = self._normalize_name(local_path)
                    self._get_volume(local_path)

                volume_info[local_path] = remote_config

        options.pop("requires", None)

        if options.get("runtime", "") == "nvidia":
            options["device_requests"] = [docker.types.DeviceRequest(driver="nvidia", count=-1, capabilities=[["gpu"]])]

        if options.get("runtime", None):
            options.pop("runtime")

        service = self._service_container(container_name)
        if service:
            service.remove(force=True)

        service = self.client.containers.run(
            image,
            entrypoint=entrypoint,
            command=command,
            name=container_name,
            hostname=name,
            links=dns_map,
            detach=True,
            mem_limit=memory,
            network=network.name,
            ports=ports,
            volumes=volume_info,
            environment=environment,
            **options,
        )
        success, service = self._check_service(name, service, template)
        self._save_service(
            name,
            service.id,
            {
                "template": template,
                "image": image,
                "volumes": volumes,
                "ports": self._get_ports(service),
                "success": success,
            },
        )
        if not success:
            self._service_error(name, service)
        return service.id

    def stop_service(self, name, remove=False, remove_network=True, remove_image=False, remove_volumes=False):
        if not self.client:
            return

        data = self.get_service(name, create=False)
        if data:
            operation = "Destroying" if remove else "Stopping"
            self.print("{} {}".format(self.notice_color(f"{operation} Zimagi service"), self.key_color(name)))
            container = self.client.containers.get(data["id"])
            container.stop()

            if remove:
                container.remove()
                try:
                    if remove_volumes:
                        for local_path, remote_config in data["volumes"].items():
                            if local_path and local_path[0] != "/":
                                self._get_volume(self._normalize_name(local_path)).remove(force=True)
                    if remove_image:
                        self.client.images.remove(container.image.name)
                    if remove_network:
                        network_name = self.app_name
                        self.client.networks.prune({"name": network_name})
                except Exception:
                    pass
        else:
            service = self._service_container(self._normalize_name(name))
            if service:
                service.remove(force=True)

        if remove:
            self._delete_service(name)

    def _service_error(self, name, service):
        error_message = f"Service {name} terminated with errors"
        log_message = ""

        try:
            log_message = "\n\n{}".format(service.logs().decode("utf-8").strip())
        except docker.errors.APIError as error:
            pass

        self.stop_service(name, True)
        raise ServiceError(f"{error_message}{log_message}")

    def display_service_logs(self, names, tail=20, follow=False):
        if self.client:
            names = self.expand_service_names(names)

            def display_logs(name):
                data = self.get_service(name, create=False)
                if data:
                    container = self.client.containers.get(data["id"])

                    if follow:
                        initial_logs = True
                        while container.status == "running":
                            lines = tail if initial_logs else 0
                            for message in container.logs(stream=follow, follow=follow, tail=lines):
                                self.print(
                                    "[ {} ] {}".format(
                                        self.key_color(name), self.value_color(message.decode("utf-8").strip())
                                    )
                                )
                            initial_logs = False
                    else:
                        for message in container.logs(stream=False, follow=False, tail=tail).decode("utf-8").split("\n"):
                            self.print(f"[ {self.key_color(name)} ] {self.value_color(message.strip())}")
                else:
                    self.print(self.warning_color(f"Service {name} has not been created or is not running"))

            Parallel.list(names, display_logs, error_cls=ServiceError)

    def get_service_shell(self, name, shell="bash"):
        name = self._normalize_name(name)
        subprocess.call(f"docker exec --interactive --tty {name} {shell}", shell=True)

    def _get_ports(self, service):
        ports = {}
        for port_name, port_list in service.attrs["NetworkSettings"]["Ports"].items():
            if port_list:
                for port in port_list:
                    if port["HostIp"] == "0.0.0.0":
                        ports[port_name] = int(port["HostPort"])
                        break
        return ports

    def collect_agents(self):
        def collect(spec, name=None, parents=None):
            if parents is None:
                parents = []
            if name and name == "controller" and not parents:
                return

            if name and "base" in spec:
                yield Collection(command=["agent", *parents, name], spec=spec)
            else:
                sub_parents = [*parents, name] if name else parents

                for key, value in spec.items():
                    if isinstance(value, dict):
                        yield from collect(value, key, sub_parents)

        yield from collect(self.interpolate_spec("command.agent"))

    def _get_agent_name(self, agent_path):
        return " ".join(agent_path).removeprefix("agent").strip()

    def _get_agent_scale_config(self, agent_path):
        return "{}_count".format("_".join(agent_path))
