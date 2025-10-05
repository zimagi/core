=====================================================
README for Directory: app/profiles/test
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as a comprehensive testing ground for various Zimagi functionalities, defining a suite of profiles that configure and execute tests for different aspects of the platform, including data management, task execution, service dependencies, and failure scenarios.

**Key Functionality**
   Testing of data object lifecycle (creation, retrieval, listing, removal), configuration management, host registration, user management, task scheduling, notification handling, module operations, dataset interactions, dependency resolution, failure condition testing, state management, logging, and caching mechanisms.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   These profiles are designed to run within the Zimagi platform's Docker-based environment, leveraging Docker Compose for service orchestration. They are executed by the Zimagi CLI, which interacts with the Zimagi server components.

**Local Dependencies**
   The profiles rely on the core Zimagi framework and its command-line interface. They interact with Docker for container management and depend on the Zimagi server's various APIs (command, data, MCP) and underlying services like PostgreSQL, Redis, and Qdrant.

File Structure and Descriptions
-------------------------------

**app/profiles/test/data**
     **Role:** This subdirectory contains base configurations and test definitions for various data-related operations.
     **Detailed Description:** It provides foundational YAML files that define common patterns for testing data plugins, including basic CRUD operations, removal scenarios, and generic data handling. Files within this directory are often inherited by other profiles to establish a consistent testing environment for different data types.

**app/profiles/test/group.yml**
     **Role:** Defines test profiles for managing and interacting with group data within Zimagi.
     **Detailed Description:** This file specifies configurations and run commands for testing the creation, retrieval, and hierarchical relationships of groups. It includes tests for saving groups with and without parent relationships, finding groups by various criteria, and retrieving child groups, ensuring the integrity of the group management system.

**app/profiles/test/config.yml**
     **Role:** Contains test profiles for managing system configurations within Zimagi.
     **Detailed Description:** This profile outlines tests for saving and retrieving configuration settings. It defines how configurations are stored with specific keys, provider names, value types, and associated groups, and then verifies their retrieval through various search queries, ensuring robust configuration management.

**app/profiles/test/host.yml**
     **Role:** Defines test profiles for managing host data within Zimagi.
     **Detailed Description:** This file provides configurations and run commands for testing the registration and retrieval of host information. It includes tests for saving host details such as hostname, command/data ports, user, token, and encryption key, and then verifying their retrieval based on these attributes.

**app/profiles/test/user.yml**
     **Role:** Defines test profiles for managing user data within Zimagi.
     **Detailed Description:** This profile inherits from `test/data/plugin`, indicating it focuses on testing user-related data operations through the plugin system. It would typically define specific user creation, modification, and retrieval scenarios, ensuring user management functions correctly.

**app/profiles/test/base.yml**
     **Role:** Provides a foundational configuration for all other test profiles in the `test` directory.
     **Detailed Description:** This file sets common parameters, such as the default verbosity level for test execution. Other profiles inherit from this base to ensure consistent settings and to avoid redundancy in configuration.

**app/profiles/test/dependency.yml**
     **Role:** Defines a complex chain of interdependent tasks to test the dependency resolution mechanism of the Zimagi task runner.
     **Detailed Description:** This profile sets up a series of tasks (a through j) where each task depends on the successful completion and output of one or more preceding tasks. The final task `test` verifies the correctness of the resolved dependency chain, ensuring that tasks execute in the correct order and pass their outputs appropriately.

**app/profiles/test/task.yml**
     **Role:** Defines basic task execution tests within Zimagi.
     **Detailed Description:** This file includes simple tasks like echoing "hello world!" and sleeping for a specified duration. It serves to verify the fundamental ability of the Zimagi task runner to execute predefined tasks and manage their basic parameters.

**app/profiles/test/schedule.yml**
     **Role:** Defines test profiles for managing scheduled tasks within Zimagi.
     **Detailed Description:** This profile inherits from `test/data/basic`, suggesting it focuses on testing the creation, retrieval, and listing of scheduled tasks. It would typically include scenarios for defining schedules and verifying their persistence and accessibility within the system.

