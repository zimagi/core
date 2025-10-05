=====================================================
README for Directory: app/spec
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for defining the declarative specifications and configurations that govern the behavior, structure, and interactions of various core components within the Zimagi application. These YAML files act as blueprints for commands, data models, plugins, services, and other system elements, enabling a highly modular, extensible, and dynamically configurable platform.

**Key Functionality**
   *  **Command Definition:** Specifies the structure, parameters, access control, and execution characteristics of all command-line interface (CLI) and API commands.
   *  **Data Model Definition:** Outlines the schema, relationships, roles, and behaviors of all data entities, forming the blueprint for data management and persistence.
   *  **Plugin Configuration:** Defines the interfaces, requirements, options, and available providers for various plugin types, enabling extensible functionalities.
   *  **Service Orchestration:** Configures the deployment, environment, and dependencies of Docker-based services and workers.
   *  **System-wide Settings:** Manages user defaults, encryption schemes, message channels, and role-based access control.


Dependencies
-------------------------

The files in this directory are primarily declarative YAML specifications. They are parsed and interpreted by the Zimagi core system, which is built with Python and relies on the Django framework. The specifications define how Zimagi interacts with:

*   **PostgreSQL:** For persistent storage of data models defined in `data` specifications.
*   **Redis:** For caching, messaging, and task queuing, often configured implicitly through service definitions.
*   **Qdrant:** For vector database operations, as specified in `qdrant` related configurations.
*   **Docker/Docker Compose:** For container orchestration and service deployment, heavily influenced by `services.yml` and `workers.yml`.
*   **Python Libraries:** Internal Zimagi Python modules and various third-party libraries (e.g., `docker` for container management, `pandas` for data processing) are utilized by the application to implement the behaviors defined in these specifications.


File Structure and Descriptions
-------------------------------

**app/spec/base**
     **Role:** Defines foundational, reusable base specifications for commands and data models.
     **Detailed Description:** This subdirectory contains core YAML files (`command.yml`, `data.yml`) that establish the fundamental structure and common properties inherited by other command and data definitions throughout the application. It sets up base command types, their default permissions, and foundational data resource types like `name_resource` and `id_resource`, including their basic fields and metadata. These base definitions are critical for maintaining consistency and extensibility across the system.

**app/spec/data**
     **Role:** Specifies the data models and their associated metadata for various application entities.
     **Detailed Description:** This subdirectory holds YAML files that define the schema, relationships, roles, and behaviors of all data entities within the Zimagi application. Each file (e.g., `user.yml`, `config.yml`, `memory.yml`) details fields, data types, foreign key relationships, role-based access control (RBAC), and dynamic field configurations. These definitions are used by the application's ORM to generate database schemas and manage data persistence and validation.

**app/spec/plugins**
     **Role:** Defines the specifications and configurations for various plugin types.
     **Detailed Description:** This subdirectory contains YAML files that outline the structure, interfaces, requirements, options, and available providers for different plugin categories (e.g., `encoder.yml`, `language_model.yml`, `data_processor.yml`). These specifications enable a modular and extensible system architecture by defining how external functionalities can be integrated and configured, such as text encoding, language model interactions, or data transformations.

**app/spec/commands**
     **Role:** Defines the command-line interface (CLI) and API specifications for various functionalities.
     **Detailed Description:** This subdirectory houses YAML files that specify the structure, parameters, and underlying base functionalities for all commands available in the Zimagi system (e.g., `module.yml`, `ai.yml`, `database.yml`). Each command definition includes details on arguments, options, flags, parsing rules, access control, and prioritization, serving as the blueprint for how users and other services interact with the application.

**app/spec/mixins**
     **Role:** Defines reusable "mixins" for commands, plugins, and data models.
     **Detailed Description:** This subdirectory contains YAML files that specify common parameters, options, and metadata structures that can be inherited and extended by various components. Mixins (e.g., `command.yml`, `plugin.yml`, `data.yml`) promote consistency and reduce redundancy by providing reusable sets of configurations for functionalities like SSH connections, logging, database operations, or common data model fields.

**app/spec/users.yml**
     **Role:** Configures default settings and user-specific overrides for AI-related functionalities and user groups.
     **Detailed Description:** This file defines `user_defaults_ai` which sets common configurations for AI features like language models, text splitters, and encoders, including their providers and options. It also lists specific users (e.g., `admin`, `dsv3`, `dsr1`) and assigns them to groups, potentially overriding default AI settings for individual users, thereby managing user-specific AI experiences and permissions.

**app/spec/encryption.yml**
     **Role:** Defines the encryption schemes and providers used for securing various data types within the application.
     **Detailed Description:** This file specifies how different types of data, such as user API keys or command/data API communications, are encrypted. It maps specific encryption contexts (e.g., `user_api_key`, `command_api`) to encryption plugin providers (e.g., `aes256`, `aes256_user`), ensuring that sensitive information is handled with appropriate cryptographic measures.

