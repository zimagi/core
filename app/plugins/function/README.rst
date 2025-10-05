=====================================================
README for Directory: app/plugins/function
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses a collection of utility functions implemented as plugins, designed to provide reusable data manipulation, transformation, and information retrieval capabilities across the Zimagi platform. These functions extend the core functionality, allowing for dynamic data processing and integration within various system components.

**Key Functionality**
   *  Data manipulation and transformation (e.g., string operations, list flattening, value extraction).
   *  Data filtering and normalization.
   *  Time-related utility functions.
   *  Retrieval of metadata and specific fields from data models.
   *  Generation of mock data for testing and development.

Dependencies
-------------------------

The plugins in this directory primarily rely on the core Zimagi plugin system (`systems.plugins.index.BaseProvider`) and various utility modules within the Zimagi project, such as `utility.data`, `utility.time`, and `utility.filesystem`. Specific plugins may also leverage standard Python libraries like `re` for regular expressions or `random` for random data generation.

File Structure and Descriptions
-------------------------------

**app/plugins/function/flatten.py**
     **Role:** Provides a function to flatten nested lists or tuples into a single, one-dimensional list.
     **Detailed Description:** This file defines a plugin that takes multiple elements, which can include nested lists or tuples, and recursively flattens them into a single list of individual values. It is useful for normalizing data structures where hierarchical data needs to be processed uniformly.

**app/plugins/function/values.py**
     **Role:** Extracts values from dictionaries or lists of dictionaries, optionally based on a specified key path.
     **Detailed Description:** This plugin allows for the extraction of all values from a dictionary or a list of dictionaries. It supports a `keys` parameter to specify a dot-separated path to retrieve nested values, providing a flexible way to query data structures.

**app/plugins/function/substitute.py**
     **Role:** Replaces occurrences of a substring within a given string.
     **Detailed Description:** This file implements a simple string substitution function. It takes an input string, a search string, and a replacement string, and returns the original string with all instances of the search string replaced by the replacement string.

**app/plugins/function/rstrip.py**
     **Role:** Removes specified suffix characters or whitespace from the end of a string.
     **Detailed Description:** This plugin provides functionality to remove trailing whitespace or a specific suffix from a string. It first strips general whitespace and then, if a suffix is provided, removes it if the string ends with that suffix.

**app/plugins/function/data_key.py**
     **Role:** Retrieves the primary key field name for a specified data type.
     **Detailed Description:** This plugin interacts with the Zimagi command's facade system to obtain the primary key identifier for a given data model type. It's crucial for operations that require unique identification of data records.

**app/plugins/function/data_atomic_fields.py**
     **Role:** Returns a list of atomic (non-relational) field names for a given data type.
     **Detailed Description:** This plugin queries the facade for a specified data type to retrieve a list of all fields that represent atomic values (e.g., strings, integers, booleans) rather than relationships to other data models.

**app/plugins/function/csv.py**
     **Role:** Converts a comma-separated string into a list of strings.
     **Detailed Description:** This plugin takes a string, typically representing comma-separated values, and splits it into a list of individual strings. It also handles cases where the input is already a list or tuple, ensuring a consistent list output.

**app/plugins/function/calculations.py**
     **Role:** Lists calculation names that match a given regular expression pattern.
     **Detailed Description:** This plugin dynamically retrieves and filters the names of available calculations within the system based on a provided regular expression pattern. It's used for discovering and managing calculation plugins.

**app/plugins/function/time_range.py**
     **Role:** Generates a sequence of time units (e.g., days, hours) between a start and end time.
     **Detailed Description:** This plugin leverages the `utility.time` module to create a list of time points within a specified range, based on a given unit type (e.g., "days", "hours"). It's useful for iterating over time periods.

**app/plugins/function/value.py**
     **Role:** Extracts a specific value from a nested dictionary or list of dictionaries using a key path.
     **Detailed Description:** This plugin provides a robust way to access deeply nested values within complex data structures. It accepts a dot-separated key path and an optional default value, returning the value at the specified path or the default if not found.

**app/plugins/function/random_keys.py**
     **Role:** Returns a shuffled list of keys from a dictionary, with an optional limit.
     **Detailed Description:** This plugin takes a dictionary, shuffles its keys randomly, and can return a limited number of these keys. It's useful for selecting a random subset of dictionary keys.

**app/plugins/function/data_id.py**
     **Role:** Retrieves the primary key value for a specified data type.
     **Detailed Description:** This plugin interacts with the Zimagi command's facade to get the actual primary key value (not just the field name) for a given data model type, facilitating direct access to specific records.

**app/plugins/function/lstrip.py**
     **Role:** Removes specified prefix characters or whitespace from the beginning of a string.
     **Detailed Description:** Similar to `rstrip.py`, this plugin removes leading whitespace or a specific prefix from a string. It first strips general whitespace and then, if a prefix is provided, removes it if the string starts with that prefix.

**app/plugins/function/keys.py**
     **Role:** Extracts all keys from a dictionary, with an optional prefix added to each key.
     **Detailed Description:** This plugin returns a list of all keys present in a dictionary. It also supports adding a custom prefix to each key in the resulting list, which can be useful for namespace management or display purposes.

**app/plugins/function/prefix.py**
     **Role:** Adds a specified prefix to each value in a list or to the keys of a dictionary.
     **Detailed Description:** This plugin is designed to prepend a given string to each item in a list or to the keys of a dictionary. It can handle nested data structures if `keys` are specified, allowing for targeted prefixing.

