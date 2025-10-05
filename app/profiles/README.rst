=====================================================
README for Directory: app/profiles
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for defining and managing various operational profiles within the Zimagi platform. These profiles dictate how different services and tasks are configured, scaled, and executed, providing a flexible and declarative way to manage the application's lifecycle and testing scenarios.

**Key Functionality**
   Manages the scaling of core Zimagi services (archiver, qdrant, encoder, language_model, browser, file_parser). Defines comprehensive test suites for data management, task execution, dependency resolution, and failure handling. Configures display fields for various data types across the Zimagi API. Orchestrates database migrations and service startup/shutdown procedures.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   These profiles are designed to run within the Zimagi platform's Docker-based environment, leveraging Docker Compose for service orchestration. They are executed by the Zimagi CLI, which interacts with the Zimagi server components.

**Local Dependencies**
   The profiles rely on the core Zimagi framework and its command-line interface. They interact with Docker for container management and depend on the Zimagi server's various APIs (command, data, MCP) and underlying services like PostgreSQL, Redis, and Qdrant.

File Structure and Descriptions
-------------------------------

**app/profiles/test**
     **Role:** This subdirectory contains a comprehensive suite of test profiles for various Zimagi functionalities.
     **Detailed Description:** It provides foundational YAML files that define common patterns for testing data plugins, including basic CRUD operations, removal scenarios, and generic data handling. Files within this directory are often inherited by other profiles to establish a consistent testing environment for different data types, ensuring the integrity and reliability of the platform.

**app/profiles/test.yml**
     **Role:** Defines the overarching test profile that orchestrates the execution of various sub-test profiles.
     **Detailed Description:** This file acts as the main entry point for running the Zimagi test suite. It configures global test parameters, such as whether to test process profiles, resource profiles, logs, dependencies, and failure scenarios. It uses `_foreach` and `_profile` directives to dynamically include and execute other test profiles based on defined configurations, allowing for a modular and extensible testing framework.

**app/profiles/display.yml**
     **Role:** Configures the fields used for listing and displaying various data types across the Zimagi API.
     **Detailed Description:** This file centralizes the definition of which fields are shown when listing or viewing details of different Zimagi resources, such as users, hosts, modules, states, configurations, groups, logs, scheduled tasks, notifications, and datasets. It ensures consistency in data presentation across the platform's user interfaces and API responses.

**app/profiles/start.yml**
     **Role:** Defines the scaling and startup configuration for various Zimagi services.
     **Detailed Description:** This profile specifies the desired number of instances for core Zimagi services like archiver, qdrant, encoder, language_model, browser, and file_parser. It uses a flexible configuration system that allows for overriding individual service scales or setting a global scale for all services, facilitating easy deployment and scaling of the Zimagi ecosystem.

**app/profiles/migrate.yml**
     **Role:** Orchestrates the database migration process for the Zimagi platform.
     **Detailed Description:** This profile defines a sequence of tasks necessary for managing database schema changes. It includes a pause task, followed by tasks to build and then apply database migrations. This ensures that the database schema is kept up-to-date with the application code, maintaining data integrity and compatibility.

**app/profiles/stop.yml**
     **Role:** Defines the scaling configuration to stop all core Zimagi services.
     **Detailed Description:** This profile sets the scale of all specified Zimagi services (archiver, qdrant, encoder, language_model, browser, file_parser) to zero. It is used to gracefully shut down these services, typically as part of a deployment or maintenance procedure, ensuring that resources are released and services are brought offline in a controlled manner.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow within `app/profiles` is typically initiated by the Zimagi CLI. For instance, `zimagi run start` would load `app/profiles/start.yml` to determine which services to scale up. Similarly, `zimagi run stop` would load `app/profiles/stop.yml` to scale services down. When running tests, `zimagi run test` would load `app/profiles/test.yml`, which then dynamically loads and executes various sub-profiles from `app/profiles/test` based on its internal configuration. Database migrations are handled by `app/profiles/migrate.yml`, which defines a sequential execution of tasks. The `app/profiles/display.yml` file is not directly executed but is consumed by the Zimagi API to determine how data objects are presented.

**External Interfaces**
   The profiles in `app/profiles` primarily interact with the Zimagi server's various APIs and underlying infrastructure:
   *   **Docker/Docker Compose:** The `start.yml` and `stop.yml` profiles directly influence the scaling and lifecycle of Docker containers managed by Docker Compose.
   *   **Zimagi CLI:** All profiles are designed to be invoked and interpreted by the Zimagi command-line interface.
   *   **Zimagi API Services:** Profiles like `display.yml` are consumed by the Command, Data, and MCP APIs to format output. Test profiles in `app/profiles/test` make extensive use of these APIs to perform CRUD operations and task executions.
   *   **Database (PostgreSQL):** The `migrate.yml` profile directly interacts with the PostgreSQL database to apply schema changes. Test profiles also implicitly interact with the database through the data API.
   *   **Celery/Redis:** Task-related profiles (e.g., within `app/profiles/test`) interact with the Celery task queue and Redis for task scheduling and execution.
