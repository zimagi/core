=====================================================
README for Directory: app/tasks
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains YAML-based task definitions that orchestrate various operations within the Zimagi platform. These tasks are designed to be executed by the Zimagi scheduler and controller services, enabling automated workflows, system maintenance, and integration with core functionalities.

**Key Functionality**
   *   Defining reusable command-line and script-based tasks.
   *   Orchestrating database migrations and schema management.
   *   Providing utility functions for system health checks and delays.
   *   Facilitating inter-service communication and dependency management.

Dependencies
-------------------------

The tasks defined in this directory primarily rely on the Zimagi platform's internal services and command-line interface. They are executed within the Dockerized environment managed by Docker Compose. Specific dependencies include:

*   **Zimagi Command-Line Interface (CLI):** Tasks often invoke `zimagi` commands for core operations.
*   **Docker:** The underlying containerization platform for service execution.
*   **Bash:** For executing shell scripts and commands within the container environment.
*   **Curl:** Used in health checks for HTTP/HTTPS endpoints.

File Structure and Descriptions
-------------------------------

**app/tasks/utility.yml**
     **Role:** Defines a collection of general-purpose utility tasks for system operations and health checks.
     **Detailed Description:** This file contains task definitions that provide basic functionalities such as echoing text, performing equality checks, introducing delays (`sleep`), and waiting for hosts or HTTP/HTTPS endpoints to become available. These tasks are crucial for scripting robust workflows, especially in CI/CD pipelines or during service startup sequences, by ensuring dependencies are met before proceeding.

**app/tasks/zimagi.yml**
     **Role:** Contains task definitions specifically related to Zimagi's database migration and schema management.
     **Detailed Description:** This file defines tasks that interact with Zimagi's database layer. It includes tasks for testing database migrations (`test_migrations`), building new migration files (`build_migrations`), and applying pending migrations to the database (`migrate`). These tasks are fundamental for managing the evolution of the application's data schema and ensuring consistency across different environments.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The tasks defined in `app/tasks` are not directly executed as standalone applications. Instead, they are invoked by the Zimagi `scheduler` or `controller` services. When a task is triggered (either manually or on a schedule), the `scheduler` or `controller` reads the YAML definition from files like `utility.yml` or `zimagi.yml`. Based on the `provider` specified in the task (e.g., `command` or `script`), the service then executes the corresponding command-line instruction or shell script within the appropriate Docker container. For instance, a `zimagi migrate` command defined in `zimagi.yml` would be executed by the `controller` service, which has access to the Zimagi CLI and the database.

**External Interfaces**
   The tasks in this directory primarily interact with the following external components:

*   **Zimagi Database (PostgreSQL):** Tasks defined in `zimagi.yml` directly interact with the PostgreSQL database for schema management and migrations.
*   **Zimagi Services (command-api, data-api, mcp-api, etc.):** Utility tasks, particularly those involving `wait-http` or `wait-https`, perform health checks against the exposed ports of various Zimagi API services.
*   **Docker Daemon:** The execution of all tasks ultimately relies on the Docker daemon to manage and run containers.
*   **Filesystem:** Tasks may read from or write to the shared filesystem within the Docker containers, for example, when scripts are executed.