**app/profiles/test/notification.yml**
     **Role:** Defines test profiles for managing notifications within Zimagi.
     **Detailed Description:** This profile inherits from `test/data/basic`, indicating its purpose is to test the lifecycle of notification objects. It would likely include tests for sending, receiving, and managing various types of notifications within the Zimagi platform.

**app/profiles/test/module.yml**
     **Role:** Defines test profiles for managing modules within Zimagi.
     **Detailed Description:** This profile inherits from `test/data/plugin`, suggesting it focuses on testing the installation, uninstallation, and management of Zimagi modules through the plugin system. It would typically include scenarios to ensure modules can be correctly loaded and operated.

**app/profiles/test/dataset.yml**
     **Role:** Defines test profiles for managing datasets within Zimagi.
     **Detailed Description:** This profile inherits from `test/data/plugin`, indicating its purpose is to test the creation, manipulation, and retrieval of datasets using the Zimagi plugin architecture. It would likely include tests for various data types and structures within datasets.

**app/profiles/test/failure.yml**
     **Role:** Defines a series of tasks designed to test failure handling and dependency interruption in Zimagi.
     **Detailed Description:** This file sets up a sequence of tasks where an intentional failure is introduced (`test2`). Subsequent tasks (`test3`, `test4`, `test5`) are configured to depend on the failing task, verifying that they are not executed as expected when a dependency fails, demonstrating robust error propagation.

**app/profiles/test/state.yml**
     **Role:** Defines test profiles for managing state data within Zimagi.
     **Detailed Description:** This profile inherits from `test/data/basic`, indicating its purpose is to test the storage and retrieval of application state. It would typically include scenarios for saving and loading different forms of state data to ensure persistence and consistency.

**app/profiles/test/log.yml**
     **Role:** Defines test profiles for querying and managing log entries within Zimagi.
     **Detailed Description:** This file specifies configurations for retrieving log entries based on various criteria, such as status, command, user, and task ID. It includes tests for getting specific log entries, listing fields from multiple entries, and finding entries using complex search queries, ensuring comprehensive log access.

**app/profiles/test/cache.yml**
     **Role:** Defines test profiles for managing the Zimagi cache.
     **Detailed Description:** This file includes a `cache_clear` command, which is used to test the functionality of clearing the Zimagi cache. It ensures that the caching mechanism can be properly reset and managed.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow within `app/profiles/test` typically begins with the Zimagi CLI invoking a specific profile (e.g., `zimagi run test/config`). The chosen profile, such as `config.yml`, `host.yml`, or `group.yml`, inherits base configurations from `base.yml` and potentially data-specific configurations from `data/basic.yml` or `data/plugin.yml`. The `pre_run` section of these profiles often generates mock data or queries existing data to set up the test environment. The `run` section then defines a series of commands or tasks, which are executed sequentially or in parallel based on their dependencies. For instance, `dependency.yml` explicitly defines a complex dependency graph, while `failure.yml` demonstrates how failures in one task prevent dependent tasks from running. The `_command` directives in the `run` sections trigger corresponding Zimagi server commands (e.g., `config save`, `host get`, `log list`), which are handled by the Zimagi API services.

**External Interfaces**
   The profiles in `app/profiles/test` primarily interact with the Zimagi server's various APIs:
   *   **Command API:** Used for executing commands like `save`, `get`, `list`, `remove`, `clear`, `children`, and `cache clear`, as seen in `config.yml`, `host.yml`, `group.yml`, `log.yml`, and `cache.yml`.
   *   **Data API:** Implicitly used by the command API for persistent storage and retrieval of data objects (configurations, hosts, groups, users, schedules, notifications, modules, datasets, state, logs).
   *   **Task Runner/Scheduler:** Tasks defined in `task.yml`, `dependency.yml`, and `failure.yml` are executed by the Zimagi task management system, which relies on Celery and Redis.
   *   **Database (PostgreSQL):** Data objects manipulated by the profiles are ultimately stored in the PostgreSQL database.
   *   **Cache (Redis):** Caching operations, such as those in `cache.yml`, interact with the Redis instance.
   *   **Vector Database (Qdrant):** While not explicitly detailed in these specific profiles, Zimagi's data layer can interact with Qdrant for vector-based search and storage.
