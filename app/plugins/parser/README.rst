=====================================================
README for Directory: app/plugins/parser
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the core parsing logic for various types of dynamic values and expressions used throughout the Zimagi platform. It provides a flexible and extensible mechanism for interpreting and resolving special syntax within configuration, state, and other data structures, enabling dynamic behavior and data retrieval.

**Key Functionality**
   *  Parsing and interpolation of configuration variables.
   *  Resolution of state variables stored in the system.
   *  Execution and evaluation of custom functions.
   *  Generation and management of unique tokens.
   *  Evaluation of conditional expressions to determine values.
   *  Resolution of references to data within the system's database.

Dependencies
-------------------------

The parsers within this directory rely on the `systems.plugins.index.BaseProvider` for their foundational structure and integration into the Zimagi plugin system. They also utilize utilities from `utility.data` for data manipulation, JSON handling, and value normalization, and `re` for regular expression matching. Specific parsers may have additional internal dependencies on other Zimagi components like the command system or database facades.

File Structure and Descriptions
-------------------------------

**app/plugins/parser/function.py**
     **Role:** Defines the parsing logic for custom functions.
     **Detailed Description:** This file contains the `Provider` class responsible for identifying and executing custom functions embedded within strings. It uses regular expressions to match function syntax, extracts function names and parameters, interpolates parameter values, and then dispatches to registered function providers to perform the actual computation. It handles both standalone function calls and functions embedded within larger strings, and can optionally suppress function execution based on configuration.

**app/plugins/parser/state.py**
     **Role:** Handles the parsing and resolution of system state variables.
     **Detailed Description:** The `Provider` in this file is designed to interpret and substitute references to system state variables. It loads state variables from the Zimagi database and allows for their retrieval, including support for accessing specific keys within dictionary or list state variables. It uses regular expressions to identify state variable syntax and replaces them with their corresponding values, supporting both direct variable references and embedded references within strings.

**app/plugins/parser/config.py**
     **Role:** Manages the parsing and interpolation of configuration variables.
     **Detailed Description:** This file's `Provider` class is dedicated to resolving configuration variables, which can originate from Django settings or the Zimagi configuration database. It supports accessing nested values within configuration dictionaries or lists using bracket notation. The parser handles both direct configuration variable references and embedded references, and can apply formatting (e.g., JSON dumping) to the resolved values. It also allows for runtime overrides of configuration values.

**app/plugins/parser/token.py**
     **Role:** Provides functionality for generating and managing unique tokens.
     **Detailed Description:** The `Provider` in this file is responsible for parsing token generation requests and managing their persistence. It identifies special token syntax, generates unique hexadecimal tokens of a specified length, and stores them in the system's state to ensure they are reused across subsequent requests within the same context. This is useful for generating unique identifiers or temporary credentials.

**app/plugins/parser/conditional_value.py**
     **Role:** Evaluates conditional expressions to determine a resulting value.
     **Detailed Description:** This file contains the `Provider` that parses and evaluates conditional expressions embedded in strings. It uses a specific syntax to define a test condition, a value to return if the condition is true, and a value to return if the condition is false. The parser interpolates all parts of the conditional expression before evaluation and can optionally suppress evaluation based on a configured pattern. It leverages Python's `eval` for dynamic expression evaluation.

**app/plugins/parser/reference.py**
     **Role:** Resolves references to data stored in the Zimagi database.
     **Detailed Description:** The `Provider` in this file is designed to parse and resolve references to database objects and their attributes. It supports complex reference syntax including facade names, scope filters, specific instance names (with wildcards), and field selection, including nested key access. It interacts with the Zimagi facade system to query the database and retrieve the requested data, which can then be returned as a single value, a list, or a dictionary. It also supports operations like distinct values and can store resolved references in configuration variables.

**app/plugins/parser/base.py**
     **Role:** Provides the foundational abstract class for all parser plugins.
     **Detailed Description:** This file defines `BaseProvider`, which serves as the base class for all specific parser implementations within the `app/plugins/parser` directory. It establishes the common interface and core functionality for parsers, including initialization, configuration handling, and a generic `interpolate` method that recursively applies parsing logic to various data structures (strings, lists, dictionaries). Individual parser plugins inherit from this base to implement their specific `parse` method.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The parsing process typically begins when a component within Zimagi (e.g., a command, a configuration loader) encounters a string that might contain dynamic expressions. This component will call the `interpolate` method on an instance of a parser, often `app/plugins/parser/base.py`. The `interpolate` method then iterates through the data, and for each string value, it delegates to the specific `parse` methods of the various parser providers (e.g., `app/plugins/parser/config.py`, `app/plugins/parser/state.py`, `app/plugins/parser/function.py`, etc.) based on the detected syntax (e.g., `@` for config, `$` for state, `#` for function, `&` for reference, `?` for conditional, `%` for token). Each parser attempts to resolve its specific type of expression, and the process continues until all recognized dynamic values are replaced with their resolved counterparts.

**External Interfaces**
   *   **Zimagi Database:** Parsers like `app/plugins/parser/state.py`, `app/plugins/parser/config.py`, and `app/plugins/parser/reference.py` directly interact with the Zimagi database to retrieve stored state variables, configuration values, and data from various models via the facade system.
   *   **Zimagi Command System:** All parsers are initialized with a `command` object, allowing them to access command-specific options, other parser providers, and the underlying database facades.
   *   **Operating System Environment:** The `app/plugins/parser/config.py` parser can access environment variables set at the OS level.
   *   **Python's `eval`:** The `app/plugins/parser/conditional_value.py` parser uses Python's built-in `eval` function to dynamically evaluate conditional expressions.
