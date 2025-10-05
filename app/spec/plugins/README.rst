=====================================================
README for Directory: app/spec/plugins
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for defining the specifications and configurations of various plugin types within the Zimagi platform. These YAML files outline the structure, interfaces, requirements, options, and available providers for each plugin, enabling a modular and extensible system architecture.

**Key Functionality**
   *   **Plugin Definition:** Defines the core structure and capabilities of different plugin categories.
   *   **Interface Specification:** Outlines the methods and their parameters/returns that a plugin of a given type must implement.
   *   **Requirement and Option Configuration:** Specifies mandatory and optional parameters for plugin instantiation and behavior.
   *   **Provider Enumeration:** Lists the concrete implementations available for each plugin type.


Dependencies
-------------------------

The files in this directory are primarily configuration files written in YAML. They are parsed and interpreted by the Zimagi core system to dynamically load and manage plugins. They do not have direct runtime dependencies in the traditional sense of code libraries, but rather define the expected structure for the Zimagi application's plugin management system.


File Structure and Descriptions
-------------------------------

**app/spec/plugins/data_processor.yml**
     **Role:** Defines the specification for data processing plugins.
     **Detailed Description:** This file outlines the `data_processor` plugin, which is responsible for executing transformations and manipulations on `pandas.DataFrame` objects. It specifies an `exec` interface that takes a dataset and options, returning a modified dataset. It also lists various providers like `drop_duplicates`, `drop_na`, `shuffle`, and `sort`, each representing a specific data processing operation.

**app/spec/plugins/validator.yml**
     **Role:** Defines the specification for data validation plugins.
     **Detailed Description:** This file specifies the `validator` plugin, used for validating various data inputs. It includes a `validate` interface that checks a given value and returns a boolean indicating validity. Requirements include an `id` for the validation message. Providers such as `exists`, `unique`, `string`, `number`, and `date_time` are defined, each with specific options to configure their validation logic (e.g., `pattern` for strings, `min`/`max` for numbers, `format` for dates).

**app/spec/plugins/document_source.yml**
     **Role:** Defines the specification for document source plugins.
     **Detailed Description:** This file describes the `document_source` plugin, which handles the retrieval and downloading of documents from various external sources. It defines a `download` interface that takes `folders` and a `root_directory` as parameters. The `google_drive` provider is listed as an example implementation for fetching documents from Google Drive.

**app/spec/plugins/calculation.yml**
     **Role:** Defines the specification for data calculation plugins.
     **Detailed Description:** This file outlines the `calculation` plugin, designed for performing various mathematical and statistical operations on data. It includes interfaces like `process`, `load_items`, `process_item`, and `calc`. Key requirements are `data` (the data model specification key) and `field` (the calculated field name). Options allow for filtering, parent record specification, and parameter passing. Providers include `subtraction`, `addition`, `multiplication`, `division`, `pchange`, `min_max_scale`, `stdev`, `cov`, and `zscore`.

**app/spec/plugins/file_parser.yml**
     **Role:** Defines the specification for file parsing plugins.
     **Detailed Description:** This file specifies the `file_parser` plugin, which is used to extract text content from various file types. It defines a `parse` interface that takes a `file_path` and returns the parsed string content. Providers are listed for common file formats such as `txt`, `md`, `binary`, `docx`, `pptx`, `xlsx`, `csv`, and `pdf`, indicating the system's capability to handle these document types.

**app/spec/plugins/group.yml**
     **Role:** Defines the specification for group data plugins.
     **Detailed Description:** This file describes the `group` plugin, which is a data-oriented plugin extending the `data` base. It is associated with the `group` data model. It includes providers like `role` and `classification`, suggesting that groups can be categorized or assigned roles within the system.

**app/spec/plugins/config.yml**
     **Role:** Defines the specification for configuration data plugins.
     **Detailed Description:** This file outlines the `config` plugin, which is a data-oriented plugin extending the `data` base. It is directly associated with the `config` data model, indicating its role in managing system configurations.

**app/spec/plugins/function.yml**
     **Role:** Defines the specification for general-purpose function plugins.
     **Detailed Description:** This file specifies the `function` plugin, providing a wide array of utility functions. It defines a generic `exec` interface that can take any parameters and return any type. Providers cover diverse functionalities such as `mock_data`, `data_id`, `data_key`, various data field accessors, `calculations`, `flatten`, `keys`, `random_keys`, `random_values`, `filter`, `values`, `value`, `prefix`, `csv`, `join`, `split`, `lstrip`, `rstrip`, `capitalize`, `substitute`, `normalize`, `default`, `time`, and `time_range`.

