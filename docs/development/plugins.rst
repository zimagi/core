Developing Plugins
==================

Zimagi's pluggable architecture allows for easy extension of its capabilities without modifying core application logic. This section guides you through developing your own plugins.

Overview
--------
Plugins are independent components that provide various functionalities, such as data processing, file parsing, encryption, and external service integrations. They are dynamically loaded and managed by the Zimagi platform.

Plugin Directory Structure (`app/plugins`)
------------------------------------------
The `app/plugins/` directory serves as the central hub for all pluggable components. It contains subdirectories for different plugin types:

*   **`app/plugins/file_parser`**: Parses various file formats into a standardized text representation.
*   **`app/plugins/text_splitter`**: Breaks down large blocks of text into smaller segments.
*   **`app/plugins/encryption`**: Provides encryption and decryption mechanisms.
*   **`app/plugins/qdrant_collection`**: Manages and interacts with Qdrant vector database collections.
*   **`app/plugins/source`**: Provides data sourcing from various external systems.
*   **`app/plugins/data_processor`**: Performs transformations and manipulations on datasets.
*   **`app/plugins/message_filter`**: Processes and conditionally returns messages.
*   **`app/plugins/field_processor`**: Transforms and manipulates individual data fields.
*   **`app/plugins/worker`**: Manages and scales worker processes.
*   **`app/plugins/encoder`**: Provides text encoding functionalities (embeddings).
*   **`app/plugins/parser`**: Houses core parsing logic for dynamic values and expressions.
*   **`app/plugins/calculation`**: Central repository for mathematical and statistical calculation plugins.
*   **`app/plugins/module`**: Manages module sources (Git, GitHub, local).
*   **`app/plugins/task`**: Defines and manages automated tasks (shell commands, scripts, file uploads).
*   **`app/plugins/formatter`**: Transforms various data types and strings.
*   **`app/plugins/validator`**: Reusable data validation plugins.
*   **`app/plugins/document_source`**: Integrates with external document storage services.
*   **`app/plugins/language_model`**: Encapsulates language model providers.
*   **`app/plugins/function`**: Collection of utility functions.
*   **`app/plugins/search_engine`**: Integrates various search engine services.
*   **`app/plugins/mixins`**: Reusable mixin classes for plugins.
*   **`app/plugins/dataset`**: Manages and processes various types of datasets.
*   **`app/plugins/channel_token`**: Defines and manages channel token plugins.
*   **`app/plugins/data.py`**: Base plugin for data providers.
*   **`app/plugins/base.py`**: Abstract base class for all plugins.

Creating a New Plugin
---------------------
1.  **Choose a Plugin Type**: Decide which existing plugin type your new plugin falls under (e.g., `file_parser`, `data_processor`). If it's a new category, you might need to define a new plugin type in `app/spec/plugins`.
2.  **Create a New File**: Inside the relevant plugin type directory, create a new Python file (e.g., `app/plugins/file_parser/my_custom_parser.py`).
3.  **Inherit from `BaseProvider`**: Your plugin class should inherit from `BaseProvider` (from `app/plugins/base.py`) and the specific `BaseProvider` for its plugin type (e.g., `app/plugins/file_parser/base.py`).
4.  **Implement Required Methods**: Override the abstract methods defined in the base provider (e.g., `parse_file` for a file parser, `exec` for a data processor).
5.  **Define Specification**: Create a corresponding entry in the `app/spec/plugins/[plugin_type].yml` file to define your plugin's name, interfaces, requirements, and options.

Example: Simple Data Processor Plugin
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's say you want to create a data processor that converts a column to uppercase.

1.  **File**: `app/plugins/data_processor/uppercase.py`

    .. code-block:: python

        from app.plugins.data_processor.base import BaseProvider

        class Provider(BaseProvider):
            def exec(self, dataset, **options):
                field = options.get('field')
                if field and field in dataset.columns:
                    dataset[field] = dataset[field].astype(str).str.upper()
                return dataset

2.  **Specification**: Add to `app/spec/plugins/data_processor.yml`

    .. code-block:: yaml

        uppercase:
            name: uppercase
            description: Converts a specified column to uppercase.
            options:
                field:
                    type: string
                    help: The name of the column to convert to uppercase.

This example demonstrates the basic steps. Each plugin type has specific interfaces and requirements detailed in its respective `README.rst` file within `app/plugins`.
