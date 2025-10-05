=====================================================
README for Directory: app/spec/commands
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for defining the command-line interface (CLI) and API specifications for various functionalities within the Zimagi application. Each YAML file in this directory corresponds to a specific command or a group of related commands, outlining their structure, parameters, and underlying base functionalities. This organization allows for a clear, declarative definition of how different parts of the system can be interacted with, both by human users via the CLI and programmatically through the API.

**Key Functionality**
   *   **Command Definition:** Defines the structure and behavior of all available commands in the Zimagi system.
   *   **Parameter Specification:** Details the arguments, options, and flags that each command accepts, including their types, default values, and help text.
   *   **API Integration:** Provides the necessary metadata for exposing CLI commands as API endpoints, ensuring consistent behavior across interfaces.
   *   **Module and Service Orchestration:** Specifies how commands interact with various modules, agents, and services within the Zimagi ecosystem.
   *   **Access Control and Prioritization:** Includes definitions for command priority and access control mechanisms, such as allowed user groups.


Dependencies
-------------------------

The files in this directory are primarily configuration files written in YAML. They are parsed and interpreted by the core Zimagi application, which is built with Python. Therefore, the primary dependency is the Zimagi application's command parsing and execution engine. There are no direct external library dependencies for these YAML files themselves, but the functionalities they define often rely on:

*   **Python 3.x:** The runtime environment for the Zimagi application.
*   **Django Framework:** Used by the Zimagi application for backend services and potentially for managing command definitions.
*   **Docker/Docker Compose:** Many commands relate to service management and container orchestration, implying a dependency on Docker for execution.


File Structure and Descriptions
-------------------------------

**app/spec/commands/database.yml**
     **Role:** Defines commands related to database management, including snapshotting, backup, restore, and cleaning operations.
     **Detailed Description:** This file specifies the structure for database-related commands. It includes definitions for `snapshots`, `backup`, `restore`, and `clean` operations. Each command outlines its priority, its base functionality (`db`), and any specific parameters it accepts, such as `snapshot_name` for restore or `keep_num` for cleaning old backups. It also includes confirmation prompts for destructive operations like `restore`.

**app/spec/commands/group.yml**
     **Role:** Defines commands for managing user groups and their relationships.
     **Detailed Description:** This file specifies the `group` command, which acts as a resource for managing user groups. It includes a `children` section for managing child groups, with parameters like `group_child_keys` to specify one or more child group keys. It also defines parsing rules for `group_key` and `group_provider_name`.

**app/spec/commands/config.yml**
     **Role:** Defines commands for managing application configuration settings.
     **Detailed Description:** This file defines the `config` command, which serves as a resource for managing configuration entries. It specifies options for saving configuration values, including their type (`config_value_type`) and the value itself (`config_value`). This allows for dynamic and type-aware configuration management within the Zimagi system.

**app/spec/commands/host.yml**
     **Role:** Defines commands for managing host-related information and operations.
     **Detailed Description:** This file defines the `host` command, which acts as a resource for managing host entities within the Zimagi environment. It sets the base name and priority for host-related operations, providing a foundational definition for interacting with host data.

**app/spec/commands/calculate.yml**
     **Role:** Defines commands for executing and managing various calculation specifications.
     **Detailed Description:** This file specifies the `calculate` command, which enables the execution of predefined calculation specifications. It includes parameters such as `field_values` for passing data to calculation providers, `calculation_names` and `tags` for filtering calculations, and flags like `ignore_requirements`, `show_spec`, `disable_save`, and `reset` for controlling execution and display behavior.

**app/spec/commands/user.yml**
     **Role:** Defines commands for managing user accounts and related operations, such as rotating user keys.
     **Detailed Description:** This file defines the `user` command, which serves as a resource for managing user accounts. It includes a `rotate` subcommand specifically for rotating user keys, requiring a `user_key` for identification. This ensures secure management of user credentials.

