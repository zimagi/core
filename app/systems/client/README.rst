=====================================================
README for Directory: app/systems/client
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the client-side command-line interface (CLI) for the Zimagi platform, providing the entry point and core logic for user interaction with the system's various functionalities. It defines how commands are parsed, executed, and how the application interacts with the Zimagi backend services.

**Key Functionality**
   *  Command-line argument parsing and validation.
   *  Routing of CLI commands to appropriate backend actions.
   *  Management of interactive chat sessions.
   *  Display of command output and system messages.

Dependencies
-------------------------

*   **Django:** Used for configuration management and command parsing utilities.
*   **Textual:** A TUI (Text User Interface) framework for building interactive command-line applications, specifically used for the chat interface.
*   **Pyperclip:** A cross-platform clipboard module used for copy/paste functionality in the chat widget.
*   **Rich:** A Python library for rich text and beautiful formatting in the terminal, used for rendering markdown and styled output.
*   **Docker SDK for Python:** Used by the `ManagerServiceMixin` for interacting with Docker containers, images, networks, and volumes.

File Structure and Descriptions
-------------------------------

**app/systems/client/cli**
     **Role:** This subdirectory contains the core implementation of the Zimagi command-line interface, including command parsing, execution, and interactive components like the chat application.
     **Detailed Description:** This directory is the heart of the Zimagi client. It defines the structure for how commands are registered, how arguments are handled, and how the client communicates with the Zimagi command and data APIs. It includes modules for base command definitions, argument parsing, error handling, and specific command implementations like `action`, `chat`, `help`, `schema`, `test`, and `version`. The interactive chat application, built with Textual, also resides here, providing a rich user experience for real-time communication with the Zimagi system.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `zimagi` bash script (not in this directory) acts as the initial entry point, setting up the environment and invoking the Python client.
   2.  `app/systems/client/cli/client.py` is the main entry point for the Python CLI. It initializes the command index and parses the initial command-line arguments.
   3.  `app/systems/client/cli/index.py` is responsible for finding and instantiating the correct command handler based on the parsed arguments. It also manages the command and data API clients.
   4.  Commands inherit from `app/systems/client/cli/commands/base.py`, which provides common argument parsing and execution logic.
   5.  Specific command implementations (e.g., `app/systems/client/cli/commands/action.py`, `app/systems/client/cli/commands/chat.py`) define the unique behavior for each command.
   6.  For interactive features like chat, `app/systems/client/cli/chat/app.py` takes over, managing the Textual UI and real-time message handling.

**External Interfaces**
   *   **Zimagi Command API:** The CLI communicates extensively with the Zimagi Command API (exposed via `command-api` Docker service) to execute actions and retrieve command schemas. This interaction is managed through `zimagi.command.client.Client`.
   *   **Zimagi Data API:** The CLI interacts with the Zimagi Data API (exposed via `data-api` Docker service) for data retrieval and manipulation, particularly for managing chat sessions and messages. This is handled by `zimagi.data.client.Client`.
   *   **Docker Daemon:** The `ManagerServiceMixin` (from `app/systems/manage/service.py`) directly interacts with the Docker daemon via the Docker SDK to manage Zimagi services (containers, images, networks, volumes).
   *   **Operating System Shell:** Commands can execute external shell commands, for example, to launch a shell inside a Docker container (`docker exec`).
