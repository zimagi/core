import os

from django.conf import settings
from utility.filesystem import create_dir, save_yaml

from .base import BaseExecutable


class SchemaCommand(BaseExecutable):

    def exec(self):
        schema_dir = os.path.join(settings.DATA_DIR, "schema")
        self._save_command_schema(schema_dir)
        self._save_data_schema(schema_dir)

    def _save_command_schema(self, schema_dir):
        schema_dir = os.path.join(schema_dir, "command")
        schema_file = os.path.join(schema_dir, "command.yaml")

        if not os.path.exists(schema_file):
            schema = self.command_client.schema.export()
            create_dir(schema_dir)
            save_yaml(schema_file, schema)

        self.print("Command schema generated successfully")

    def _save_data_schema(self, schema_dir):
        schema_dir = os.path.join(schema_dir, "data")
        schema_file = os.path.join(schema_dir, "data.yaml")

        if not os.path.exists(schema_file):
            schema = self.data_client.get_schema(True)
            create_dir(schema_dir)
            save_yaml(schema_file, schema)

        self.print("Data schema generated successfully")