**app/spec/commands/import.yml**
     **Role:** Defines commands for importing data based on specified import specifications.
     **Detailed Description:** This file specifies the `import` command, designed for handling data import processes. It provides parameters like `field_values` for passing data to import providers, `import_names` and `tags` for selecting specific import specifications, and flags such as `ignore_requirements`, `show_spec`, and `disable_save` to control the import behavior and display options.

**app/spec/commands/template.yml**
     **Role:** Defines commands for generating new modules from templates.
     **Detailed Description:** This file defines the `template` command, specifically the `generate` subcommand, which is used to create new modules based on existing templates. It includes parameters for specifying the `base` module type, `priority`, and parsing options for `module_key`, `module_template`, `template_fields`, and `display_only`.

**app/spec/commands/schedule.yml**
     **Role:** Defines commands for managing scheduled tasks within the system.
     **Detailed Description:** This file defines the `schedule` command, which acts as a resource for managing `scheduled_task` entities. It sets the base name and priority for scheduling operations, providing a foundational definition for interacting with scheduled tasks.

**app/spec/commands/chat.yml**
     **Role:** Defines commands for chat-based interactions, including listening for messages and sending responses, often used by AI agents.
     **Detailed Description:** This file defines the `chat` command, which includes `listen` and `send` subcommands. The `listen` command allows the system to monitor chat channels for messages, with parameters for `chat_channel`, `listen_timeout`, and `listen_state_key`. The `send` command enables sending messages to chat channels, with `chat_channel`, `chat_name`, `chat_text`, and `disable_save` parameters. It also includes detailed `_chat_directive` definitions for AI agents, outlining their core mission, operational principles, communication protocols, sensors, memory management, and available tools like `chat:send@local`, `web:search@local`, and `web:fetch@local`.

**app/spec/commands/library.yml**
     **Role:** Defines commands for interacting with various libraries, including file and web search/fetch/upload operations.
     **Detailed Description:** This file defines `file` and `web` commands, both utilizing `mcp` (Management Control Plane) and `library` mixins. The `file` command includes `search`, `download`, and `upload` subcommands for managing files within a library, with parameters like `library_name`, `search_text`, `max_results`, `file_path`, and `file_content`. The `web` command provides `search` and `fetch` functionalities for web resources, with parameters such as `search_provider`, `search_text`, `max_results`, `file_url`, `library_name`, and `file_path`.

**app/spec/commands/service.yml**
     **Role:** Defines commands for managing system services, including scaling, locking, and monitoring.
     **Detailed Description:** This file defines commands for `scale` and `service` management. The `scale` command allows for adjusting the number of agent services, with parameters for `agent_name` and `agent_count`. The `service` command includes subcommands for `lock` (with `set` and `clear` operations for service keys and expiration), `wait` (for service keys with timeout and interval options), and `follow` (for monitoring service communication channels).

**app/spec/commands/mcp.yml**
     **Role:** Defines commands related to the Management Control Plane (MCP), specifically for managing MCP tools.
     **Detailed Description:** This file defines the `tools` subcommand under the `mcp` command. It allows for managing MCP tools, with parameters such as `tool_user` to filter by user and `servers` to filter by MCP server names. This command is designed for administrative interaction with the MCP.

**app/spec/commands/notification.yml**
     **Role:** Defines commands for managing system notifications, including saving, removing, and clearing notifications.
     **Detailed Description:** This file defines the `notification` command, which acts as a resource for managing notification entities. It includes subcommands for `save`, `remove`, and `clear` notifications. Parameters like `group_provider_name`, `notify_failure`, `notify_command`, and `notify_groups` allow for fine-grained control over notification behavior and targeting.

