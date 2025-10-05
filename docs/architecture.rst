Project Architecture and Modules
================================

The Zimagi codebase is organized into several key modules, each designed to manage specific functionalities of the platform. This section provides an overview of the main directories and their roles.

Source Modules (`app/`)
-----------------------
The `app/` directory serves as the root for the entire Zimagi application codebase. It encapsulates all core functionalities, configurations, scripts, and specifications necessary to build, run, test, and extend the Zimagi platform.

Key subdirectories within `app/`:

*   **`app/settings`**: Centralizes all application-wide settings and configurations.
*   **`app/tasks`**: Contains YAML-based task definitions for automated workflows.
*   **`app/data`**: Repository for all application data models, migrations, and foundational mixins.
*   **`app/spec`**: Central repository for declarative specifications and configurations (commands, data models, plugins).
*   **`app/scripts`**: Collection of shell scripts for managing and operating Zimagi services.
*   **`app/help`**: Central repository for all help documentation.
*   **`app/plugins`**: Central hub for all pluggable components (data processing, file parsing, encryption, etc.).
*   **`app/components`**: Houses core profile components for managing module resources.
*   **`app/commands`**: Central hub for all command-line interface (CLI) and API commands.
*   **`app/services`**: Central hub for all core Zimagi application services (APIs, Celery).
*   **`app/tests`**: Central hub for all automated tests.
*   **`app/systems`**: Defines and manages core functionalities and architectural components.
*   **`app/utility`**: Collection of reusable utility functions and classes.
*   **`app/templates`**: Central repository for all Jinja2 template files.
*   **`app/profiles`**: Defines and manages various operational profiles (scaling, testing).

Core API/Services
-----------------
The Zimagi platform exposes several core APIs and services:

*   **`app/systems/api`**: Defines and manages distinct API layers for commands, data, and the Model Context Protocol (MCP), handling authentication, authorization, encryption, routing, and schema generation.
*   **`app/services`**: Defines the configurations and entry points for these API services, along with background task processing via Celery.

Documentation (`docs/`)
----------------------
The `app/help/` directory serves as the central repository for all help documentation within the application. It organizes help content by language and command, providing descriptive overviews and detailed explanations for various functionalities. This structure ensures that both human users and AI models can easily access and understand the purpose and usage of different application commands and features.

SDKs (`sdk/`)
--------------
The `sdk/` directory serves as the central repository for all Software Development Kits (SDKs) related to the Zimagi platform.

*   **`sdk/python`**: Provides the foundational Python SDK for interacting with the Zimagi platform.
*   **`sdk/javascript`**: Provides the foundational JavaScript SDK for interacting with the Zimagi platform.

Reactor (`reactor/`)
-------------------
The `reactor/` directory serves as the core operational hub for the Zimagi application's reactor environment. It centralizes scripts and configurations essential for building, initializing, managing, and executing various components of the Zimagi system, including Docker images, services, and command-line operations.
