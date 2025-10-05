Developing Commands
===================

Commands are the primary way users and other services interact with the Zimagi platform, both via the Command Line Interface (CLI) and the API. This section guides you through developing new commands.

Overview
--------
Commands encapsulate specific operations, ranging from system management and configuration to AI interactions and data manipulation. They are dynamically generated and managed by the Zimagi framework.

Command Directory Structure (`app/commands`)
--------------------------------------------
The `app/commands/` directory serves as the central hub for all CLI and API commands. It contains subdirectories for different command categories:

*   **`app/commands/base`**: Foundational classes and patterns for all CLI commands and agent operations.
*   **`app/commands/cache`**: Manages application's caching mechanisms.
*   **`app/commands/notification`**: Manages command notification preferences.
*   **`app/commands/group`**: Manages user groups.
*   **`app/commands/chat`**: Encapsulates chat functionality.
*   **`app/commands/db`**: Manages database snapshots.
*   **`app/commands/qdrant`**: Manages Qdrant vector database instances.
*   **`app/commands/template`**: Handles template generation.
*   **`app/commands/log`**: Manages and interacts with system logs.
*   **`app/commands/module`**: Manages modules.
*   **`app/commands/file`**: Implements file operations.
*   **`app/commands/agent`**: Houses agent-based command implementations.
*   **`app/commands/web`**: Provides web-related functionalities.
*   **`app/commands/user`**: Manages user accounts.
*   **`app/commands/mixins`**: Reusable mixin classes that extend core command functionality.

Core Command System (`app/systems/commands`)
--------------------------------------------
The `app/systems/commands/` directory provides the robust and extensible framework for command management:

*   **`app/systems/commands/factory`**: Dynamically generates command classes for resource operations.
*   **`app/systems/commands/mixins`**: Reusable mixin classes for argument parsing, data querying, etc.
*   **`app/systems/commands/exec.py`**: Base class for all executable commands.
*   **`app/systems/commands/profile.py`**: Manages command profiles.
*   **`app/systems/commands/schema.py`**: Defines data structures for command schemas.
*   **`app/systems/commands/router.py`**: Implements a command router.
*   **`app/systems/commands/messages.py`**: Defines various message types for output.
*   **`app/systems/commands/processor.py`**: Generic framework for processing specifications.
*   **`app/systems/commands/help.py`**: Manages command descriptions and help text.
*   **`app/systems/commands/cli.py`**: Entry point for the command-line interface.
*   **`app/systems/commands/index.py`**: Central registry and factory for all commands.
*   **`app/systems/commands/calculator.py`**: Specialized processor for calculations.
*   **`app/systems/commands/agent.py`**: Base class for agent commands.
*   **`app/systems/commands/importer.py`**: Specialized processor for importing data.
*   **`app/systems/commands/action.py`**: Base class for action commands.
*   **`app/systems/commands/options.py`**: Manages command options.
*   **`app/systems/commands/args.py`**: Custom `argparse.Action` classes.
*   **`app/systems/commands/base.py`**: Foundational base class for all commands.
*   **`app/systems/commands/webhook.py`**: Base class for webhook commands.

Creating a New Command
----------------------
1.  **Choose a Category**: Decide which existing command category your new command belongs to, or create a new subdirectory in `app/commands/`.
2.  **Create a New File**: Inside the chosen directory, create a new Python file (e.g., `app/commands/my_category/my_command.py`).
3.  **Inherit from `Command`**: Your command class should inherit from `systems.commands.index.Command` (or a more specific base class like `systems.commands.action.ActionCommand` if it's a simple action).
4.  **Define `parse` Method**: Implement the `parse` method to define command-line arguments, options, and flags using `self.add_argument`.
5.  **Implement `exec` Method**: Implement the `exec` method to contain the core logic of your command. This is where you perform operations, interact with facades, or call other services.
6.  **Define Specification**: Create a corresponding entry in the `app/spec/commands/[category].yml` file to define your command's name, description, parameters, and any mixins it uses.

Example: Simple "Hello World" Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's create a command that prints a greeting.

1.  **File**: `app/commands/my_category/hello.py`

    .. code-block:: python

        from systems.commands.index import Command

        class Hello(Command):
            def parse(self):
                self.add_argument('name', type=str, help='Name to greet')

            def exec(self, name):
                self.success(f"Hello, {name}!")

2.  **Specification**: Add to `app/spec/commands/my_category.yml` (you might need to create this file)

    .. code-block:: yaml

        hello:
            name: hello
            description: Prints a greeting message.
            parameters:
                name:
                    type: string
                    help: The name to greet.

This example demonstrates the basic steps. Commands can be much more complex, leveraging mixins for database interaction, logging, and more.