**app/spec/plugins/formatter.yml**
     **Role:** Defines the specification for data formatting plugins.
     **Detailed Description:** This file describes the `formatter` plugin, used for transforming data into specific display or storage formats. It includes a `format` interface that takes a value and returns a formatted value. A `requirement` for an `id` (formatter message identifier) is specified. Providers include `string` (with sub-providers like `capitalize`, `upper`, `title`, `lower`), `number` (with `integer`), `date`, `date_time`, `joiner`, and `remove_suffix`, each offering distinct formatting capabilities.

**app/spec/plugins/field_processor.yml**
     **Role:** Defines the specification for field-specific data processing plugins.
     **Detailed Description:** This file outlines the `field_processor` plugin, which focuses on processing individual fields within a `pandas.DataFrame`. It defines an `exec` interface that takes a dataset, field data (as a `pandas.Series`), and options, returning a processed `pandas.Series`. Providers like `bool_to_number` and `combined_text` suggest transformations specific to boolean and text fields.

**app/spec/plugins/encryption.yml**
     **Role:** Defines the specification for encryption and decryption plugins.
     **Detailed Description:** This file specifies the `encryption` plugin, which provides functionalities for securing data. It defines `encrypt` and `decrypt` interfaces, handling plain text to cipher text and vice-versa. A `requirement` for `type` (e.g., 'api', 'data') is included. Options allow for specifying a `key`, `decoder`, and `binary_marker`. Providers like `aes256` and `aes256_user` (which extends `aes256` with a `user` requirement) are available for different encryption schemes.

**app/spec/plugins/user.yml**
     **Role:** Defines the specification for user data plugins.
     **Detailed Description:** This file describes the `user` plugin, which is a data-oriented plugin extending the `data` base. It is directly associated with the `user` data model, indicating its role in managing user-related information within the system.

**app/spec/plugins/message_filter.yml**
     **Role:** Defines the specification for message filtering plugins.
     **Detailed Description:** This file outlines the `message_filter` plugin, used for selectively processing messages based on defined criteria. It defines a `filter` interface that takes a `message` dictionary and a `value`, returning either a filtered message or `null`. Providers such as `mentions_me` and `field_exists` suggest filtering based on message content or the presence of specific fields.

**app/spec/plugins/task.yml**
     **Role:** Defines the specification for task execution plugins.
     **Detailed Description:** This file specifies the `task` plugin, which encapsulates various executable operations. It includes `get_fields` and `execute` interfaces. Providers like `command`, `script`, `remote_command`, `remote_script`, and `upload` are defined, each with specific requirements (e.g., `command` string, `script` file) and options (e.g., `options` for interpolation, `sudo`, `lock`). These plugins enable local and remote command/script execution and file transfers.

**app/spec/plugins/source.yml**
     **Role:** Defines the specification for data source plugins.
     **Detailed Description:** This file describes the `source` plugin, responsible for loading data from various origins. It defines interfaces such as `process`, `load`, `load_contexts`, `load_items`, `item_columns`, and `load_item`. A `requirement` for `data` (data model specification key) is included. Options allow for disabling saving and configuring data loading behavior. The `csv_file` provider is detailed with requirements for a `file` path and options for `archive_file`, `separator`, `data_type`, and `header`.

**app/spec/plugins/text_splitter.yml**
     **Role:** Defines the specification for text splitting plugins.
     **Detailed Description:** This file outlines the `text_splitter` plugin, used for breaking down large blocks of text into smaller, manageable segments. It defines a `split` interface that takes a `text` string and returns a list of strings. An `option` for `max_sentence_length` is provided. The `spacy` provider is listed, with options for specifying a `model` (e.g., `en_core_web_lg`) and whether to `validate` sentences.

**app/spec/plugins/search_engine.yml**
     **Role:** Defines the specification for search engine integration plugins.
     **Detailed Description:** This file specifies the `search_engine` plugin, which provides an interface for performing searches using external search engines. It defines a `search` interface that takes a `query` string and `max_results`, returning a list of search results. The `google` provider is listed as an example implementation for integrating with Google Search.

**app/spec/plugins/module.yml**
     **Role:** Defines the specification for module management plugins.
     **Detailed Description:** This file describes the `module` plugin, which is a data-oriented plugin associated with the `module` data model. It provides a rich set of interfaces for managing modules, including `get_profile_class`, `get_profile`, `run_profile`, `export_profile`, `destroy_profile`, `import_tasks`, `get_task`, and `exec_task`. Providers like `core`, `local`, `git`, and `github` are defined, enabling module management from various sources, with `git` and `github` having specific requirements for `remote` and options for `reference`, `username`, `password`, and `keys`.

