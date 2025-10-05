Command Line Interface (CLI)
============================

The Zimagi Command Line Interface (CLI) is the primary way users interact with the platform. It provides a rich set of commands for managing all aspects of Zimagi.

Overview
--------
The CLI is accessed via the `zimagi` executable script. It supports a hierarchical command structure, argument parsing, and formatted output.

Accessing the CLI
-----------------
After installation, you can run Zimagi commands directly from your terminal:

.. code-block:: bash

    zimagi [command] [subcommand] [arguments] [options]

Getting Help
------------
*   **General Help**: To see a list of all top-level commands:

    .. code-block:: bash

        zimagi --help

*   **Command-Specific Help**: To get help on a particular command and its subcommands:

    .. code-block:: bash

        zimagi module --help

    Or for a subcommand:

    .. code-block:: bash

        zimagi module create --help

Command Structure
-----------------
Zimagi commands follow a `[category] [action]` or `[category] [resource] [action]` pattern.

Examples:

*   `zimagi platform info`: Get general platform information.
*   `zimagi module create my-module`: Create a new module.
*   `zimagi config save my-setting --value "test"`: Save a configuration setting.

Key CLI Features
----------------
*   **Argument Parsing**: Robust parsing of flags, variables, and fields.
*   **Dynamic Command Generation**: Commands are dynamically generated based on specifications.
*   **Formatted Output**: Data is presented in human-readable tables, lists, and messages.
*   **Interactive Chat**: Engage in real-time chat sessions with AI agents.
*   **Error Reporting**: Clear and concise error messages with debugging information.

Core CLI Components (`app/systems/client/cli`)
----------------------------------------------
*   **`app/systems/client/cli/client.py`**: Main entry point for the Python CLI.
*   **`app/systems/client/cli/index.py`**: Manages command discovery and instantiation.
*   **`app/systems/client/cli/commands/base.py`**: Base class for CLI commands.
*   **`app/systems/client/cli/chat/app.py`**: Interactive chat application.

For a comprehensive list of commands and their usage, refer to the :doc:`api_commands` section and the `app/help/en` directory for detailed descriptions.
