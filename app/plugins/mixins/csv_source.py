import re
import zipfile

import pandas
import requests
from django.conf import settings
from systems.commands.args import get_type
from systems.plugins.index import ProviderMixin
from utility.temp import TempDir


class CSVSourceMixin(ProviderMixin("csv_source")):
    def load_csv_data_from_file(self, file, columns, archive_file=None, separator=",", data_type=None, header=None):
        zipped_file = True if file.endswith(".zip") else False
        temp = TempDir()

        if re.match(r"^https?\:\/\/", file):
            response = requests.get(file)
            if not isinstance(response.content, str) and not zipped_file:
                content = response.content.decode("utf-8")
            else:
                content = response.content

            file = temp.save(content, binary=zipped_file)
        else:
            file = settings.MANAGER.index.get_module_file(file)

        if zipped_file:
            with zipfile.ZipFile(file, "r") as archive:
                archive.extractall(temp.base_path)
            file = temp.path(archive_file)

        data_type = self.get_column_type(data_type)
        file_data = pandas.read_csv(file, sep=separator, engine="python", dtype=data_type, header=header)
        temp.delete()

        if columns:
            return pandas.DataFrame(file_data, columns=columns, dtype=data_type).drop_duplicates(columns)
        else:
            return pandas.DataFrame(file_data, dtype=data_type)

    def get_column_type(self, data_type):
        if data_type is None:
            return data_type
        return get_type(data_type)