**app/spec/commands/module.yml**
     **Role:** Defines commands for managing application modules, including task execution, module lifecycle (run, destroy), and module creation/installation.
     **Detailed Description:** This file defines a comprehensive set of commands for module management. The `task` command allows for executing module-specific tasks with `module_key`, `task_key`, and `task_fields`. The `run` and `destroy` commands manage the lifecycle of modules and profiles, with options for `display_only`, `test`, `ignore_missing`, `profile_components`, `module_key`, `profile_key`, and `profile_config_fields`. The `module` command itself acts as a resource for module entities, with subcommands for `create` (specifying `module_provider_name` and `module_template`), `add` (for remote modules), `init` (for initializing data types), and `install` (for building module images with a `tag`).

**app/spec/commands/ai.yml**
     **Role:** Defines commands for artificial intelligence functionalities, specifically for text encoding and language model interaction.
     **Detailed Description:** This file defines `encode` and `ask` commands under the `ai` umbrella. The `encode` command is used to generate embeddings from `source_text`, with an option to `display_embeddings`. The `ask` command facilitates interaction with language models, taking `instruction_text` and optional `model_options` to guide the language model's response.

**app/spec/commands/agents.yml**
     **Role:** Defines various types of agents within the system, such as archiver, qdrant, encoder, language model, and file parser agents.
     **Detailed Description:** This file defines several agent types under the `agent` command. These include `archiver` (with `scaling_event` mixin), `qdrant` (with `qdrant` mixin and `qdrant` worker type), `encoder` (with `qdrant` mixin and `encoder` worker type), `language_model` (with `language_model` worker type), and `file_parser` (with `file_parser` worker type). These definitions specify the base agent functionality and any specific mixins or worker types associated with each agent.

**app/spec/commands/dataset.yml**
     **Role:** Defines commands for managing datasets within the application.
     **Detailed Description:** This file defines the `data` command, which acts as a resource for managing `dataset` entities. It sets the base name and priority for dataset operations, providing a foundational definition for interacting with data collections.

**app/spec/commands/controller.yml**
     **Role:** Defines commands related to the system's controller, specifically for agent control.
     **Detailed Description:** This file defines the `agent` subcommand under the `controller` command. This indicates that the controller has capabilities to manage or interact with agents, providing a specific entry point for agent control operations.

**app/spec/commands/state.yml**
     **Role:** Defines commands for managing the application's state, including saving specific state fields.
     **Detailed Description:** This file defines the `state` command, which acts as a resource for managing application state. It includes options for saving specific state fields, such as `state_value`, allowing for persistent storage and retrieval of application state.

**app/spec/commands/platform.yml**
     **Role:** Defines core platform-level commands such as displaying information, versioning, building, and testing.
     **Detailed Description:** This file defines fundamental platform commands. `info` provides general system information. `version` displays the application version. `build` allows for building modules, with parameters for `build_modules`. `test` facilitates running various types of tests, with options for `test_types`, `test_tags`, and `test_exclude_tags`. These commands are crucial for system introspection, development, and quality assurance.

**app/spec/commands/scaling.yml**
     **Role:** Defines commands related to scaling events and their management.
     **Detailed Description:** This file defines the `scaling` command, which acts as a resource for managing `scaling_event` entities. It sets the base name and priority for scaling operations and explicitly disallows direct access, update, or removal of scaling events through this command, suggesting they are managed internally or through other mechanisms.

**app/spec/commands/qdrant.yml**
     **Role:** Defines commands for interacting with the Qdrant vector database, including listing, snapshotting, removing, cleaning, and restoring collections.
     **Detailed Description:** This file defines commands for `qdrant` administration. It includes `list` and `snapshot` for managing collections, `remove` for deleting collections or snapshots (with confirmation), `clean` for removing old snapshots (with a `keep_num` parameter), and `restore` for restoring collections from snapshots. These commands provide comprehensive management capabilities for the Qdrant vector database.

**app/spec/commands/log.yml**
     **Role:** Defines commands for managing system logs, including getting, aborting, rerunning, and cleaning log entries.
     **Detailed Description:** This file defines the `log` command, which acts as a resource for managing log entries. It includes subcommands for `get` (retrieving logs by `log_key` with `poll_interval`), `abort` (stopping log processes by `log_keys`), `rerun` (re-executing log processes by `log_keys`), and `clean` (removing old logs based on `log_days` and `log_message_days`). It also restricts direct access to log entries.

