=====================================================
README for Directory: app/utility
=====================================================

Directory Overview
------------------

**Purpose**
   This directory provides a collection of reusable utility functions and classes designed to support various functionalities across the Zimagi application, ranging from data manipulation and file system operations to external service interactions and parallel processing.

**Key Functionality**
   Data serialization and manipulation, file system management, terminal output formatting, web scraping, Git and SSH operations, time utilities, and parallel execution.

Dependencies
-------------------------

The utilities in this directory rely on several third-party libraries including `pandas` for dataframes, `colorful` for terminal styling, `pygit2` for Git operations, `paramiko` for SSH, `pynvml` for NVIDIA GPU management, `requests` and `urllib3` for HTTP requests, `beautifulsoup4` for HTML parsing, `selenium` for browser automation, `redis` for mutex locking, and `oyaml` for YAML processing. It also depends on Django's settings and timezone utilities.

File Structure and Descriptions
-------------------------------

**app/utility/nvidia.py**
     **Role:** Provides an interface for interacting with NVIDIA GPU devices.
     **Detailed Description:** This file contains the `Nvidia` class, which allows for querying GPU device information such as memory usage and driver versions, and selecting available devices based on specified criteria. It uses the `pynvml` library to communicate with NVIDIA drivers.

**app/utility/query.py**
     **Role:** Offers helper functions for querying and manipulating Django querysets and dictionaries.
     **Detailed Description:** This module includes functions like `get_queryset` for traversing related Django models, `init_fields` and `init_filters` for preparing query parameters, and `get_field_values` for extracting unique field values from a queryset. It aids in constructing and refining data retrieval operations.

**app/utility/text.py**
     **Role:** Contains utilities for text manipulation, interpolation, and formatting.
     **Detailed Description:** This file defines the `Template` class for advanced string interpolation using a custom delimiter, and the `interpolate` function for recursively applying variable substitutions to various data structures. It also provides functions for splitting and wrapping text, including `TextWrapper` for handling paragraphs.

**app/utility/shell.py**
     **Role:** Facilitates the execution of shell commands and captures their output.
     **Detailed Description:** The `Shell` class provides static methods `exec` and `capture` to run external commands. `exec` allows for interactive execution with input and output streaming, while `capture` returns the command's standard output as a string. It handles environment variables and sudo privileges.

**app/utility/validation.py**
     **Role:** Provides tools for validating data types and filtering dictionaries based on various lookup types.
     **Detailed Description:** This module includes `TypeValidator` for checking if a value conforms to a specified Python type, including optional types. It also features `validate_flattened_dict` which can filter a flattened dictionary using Django-like lookup syntax (e.g., `exact`, `contains`, `startswith`).

**app/utility/dataframe.py**
     **Role:** Manages operations related to pandas DataFrames, such as merging and concatenation.
     **Detailed Description:** This file offers functions like `merge` to combine multiple DataFrames with outer joins and optional forward-fill, and `concatenate` to stack DataFrames while handling duplicate indices. It also includes `get_csv_file_name` for consistent CSV naming.

**app/utility/mutex.py**
     **Role:** Implements distributed locking mechanisms using Redis to prevent race conditions.
     **Detailed Description:** This module provides `check_mutex` as a decorator or context manager for acquiring and releasing Redis-backed locks, ensuring exclusive execution of critical sections. The `Mutex` class offers methods to set, clear, and wait for specific keys in Redis, useful for coordinating processes.

**app/utility/python.py**
     **Role:** Contains utilities for dynamic Python module and class creation, and variable parsing.
     **Detailed Description:** This file provides functions to `create_module` and `create_class` dynamically at runtime. The `PythonParser` class handles the parsing of string values that reference Python module attributes, allowing for dynamic configuration loading.

**app/utility/git.py**
     **Role:** Provides a Pythonic interface for Git repository operations.
     **Detailed Description:** The `Git` class wraps the `pygit2` library to perform common Git actions such as cloning, initializing, checking out branches, pulling, committing, and pushing. It also handles Git credentials and submodule management, simplifying interaction with Git repositories.

**app/utility/ssh.py**
     **Role:** Offers a robust client for SSH connections and remote command execution.
     **Detailed Description:** This file defines the `SSH` class, which uses `paramiko` to establish SSH connections, execute commands (including sudo), and perform secure file transfers (upload/download). It also includes methods for generating SSH key pairs and secure passwords.

**app/utility/terminal.py**
     **Role:** Provides utilities for enhanced terminal output, including colored text and formatted messages.
     **Detailed Description:** The `TerminalMixin` class offers methods for printing colored text, formatting timestamps, and styling messages for better readability in the terminal. It integrates with the `colorful` library and handles terminal size and color settings.

**app/utility/project.py**
     **Role:** Manages project-specific directories and file system operations within a project context.
     **Detailed Description:** This file defines the `ProjectDir` class, which extends `FileSystem` to create and manage directories specific to different project types (e.g., "modules", "data"). It provides context managers `project_dir` and `project_temp_dir` for temporary project directory handling.

**app/utility/web.py**
     **Role:** Provides a utility for parsing web pages and extracting text content.
     **Detailed Description:** The `WebParser` class fetches content from specified URLs, uses `BeautifulSoup` to parse HTML, and extracts clean, readable text. It handles common web request errors and can process multiple URLs, making it useful for content extraction.