**app/spec/plugins/worker.yml**
     **Role:** Defines the specification for worker process management plugins.
     **Detailed Description:** This file outlines the `worker` plugin, which is responsible for managing worker processes. It defines an `ensure` interface. Requirements include `worker_type` (e.g., 'processor machine type'), `command_name` (the full command to be executed), and `command_options`. Providers like `docker` and `kubernetes` indicate support for deploying and managing workers in containerized environments.

**app/spec/plugins/dataset.yml**
     **Role:** Defines the specification for dataset management plugins.
     **Detailed Description:** This file specifies the `dataset` plugin, which is a data-oriented plugin associated with the `dataset` data model. It requires `query_fields` to define how data is queried. Options include `dataset_class`, `required_types`, `index_field`, `merge_fields`, `remove_fields`, and `processors`. Providers like `collection` and `period` are defined, with `period` offering extensive options for time-based data querying, including `start_time`, `end_time`, `unit_type`, `units`, `last_known_value`, `forward_fill`, `resample`, `resample_summary`, and `period_fields`.

**app/spec/plugins/parser.yml**
     **Role:** Defines the specification for general-purpose parsing plugins.
     **Detailed Description:** This file describes the `parser` plugin, which is used to interpret and transform various input values. It defines `initialize` and `parse` interfaces. Providers are listed with associated `weight` values, indicating their processing order or priority: `conditional_value`, `function`, `token`, `state`, `config`, and `reference`. The `reference` parser also has a `query` flag.

**app/spec/plugins/encoder.yml**
     **Role:** Defines the specification for data encoding plugins.
     **Detailed Description:** This file outlines the `encoder` plugin, used for transforming text into numerical representations (embeddings). It defines an `encode` interface that takes a list of text strings and returns a list of encoded representations. A `requirement` for a `model` name is included. Options allow for specifying `dimension` and `format` of the embeddings. Providers like `transformer`, `litellm`, and `deepinfra` are listed, with `transformer` having an option for `device` (e.g., 'cuda:0').

**app/spec/plugins/channel_token.yml**
     **Role:** Defines the specification for channel token plugins.
     **Detailed Description:** This file specifies the `channel_token` plugin, which manages tokens for various communication channels. It defines a `load` interface that takes a `message` (int, str, or dict) and returns a dictionary. A `requirement` for `value` (the token string) is included. Options allow for specifying `fields` to load, `filters` to apply, and an `id_field`. The `data_type` provider is listed.

**app/spec/plugins/qdrant.yml**
     **Role:** Defines the specification for Qdrant collection management plugins.
     **Detailed Description:** This file describes the `qdrant_collection` plugin, which provides an interface for interacting with Qdrant vector databases. It defines interfaces for `exists`, `get`, `store`, `remove`, and `search` operations on collections. Options include `dimension` for embedding vectors and `shards` for data distribution. Providers like `memory`, `section`, and `library` are listed, suggesting different ways to manage Qdrant collections.

**app/spec/plugins/language_model.yml**
     **Role:** Defines the specification for language model integration plugins.
     **Detailed Description:** This file outlines the `language_model` plugin, which provides an interface for interacting with various large language models. It defines interfaces for `get_context_length`, `get_max_new_tokens`, `get_max_tokens`, `get_token_count`, and `exec` (for executing the model with messages). A `requirement` for a `model` name is included. An `option` for `output_token_percent` is provided. Providers like `transformer` and `litellm` are listed, with `transformer` having options for `device`, `temperature`, `top_k`, and `top_p`.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The files in `app/spec/plugins` are primarily declarative YAML specifications. They are not executed directly in a traditional sense. Instead, the Zimagi core application reads and interprets these YAML files during its initialization and runtime to understand the available plugin types, their expected interfaces, and their configurations. When a component of Zimagi needs to use a specific plugin (e.g., a `data_processor` or `encryption` plugin), it consults these specifications to ensure proper instantiation and interaction with the chosen plugin provider. The `module.yml` file, for instance, defines how modules (which can contain plugins) are managed, including their profiles and tasks.

**External Interfaces**
   The plugin specifications defined in this directory dictate how Zimagi interacts with various external systems and internal components. For example:
   *   **`qdrant.yml`**: Defines interaction with the Qdrant vector database for vector search and storage.
   *   **`language_model.yml`**: Specifies interfaces for communicating with external or integrated large language models (e.g., via `litellm` or `transformer` libraries).
   *   **`document_source.yml`**: Outlines how documents are retrieved from external sources like Google Drive.
   *   **`search_engine.yml`**: Describes integration with external search providers like Google.
   *   **`worker.yml`**: Defines how worker processes are managed, potentially interacting with container orchestration systems like Docker or Kubernetes.
   *   **`task.yml`**: Specifies tasks that can involve executing commands or scripts, which might interact with the underlying operating system or remote machines via SSH.