**app/spec/commands/browser.yml**
     **Role:** Defines commands for browser-related operations, such as fetching web pages, and for browser-based agents.
     **Detailed Description:** This file defines the `browser` command, which includes a primary command for fetching a URL (`url`) to retrieve JavaScript-rendered web pages. It also defines an `agent` subcommand for a `browser` agent, indicating that browser-based automation or data extraction can be performed by dedicated agents.

**app/spec/commands/cache.yml**
     **Role:** Defines commands for managing the application's cache, specifically for clearing cache entries.
     **Detailed Description:** This file defines the `cache` command, which includes a `clear` subcommand. This command is used to invalidate or remove cached data, ensuring that the application can retrieve fresh information when needed.

**app/spec/commands/gpu.yml**
     **Role:** Defines commands related to GPU management and utilization.
     **Detailed Description:** This file defines the `gpu` command, which serves as a high-priority entry point for GPU-related operations. While the specific subcommands are not detailed here, its presence indicates that the system has capabilities for interacting with and managing GPU resources.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow within `app/spec/commands` is primarily declarative. When a user or an API call initiates a command (e.g., `zimagi module create`), the Zimagi application's command parsing engine first consults these YAML files.
   1.  The engine identifies the relevant YAML file (e.g., `module.yml`) based on the command invoked.
   2.  It then navigates the YAML structure to find the specific subcommand (e.g., `create` under `module`).
   3.  The `base` field in the command definition (e.g., `base: module` in `module.yml`) points to the underlying Python module or class that implements the actual logic for that command.
   4.  Parameters defined in the YAML (e.g., `module_provider_name`, `module_template` in `template.yml`) are parsed and validated against the specified types and options.
   5.  The `parse` section dictates how command-line arguments or API payload fields are mapped to the internal parameters of the command's implementation.
   6.  Flags like `confirm` (e.g., in `database.yml` for `restore`) trigger interactive prompts or require explicit confirmation.
   7.  `priority` fields (e.g., in `module.yml`, `database.yml`) can influence the order of command execution or display in help menus.
   8.  For agent-related commands (e.g., `chat.yml`, `agents.yml`), the definitions guide the instantiation and behavior of autonomous agents, including their sensors, rules, and tool usage.

**External Interfaces**
   The commands defined in this directory interact with various external and internal components:

   *   **Databases (PostgreSQL, Redis, Qdrant):** Commands in `database.yml` and `qdrant.yml` directly manage these data stores. Other commands implicitly interact with them for data persistence and retrieval.
   *   **Docker/Container Runtime:** Many commands, particularly those related to `service.yml`, `module.yml` (for image building), and `agents.yml`, orchestrate Docker containers and services.
   *   **Web Services/APIs:** Commands in `library.yml` (for `web:search`, `web:fetch`) and `browser.yml` interact with external web services. The `chat.yml` also defines tools like `web:search@local` and `web:fetch@local` for agents to use.
   *   **File System:** Commands in `library.yml` (for `file:search`, `file:download`, `file:upload`) interact with the local or networked file system.
   *   **Internal Zimagi Modules and Agents:** Commands in `module.yml` trigger the execution of specific module functionalities, while `agents.yml` and `chat.yml` define the behavior and tools available to various autonomous agents within the Zimagi ecosystem.
   *   **Management Control Plane (MCP):** Commands in `mcp.yml` and some in `library.yml` (e.g., `base: mcp`) indicate interaction with a central management component for distributed operations.
   *   **Notification Systems:** `notification.yml` defines how the system interacts with notification providers to send alerts.
   *   **GPU Resources:** `gpu.yml` suggests interaction with underlying GPU hardware or drivers for accelerated computing tasks.
