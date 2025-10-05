=====================================================
README for Directory: app/systems/manage
=====================================================

Directory Overview
------------------

**Purpose**
   This directory encapsulates the core management functionalities for the Zimagi platform, providing mixins and utilities for interacting with various system components such as Docker services, Kubernetes clusters, Redis for communication and task management, and module runtime environments. It centralizes the logic for service orchestration, inter-service communication, task execution, and dynamic configuration management.

**Key Functionality**
   *   Orchestration and management of Docker containers and Kubernetes resources.
   *   Real-time inter-service communication and task status tracking via Redis.
   *   Dynamic loading and installation of module requirements and scripts.
   *   Templating and configuration management for various system components.
   *   Handling of long-running tasks and their lifecycle, including abortion.

Dependencies
-------------------------

This directory heavily relies on several external and internal components:

*   **`redis`**: Used for inter-service communication, task status tracking, and control signals.
*   **`docker` (Python client)**: Interacts with the Docker daemon for managing containers, images, networks, and volumes.
*   **`django.conf.settings`**: Accesses global application settings for configuration, such as Redis URLs, Docker user IDs, and Kubernetes configurations.
*   **`utility.data`**: Provides data structures like `Collection` and utilities for JSON serialization/deserialization, data normalization, and dependency resolution.
*   **`utility.time`**: Offers time-related utilities for consistent timestamping.
*   **`utility.filesystem`**: Used for file operations like loading/saving YAML and JSON, and directory creation.
*   **`utility.parallel`**: Facilitates parallel execution of tasks.
*   **`utility.shell`**: Executes shell commands.
*   **`utility.text`**: Provides text interpolation capabilities.
*   **`systems.kubernetes.cluster`**: Interacts with Kubernetes clusters for resource management.
*   **`jinja2`**: Templating engine used for dynamic configuration generation.

File Structure and Descriptions
-------------------------------

**app/systems/manage/cluster.py**
     **Role:** Manages interactions with the Kubernetes cluster for configuration and service restarts.
     **Detailed Description:** This file defines the `ManagerClusterMixin` class, which provides methods for retrieving and updating global, scheduler, worker, command, and data configurations within a Kubernetes cluster. It leverages the `KubeCluster` utility to abstract Kubernetes API interactions and includes functionality to restart scheduler and other services by updating their configurations with a new timestamp. It also handles the dynamic generation of worker specifications based on module definitions and environment variables.

**app/systems/manage/service.py**
     **Role:** Provides a comprehensive interface for managing Docker services (containers, images, networks, volumes).
     **Detailed Description:** The `ManagerServiceMixin` class in this file offers methods to start, stop, and manage the lifecycle of Docker containers. It includes functionalities for generating image names, listing and creating images, managing Docker networks and volumes, and retrieving service specifications. It handles the persistence of service metadata, checks service health, and provides utilities for displaying service logs and accessing container shells. This mixin is crucial for orchestrating the various microservices that constitute the Zimagi application.

**app/systems/manage/template.py**
     **Role:** Manages the loading, processing, and rendering of Jinja2 templates for dynamic configuration.
     **Detailed Description:** This file contains the `ManagerTemplateMixin` class, which initializes and manages a Jinja2 templating environment. It provides methods for loading templates from various module paths, including special handling for template functions. It supports deep merging of configuration data from multiple sources and ensures that templates are correctly processed and saved, enabling dynamic generation of configuration files and other resources based on application state and module definitions.

**app/systems/manage/communication.py**
     **Role:** Facilitates real-time, channel-based communication between different parts of the system using Redis streams.
     **Detailed Description:** The `ManagerCommunicationMixin` class defines methods for sending and listening to messages on named channels. It uses Redis streams to provide a persistent and ordered message queue. Messages can be validated against predefined channel schemas, ensuring data integrity. This mixin is essential for inter-service communication, allowing components to publish and subscribe to events and data streams, and includes utilities for managing stream states and deleting channels.

**app/systems/manage/runtime.py**
     **Role:** Manages the runtime environment for modules, including script execution and dependency installation.
     **Detailed Description:** This file introduces the `ManagerRuntimeMixin` class, which is responsible for installing module-specific scripts and Python requirements. It parses `requirements.txt` files from modules, deduplicates dependencies, and executes `pip install` commands. It also handles the execution of arbitrary shell scripts defined within modules, providing a mechanism for modules to customize their runtime environment or perform setup tasks.

**app/systems/manage/task.py**
     **Role:** Manages the lifecycle and control of long-running tasks, including status tracking and abortion.
     **Detailed Description:** The `ManagerTaskMixin` class provides functionalities for initializing, tracking, and controlling tasks. It uses Redis to store task statuses, publish messages related to task progress, and handle task abortion signals. It includes a `ControlSensor` thread for real-time monitoring of task control messages and methods for following task output and waiting for tasks to complete. This mixin is critical for managing asynchronous operations and ensuring robust task execution.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The `app/systems/manage` directory provides foundational mixins that are integrated into a larger manager object (likely in `app/systems/manager/base.py` or similar). When the application starts, the manager initializes connections to Redis (via `communication.py` and `task.py`) and potentially Docker (via `service.py`). Modules are loaded, and their templates are processed by `template.py`. During module installation or updates, `runtime.py` handles script execution and dependency installation. Long-running operations or background processes leverage `task.py` for status updates and control. Service orchestration, such as starting or stopping microservices, is handled by `service.py`. In a Kubernetes environment, `cluster.py` manages cluster-wide configurations and service restarts.

**External Interfaces**
   *   **Redis**: `communication.py` and `task.py` directly interact with Redis for message queuing, stream management, and task state persistence.
   *   **Docker Daemon**: `service.py` communicates with the local Docker daemon (via the Python Docker SDK) to manage containers, images, networks, and volumes.
   *   **Kubernetes API**: `cluster.py` interacts with the Kubernetes API to manage cluster configurations and deploy/restart services.
   *   **Operating System Shell**: `runtime.py` executes shell commands (e.g., `pip install`, custom scripts) to configure the environment.
   *   **File System**: `template.py`, `runtime.py`, and `service.py` read and write files for configurations, scripts, and service metadata.
   *   **Other Zimagi Services**: The communication and task management mechanisms enable inter-service communication between various Zimagi microservices (e.g., command-api, mcp-api, data-api, controller, scheduler, tasks).
