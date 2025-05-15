import copy
import datetime
import json
import logging
import os
import pickle
import re
import shutil
import time

from terminaltables import AsciiTable

from . import exceptions, settings

logger = logging.getLogger(__name__)


def get_service_url(protocol, host, port):
    return f"{protocol}://{host}:{port}/"


def wrap_api_call(type, path, processor, params=None):
    try:
        return processor()

    except Exception as error:
        logger.debug(f"{type.title()} API error: {format_error(path, error, params)}")
        raise error


def normalize_value(value, strip_quotes=False, parse_json=False):
    if value is not None:
        if isinstance(value, str):
            if strip_quotes:
                value = value.lstrip("'\"").rstrip("'\"")

            if value:
                if re.match(r"^(NONE|None|none|NULL|Null|null)$", value):
                    value = None
                elif re.match(r"^(TRUE|True|true)$", value):
                    value = True
                elif re.match(r"^(FALSE|False|false)$", value):
                    value = False
                elif re.match(r"^\d+$", value):
                    value = int(value)
                elif re.match(r"^\d*\.\d+$", value):
                    value = float(value)
                elif parse_json and value[0] == "[" and value[-1] == "]":
                    value = load_json(value)
                elif parse_json and value[0] == "{" and value[-1] == "}":
                    value = load_json(value)

        elif isinstance(value, (list, tuple)):
            value = list(value)
            for index, element in enumerate(value):
                value[index] = normalize_value(element, strip_quotes, parse_json)

        elif isinstance(value, dict):
            for key, element in value.items():
                value[key] = normalize_value(element, strip_quotes, parse_json)
    return value


def format_options(method, options):
    if options is None:
        options = {}

    for key, value in options.items():
        if isinstance(value, dict):
            options[key] = dump_json(value)
        elif isinstance(value, (list, tuple)):
            if method == "GET":
                options[key] = ",".join(value)
            else:
                options[key] = dump_json(list(value))

    return options


def format_error(path, error, params=None):
    params = ""
    if params:
        param_render = dump_json(params, indent=2)
        params = f"\n{param_render}"

    return "[ {} ]({}) {}\n\n{}".format(
        "/".join(path) if isinstance(path, (tuple, list)) else path,
        params,
        str(error),
        "> " + "\n".join([item.strip() for item in exceptions.format_exception_info()]),
    )


def format_response_error(response, cipher=None):
    message = cipher.decrypt(response.content).decode("utf-8") if cipher else response.text
    try:
        error_data = load_json(message)
        error_message = dump_json(error_data, indent=2)
    except Exception as error:
        error_message = message
        error_data = error_message

    return {"message": f"Error {response.status_code}: {response.reason}: {error_message}", "data": error_data}


def format_table(data, prefix=None):
    table_rows = AsciiTable(data).table.splitlines()
    prefixed_rows = []

    if prefix:
        for row in table_rows:
            prefixed_rows.append(f"{prefix}{row}")
    else:
        prefixed_rows = table_rows

    return ("\n".join(prefixed_rows), len(table_rows[0]))


def format_list(data, prefix=None, row_labels=False, width=None):
    if width is None:
        columns, rows = shutil.get_terminal_size(fallback=(80, 25))
        width = columns

    prefixed_text = ["=" * width]
    if not row_labels:
        labels = list(data[0])
        values = data[1:]
    else:
        values = data

    def format_item(item):
        text = []

        if row_labels:
            values = item[1:]
            if len(values) > 0 and "\n" in values[0]:
                values[0] = f"\n{values[0]}"

            text.append(" * {}: {}".format(item[0].replace("\n", " "), "\n".join(values)))
        else:
            text.append("-" * width)
            for index, label in enumerate(labels):
                value = str(item[index]).strip()
                if "\n" in value:
                    value = f"\n{value}"

                text.append(" * {}: {}".format(label.replace("\n", " "), value))
        return text

    for item in values:
        text = format_item(item)
        if text:
            prefixed_text.extend(text)

    return "\n".join(prefixed_text)


def format_data(data, prefix=None, row_labels=False, width=None):
    if width is None:
        columns, rows = shutil.get_terminal_size(fallback=(80, 25))
        width = columns

    table_text, table_width = format_table(data, prefix)
    if table_width <= width:
        return "\n" + table_text
    else:
        return "\n" + format_list(data, prefix, row_labels=row_labels, width=width)


def dump_json(data, **options):
    def _parse(value):
        if isinstance(value, dict):
            for key, item in value.items():
                value[key] = _parse(item)
        elif isinstance(value, (list, tuple)):
            value = list(value)
            for index, item in enumerate(value):
                value[index] = _parse(item)
        elif isinstance(value, datetime.date):
            value = value.strftime("%Y-%m-%d")
        elif isinstance(value, datetime.datetime):
            value = value.strftime("%Y-%m-%d %H:%M:%S %Z")
        elif value is not None and not isinstance(value, (str, bool, int, float)):
            value = str(value)
        return value

    return json.dumps(_parse(copy.deepcopy(data)), **options)


def load_json(data, **options):
    def _parse(value):
        if isinstance(value, dict):
            for key, item in value.items():
                value[key] = _parse(item)
        elif isinstance(value, (list, tuple)):
            value = list(value)
            for index, item in enumerate(value):
                value[index] = _parse(item)
        elif isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S %Z")
            except ValueError:
                try:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    pass
        return value

    return _parse(json.loads(data, **options))


def cache_data(cache_name, generator_function, cache_lifetime=3600):
    if settings.CACHE_DIR:
        cache_file = os.path.join(settings.CACHE_DIR, f"{cache_name}.pkl")
        timestamp_file = os.path.join(settings.CACHE_DIR, f"{cache_name}.timestamp")
        start_time = 0

        if timestamp_file and os.path.isfile(timestamp_file):
            with open(timestamp_file) as file:
                start_time = float(file.read())

        if (time.time() - start_time) >= cache_lifetime:
            if os.path.isfile(cache_file):
                os.remove(cache_file)
    else:
        cache_file = None

    if cache_file and os.path.isfile(cache_file):
        with open(cache_file, "rb") as file:
            data = pickle.load(file)
    else:
        data = generator_function()
        if cache_file:
            with open(cache_file, "wb") as file:
                pickle.dump(data, file)
            with open(timestamp_file, "w") as file:
                file.write(str(time.time()))

    return data
