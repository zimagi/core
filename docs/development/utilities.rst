Utility Functions
=================

The `app/utility/` directory provides a comprehensive collection of reusable utility functions and classes that support various functionalities across the Zimagi application.

Overview
--------
These utilities cover a wide range of operations, from data manipulation and file system interactions to external service integrations and parallel processing. They are designed to promote code reuse, consistency, and efficiency.

Utility Categories
------------------

*   **Data Manipulation (`app/utility/data.py`)**:
    *   `Collection`, `RecursiveCollection`: Flexible dictionary-like objects with attribute access.
    *   `ensure_list`, `deep_merge`, `flatten_dict`: Functions for list and dictionary manipulation.
    *   `env_value`, `normalize_value`: Environment variable and value normalization.
    *   `dump_json`, `load_json`: JSON serialization/deserialization.
    *   `dependents`: Collects dependencies.

*   **File System Operations (`app/utility/filesystem.py`)**:
    *   `FileSystem`: Base class for file system interactions.
    *   `load_json`, `save_file`, `create_dir`, `remove_dir`: Functions for file and directory management.

*   **Terminal Output (`app/utility/terminal.py`, `app/utility/display.py`)**:
    *   `TerminalMixin`: For colored text and formatted messages.
    *   `colorize_data`, `format_table`, `format_list`: Functions for structured terminal output.
    *   `format_exception_info`: Formats exception details.

*   **Web Operations (`app/utility/request.py`, `app/utility/web.py`, `app/utility/crawler.py`, `app/utility/browser.py`)**:
    *   `request_legacy_session`, `validate_url`: HTTP requests and URL validation.
    *   `WebParser`: Parses web pages and extracts text.
    *   `WebCrawler`: Implements web crawling.
    *   `Browser`: High-level interface for Selenium browser automation.

*   **Git & SSH Operations (`app/utility/git.py`, `app/utility/ssh.py`)**:
    *   `Git`: Pythonic interface for Git repository operations (`pygit2`).
    *   `SSH`: Robust client for SSH connections and remote command execution (`paramiko`).

*   **Time Utilities (`app/utility/time.py`)**:
    *   `Time`: Comprehensive utilities for time and date manipulation, including timezone support.

*   **Parallel Execution (`app/utility/parallel.py`)**:
    *   `ThreadPool`, `Parallel`: Utilities for executing tasks in parallel using threads.

*   **NVIDIA GPU Management (`app/utility/nvidia.py`)**:
    *   `Nvidia`: Interface for interacting with NVIDIA GPU devices (`pynvml`).

*   **Distributed Locking (`app/utility/mutex.py`)**:
    *   `Mutex`, `check_mutex`: Implements distributed locking using Redis to prevent race conditions.

*   **Dynamic Python (`app/utility/python.py`)**:
    *   `create_module`, `create_class`: Dynamic Python module and class creation.
    *   `PythonParser`: Parses string values referencing Python module attributes.

*   **Project & Temporary Files (`app/utility/project.py`, `app/utility/temp.py`)**:
    *   `ProjectDir`: Manages project-specific directories.
    *   `TempDir`: Manages temporary directories and files.

*   **Runtime Configuration (`app/utility/runtime.py`)**:
    *   `Runtime`: Manages thread-safe runtime configuration and settings.

*   **Validation (`app/utility/validation.py`)**:
    *   `TypeValidator`, `validate_flattened_dict`: Tools for validating data types and filtering dictionaries.

*   **DataFrame Operations (`app/utility/dataframe.py`)**:
    *   `merge`, `concatenate`, `get_csv_file_name`: Functions for pandas DataFrame manipulation.

How to Use
----------
These utilities are typically imported and used by other parts of the Zimagi application, such as commands, plugins, and core system components. For example, a command might use `utility.filesystem.load_json` to read a configuration file, or a plugin might use `utility.data.deep_merge` to combine data.