**app/utility/temp.py**
     **Role:** Manages the creation and cleanup of temporary directories and files.
     **Detailed Description:** This file defines the `TempDir` class, which inherits from `FileSystem` to create uniquely named temporary directories. It provides a `temp_dir` context manager to ensure that temporary directories are automatically cleaned up after use, preventing clutter.

**app/utility/runtime.py**
     **Role:** Manages runtime configuration and settings for the application.
     **Detailed Description:** The `Runtime` class provides a thread-safe mechanism to store and retrieve application-wide configuration settings. It includes methods for toggling debug mode, parallel execution, color output, and managing active user information, allowing for dynamic adjustment of application behavior.

**app/utility/time.py**
     **Role:** Offers comprehensive utilities for time and date manipulation.
     **Detailed Description:** This file defines the `Time` class, which provides methods for converting between strings and datetime objects, shifting dates, calculating time distances, and generating sequences of dates. It handles timezones and daylight saving time considerations.

**app/utility/request.py**
     **Role:** Provides utilities for making HTTP requests, including handling legacy SSL contexts and URL validation.
     **Detailed Description:** This file includes `CustomHttpAdapter` to support legacy SSL connections for `requests`. It also provides `request_legacy_session` to create a session with this adapter and `validate_url` to check the validity of a given URL string using the `validators` library.

**app/utility/crawler.py**
     **Role:** Implements a web crawler for fetching and processing web page content.
     **Detailed Description:** The `WebCrawler` class fetches web pages, extracts text and links, and stores unique statements. It can traverse links up to a specified depth, filters URLs based on domain and format, and processes page content to identify unique textual statements.

**app/utility/parallel.py**
     **Role:** Facilitates parallel execution of tasks using threads and processes.
     **Detailed Description:** This module provides `ThreadPool` for managing worker threads and `Parallel` for executing a list of items concurrently. It includes `ThreadResults` to collect outcomes and errors from parallel tasks, and can raise exceptions for failed operations, making it suitable for performance-critical tasks.

**app/utility/data.py**
     **Role:** Offers a wide range of data manipulation, serialization, and utility functions.
     **Detailed Description:** This file defines `Collection` and `RecursiveCollection` for dictionary-like object access, and includes functions for list and dictionary manipulation (e.g., `ensure_list`, `deep_merge`, `flatten_dict`). It also provides utilities for JSON/YAML serialization, base64 encoding, and generating unique identifiers.

**app/utility/display.py**
     **Role:** Provides functions for formatting and displaying data in the terminal, including tables and lists.
     **Detailed Description:** This module offers `format_table` and `format_list` for presenting structured data in a readable format. It also includes context managers like `suppress_stdout` and `capture_output` for controlling and capturing console output, and functions for displaying exception and traceback information.

**app/utility/filesystem.py**
     **Role:** Provides a comprehensive set of utilities for file system operations.
     **Detailed Description:** This file defines the `FileSystem` class and various functions for creating, removing, loading, and saving files and directories. It supports YAML, JSON, and CSV formats, handles file permissions, and includes context managers for temporary directories, ensuring robust file management.

**app/utility/browser.py**
     **Role:** Provides a high-level interface for browser automation using Selenium.
     **Detailed Description:** This file defines the `Browser` class, which wraps a Selenium Firefox WebDriver to interact with web pages. It includes methods for navigating to URLs, retrieving page titles and source, and selecting elements using various strategies (ID, class, XPath, CSS). The `SelectorMixin` and `Element` classes provide a convenient way to interact with web elements.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The `app/utility` directory primarily consists of helper modules that are imported and utilized by other parts of the Zimagi application. There isn't a single entry point within this directory; rather, its functions and classes are called as needed. For example, a command in `app/systems/manage/service.py` might use `app/utility/shell.py` to execute a Docker command, `app/utility/data.py` to manipulate configuration, and `app/utility/terminal.py` to display formatted output. Web-related tasks might involve `app/utility/request.py` for fetching, `app/utility/web.py` for parsing, and `app/utility/crawler.py` for automated content gathering.

**External Interfaces**
   The modules in `app/utility` interact with a variety of external systems and internal components:
   *   **Operating System:** `app/utility/shell.py` and `app/utility/filesystem.py` directly interact with the underlying operating system for command execution and file system management.
   *   **Docker:** `app/utility/shell.py` is used by `app/systems/manage/service.py` to interact with Docker for container management.
   *   **Git Repositories:** `app/utility/git.py` interacts with remote Git repositories for version control operations.
   *   **SSH Servers:** `app/utility/ssh.py` establishes connections and executes commands on remote SSH servers.
   *   **Web Services:** `app/utility/request.py`, `app/utility/web.py`, `app/utility/crawler.py`, and `app/utility/browser.py` interact with external web servers to fetch and parse content.
   *   **Redis:** `app/utility/mutex.py` uses Redis for distributed locking and state management.
   *   **NVIDIA Drivers:** `app/utility/nvidia.py` communicates with NVIDIA GPU drivers to retrieve device information.
   *   **Django Framework:** Many modules, such as `app/utility/time.py` and `app/utility/terminal.py`, leverage Django's settings and timezone configurations.
   *   **Databases:** `app/utility/query.py` is designed to work with Django querysets, implying interaction with the project's configured database.