**app/spec/workers.yml**
     **Role:** Defines the default worker configurations and specific worker types for background task processing.
     **Detailed Description:** This file establishes a `_default_worker` template with common settings for Docker image, runtime, Kubernetes resource limits (CPU, memory), and environment variables. It then defines various worker types (e.g., `qdrant`, `encoder`, `language_model`, `file_parser`) that inherit from this default, allowing for specialized background processing capabilities within the application's distributed task queue.

**app/spec/mcp.yml**
     **Role:** Configures the Management Control Plane (MCP) connections for external services.
     **Detailed Description:** This file defines the connection details for external Management Control Plane services, such as GitHub. It specifies the URL and authentication token (e.g., `GITHUB_TOKEN`) required to interact with these external MCPs, enabling the Zimagi application to integrate with and manage resources on platforms like GitHub.

**app/spec/channels.yml**
     **Role:** Defines the communication channels used for inter-service messaging and event notification.
     **Detailed Description:** This file specifies various message channels (e.g., `data:save:{data_type}`, `encoder:save`, `language_model:generate`, `chat:message`) along with their descriptions, associated user groups, and the expected message schema. These definitions are crucial for enabling asynchronous communication, event-driven architectures, and real-time notifications between different components and agents within the Zimagi system.

**app/spec/roles.yml**
     **Role:** Defines the role-based access control (RBAC) roles available within the Zimagi application.
     **Detailed Description:** This file lists and describes all predefined user roles (e.g., `admin`, `db-admin`, `chat-user`, `ai-user`). Each role is given a clear description of the privileges it grants, which are then referenced throughout the application's data models and command definitions to enforce granular access control and security policies.

**app/spec/services.yml**
     **Role:** Defines templates and configurations for Docker-based services and workers.
     **Detailed Description:** This file provides reusable templates for Docker volumes (`_base-volumes`, `_local-volumes`, `_prod-volumes`) and a base `_zimagi` service configuration, including image, runtime, network, and environment settings. It then defines specific worker and agent service configurations that inherit from these templates, detailing their entry points and volume mounts, which are used for deploying and managing containerized application components.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The files within `app/spec` are primarily declarative configuration files. Their "execution flow" is indirect, as they are parsed and interpreted by the Zimagi core application during initialization and runtime.
   1.  **Application Startup:** Upon startup, the Zimagi framework loads and parses all YAML files in `app/spec`.
   2.  **Schema Generation:** Definitions in `app/spec/data` are used to dynamically generate or update database schemas and Django models.
   3.  **Command Registration:** `app/spec/commands` and `app/spec/mixins/command.yml` define the available CLI and API commands, which are then registered with the command parsing engine.
   4.  **Plugin Loading:** `app/spec/plugins` and `app/spec/mixins/plugin.yml` inform the system about available plugin types, their interfaces, and providers, allowing for dynamic loading and instantiation.
   5.  **Service Deployment:** `app/spec/services.yml` and `app/spec/workers.yml` guide the deployment and configuration of Docker containers for various services (e.g., APIs, controller, scheduler) and background workers.
   6.  **Runtime Configuration:** `app/spec/users.yml`, `app/spec/encryption.yml`, `app/spec/mcp.yml`, `app/spec/channels.yml`, and `app/spec/roles.yml` provide system-wide and user-specific configurations that influence runtime behavior, security, and communication.
   7.  **Component Interaction:** When a user or an internal process invokes a command, interacts with a data model, or utilizes a plugin, the application's core logic consults these parsed specifications to validate requests, enforce permissions, and execute the defined behaviors.

**External Interfaces**
   The configurations defined in `app/spec` dictate how the Zimagi application interacts with a variety of external and internal systems:

   *   **Databases (PostgreSQL, Redis, Qdrant):** Data models (`app/spec/data`) are translated into database schemas. Commands (`app/spec/commands/database.yml`, `app/spec/commands/qdrant.yml`) directly manage these data stores.
   *   **Container Runtimes (Docker, Kubernetes):** Service and worker definitions (`app/spec/services.yml`, `app/spec/workers.yml`) orchestrate Docker containers and can be extended for Kubernetes deployments.
   *   **External APIs/Services:** MCP configurations (`app/spec/mcp.yml`) define connections to external management planes (e.g., GitHub). Plugin specifications (`app/spec/plugins`) enable integration with external language models, search engines, and document sources.
   *   **Message Queues/Brokers:** Channel definitions (`app/spec/channels.yml`) establish the structure for inter-service communication, often implemented via message brokers like Redis.
   *   **Operating System:** Task plugins (`app/spec/plugins/task.yml`) can execute commands or scripts on the underlying operating system or remote machines via SSH.
   *   **User Authentication/Authorization Systems:** Role definitions (`app/spec/roles.yml`) and user configurations (`app/spec/users.yml`) integrate with the application's authentication and authorization mechanisms.