**app/plugins/function/join.py**
     **Role:** Combines multiple lists or individual elements into a single flattened list.
     **Detailed Description:** This plugin takes an arbitrary number of arguments, which can be individual values or lists, and concatenates them into a single, flat list. It's a utility for consolidating disparate data into a unified collection.

**app/plugins/function/split.py**
     **Role:** Splits a string into a list of substrings based on a delimiter.
     **Detailed Description:** This plugin uses regular expressions to split an input string into a list of substrings. It takes the string and a `split_value` (which can be a regular expression pattern) as arguments.

**app/plugins/function/data_scope_fields.py**
     **Role:** Returns a list of field names that define the scope of a data type.
     **Detailed Description:** This plugin queries the facade for a specified data type to retrieve a list of fields that are used to define the unique scope or context of instances of that data type.

**app/plugins/function/default.py**
     **Role:** Provides a default value if the input data is `None`.
     **Detailed Description:** This plugin acts as a null coalescing operator. It takes an input `data` and a `default` value, returning the `default` if `data` is `None` (after normalization), otherwise returning the `data` itself.

**app/plugins/function/data_dynamic_fields.py**
     **Role:** Returns a list of dynamic field names for a given data type.
     **Detailed Description:** This plugin retrieves a list of field names from the facade of a specified data type that are considered "dynamic," meaning their presence or value might change based on context or other data.

**app/plugins/function/capitalize.py**
     **Role:** Capitalizes the first letter of a string.
     **Detailed Description:** This plugin provides a simple string capitalization function. It takes an input string and returns a new string with its first character capitalized and the rest of the characters unchanged.

**app/plugins/function/random_values.py**
     **Role:** Returns a shuffled list of values from a list, with an optional limit.
     **Detailed Description:** This plugin takes a list, shuffles its elements randomly, and can return a limited number of these shuffled values. It's useful for selecting a random subset of list elements.

**app/plugins/function/time.py**
     **Role:** Returns the current time formatted as a string.
     **Detailed Description:** This plugin utilizes the `utility.time` module to get the current timestamp and formats it according to a specified format string (defaulting to ISO 8601-like format).

**app/plugins/function/filter.py**
     **Role:** Filters a dictionary based on key-value pairs in nested dictionaries.
     **Detailed Description:** This plugin iterates through a dictionary and filters its items based on provided key-value filters. It can check for the existence and matching value of a filter parameter within nested dictionary values.

**app/plugins/function/normalize.py**
     **Role:** Normalizes various data types into a consistent format.
     **Detailed Description:** This plugin wraps the `utility.data.normalize_value` function, providing a way to convert strings (e.g., "true", "false", "null", numeric strings) into their appropriate Python types (boolean, None, int, float).

**app/plugins/function/data_relation_fields.py**
     **Role:** Returns a list of field names representing forward relationships for a data type.
     **Detailed Description:** This plugin queries the facade for a specified data type to retrieve a list of field names that represent direct (forward) relationships to other data models.

**app/plugins/function/data_query_fields.py**
     **Role:** Returns a list of field names that are queryable for a data type.
     **Detailed Description:** This plugin retrieves a list of field names from the facade of a specified data type that can be used in query operations, indicating which fields are indexed or searchable.

**app/plugins/function/mock_data.py**
     **Role:** Loads mock data from a YAML file for testing or development purposes.
     **Detailed Description:** This plugin facilitates the loading of predefined mock data. It takes a `type` parameter, which corresponds to a YAML file in the `tests/data/` directory, and returns the parsed data.

**app/plugins/function/data_reverse_relation_fields.py**
     **Role:** Returns a list of field names representing reverse relationships for a data type.
     **Detailed Description:** This plugin queries the facade for a specified data type to retrieve a list of field names that represent reverse relationships, i.e., fields on other models that point back to this model.

**app/plugins/function/base.py**
     **Role:** Defines the base class for all function plugins.
     **Detailed Description:** This file establishes the `BaseProvider` class for "function" type plugins. It inherits from `systems.plugins.index.BasePlugin` and defines the `exec` method, which all concrete function plugins must override to implement their specific logic. This file is fundamental to the plugin architecture within this directory.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow for these function plugins typically begins when they are invoked by other parts of the Zimagi system (e.g., command handlers, data processing pipelines, or other plugins). The `exec` method in each plugin (defined by `app/plugins/function/base.py`) serves as the entry point for its specific functionality. For instance, a command might call `function.time()` to get the current time, which then executes the `exec` method in `app/plugins/function/time.py`. Data-related functions like `app/plugins/function/data_key.py` or `app/plugins/function/data_atomic_fields.py` interact with the `command.facade` to retrieve metadata about data models.

**External Interfaces**
   The plugins in this directory primarily interface with the internal Zimagi system components. Specifically:
   *   **Zimagi Command Facade:** Many `data_` prefixed plugins (e.g., `data_key.py`, `data_atomic_fields.py`) interact with the `self.command.facade()` to retrieve schema information, field lists, and other metadata about data models.
   *   **Zimagi Utility Modules:** Plugins like `time.py`, `normalize.py`, `join.py`, `random_values.py`, and `csv.py` leverage functions from `utility.time` and `utility.data` for core data and time manipulation.
   *   **Filesystem:** `mock_data.py` interacts with the filesystem to load YAML files containing mock data.
   *   **Plugin Manager:** `calculations.py` interacts with the `self.manager` to discover other plugins (specifically, calculation plugins).
