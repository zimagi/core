import os
import re

from django.conf import settings
from utility.filesystem import load_yaml, save_yaml

from .base import BaseExecutable


class SchemaCommand(BaseExecutable):

    def exec(self):
        schema_dir = os.path.join(settings.DATA_DIR, "schema")
        self._save_command_schema(schema_dir)
        self._save_data_schema(schema_dir)

    def _save_command_schema(self, schema_dir):
        schema_dir = os.path.join(schema_dir, "command")
        schema_file = os.path.join(schema_dir, "_command.yaml")

        if not os.path.exists(schema_file):
            schema = self.command_client.schema.export()
            save_yaml(schema_file, schema)
        else:
            schema = load_yaml(schema_file)

        self._save_command_spec(schema_dir, schema)
        self.print("Command schema generated successfully")

    def _save_command_spec(self, schema_dir, schema, command=None):
        if command is None:
            command = []

        if "url" in schema and "name" in schema:
            command_name = ".".join(command)
            schema_file = os.path.join(schema_dir, f"{command_name}.yaml")
            save_yaml(schema_file, schema)
        else:
            for name, spec in schema.items():
                self._save_command_spec(schema_dir, spec, [*command, name])

    def _save_data_schema(self, schema_dir):
        schema_dir = os.path.join(schema_dir, "data")
        schema_file = os.path.join(schema_dir, "_data.yaml")

        if not os.path.exists(schema_file):
            schema = self.data_client.get_schema(True)
            save_yaml(schema_file, schema)
        else:
            schema = load_yaml(schema_file)

        self._save_data_spec(schema_dir, schema)
        self.print("Data schema generated successfully")

    def _save_data_spec(self, schema_dir, schema):
        for path, schema in schema["paths"].items():
            path_name = re.sub(r"[\{\}]", "", path.strip("/").replace("/", "."))
            save_yaml(os.path.join(schema_dir, f"{path_name}.yaml"), schema)
