=====================================================
README for Directory: app/scripts
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains a collection of shell scripts that serve as entry points and utility functions for managing and operating the Zimagi application services. These scripts are crucial for installation, starting various application components, and handling common operational tasks within the Dockerized environment.

**Key Functionality**
   *   Installation and setup of the Zimagi application.
   *   Launching and managing core Zimagi services like command API, data API, MCP API, controller, and scheduler.
   *   Providing client-side command-line interface execution.
   *   Handling service-specific configurations and process management.
   *   Ensuring service readiness through network and port waiting mechanisms.

Dependencies
-------------------------

The scripts in this directory primarily rely on standard Unix-like shell environments (Bash) and Docker for container orchestration. Specific dependencies include:

*   **Bash:** For script execution and shell functionalities.
*   **Docker and Docker Compose:** For building, running, and managing containerized Zimagi services.
*   **`watchmedo`:** Used in several service scripts for automatic code reloading during development (when `ZIMAGI_AUTO_UPDATE` is true).
*   **`celery`:** For task queue management, specifically in `celery-flower.sh`, `scheduler.sh`, and `worker.sh`.
*   **`gunicorn`:** A WSGI HTTP server used by `command.sh` and `data.sh`.
*   **`uvicorn`:** An ASGI server used by `mcp.sh`.
*   **`curl`:** Used in health checks within Docker Compose configurations (though not directly in these scripts, it's a related dependency for service readiness).
*   **`hexdump`:** Used in the `start` script for generating random passwords and keys.
*   **`getent`:** Used in the `start` script for retrieving group information.
*   **`awk`:** Used in the `start` script for parsing group information.

File Structure and Descriptions
-------------------------------

**app/scripts/config**
     **Role:** This directory holds configuration scripts that define the specific processes and settings for various Zimagi services.
     **Detailed Description:** Each file within this subdirectory (e.g., `controller.sh`, `scheduler.sh`, `wsgi.sh`, `mcp.sh`, `worker.sh`) exports environment variables, primarily `ZIMAGI_SERVICE_PROCESS`, which dictates the exact command and arguments used to start a particular Zimagi service. This modular approach allows for flexible and centralized management of service startup commands.

**app/scripts/install.sh**
     **Role:** The primary script for installing the Zimagi application.
     **Detailed Description:** This script sets up the environment for installation, including debug flags and color settings, and then executes the main Python-based installation script (`zimagi-install.py`). It acts as the initial entry point for deploying the application.

**app/scripts/data.sh**
     **Role:** This script is responsible for starting the Zimagi data API service.
     **Detailed Description:** It conditionally uses `watchmedo` for automatic reloading during development or directly invokes `zimagi-gateway` to run the WSGI application for the data API. It ensures the data API is properly initialized and running, handling requests related to data management.

**app/scripts/gateway.sh**
     **Role:** A generic service gateway script used to initialize and start various Zimagi services.
     **Detailed Description:** This script is a central component for service management. It takes a service type as an argument, sources service-specific configurations from `app/scripts/config`, waits for database and Redis connectivity, performs initial database migrations and module initialization (for scheduler), and then launches the specified service process. It handles service lifecycle events, including graceful shutdown.

**app/scripts/controller.sh**
     **Role:** This script initiates the Zimagi controller service.
     **Detailed Description:** Similar to `data.sh`, it leverages `watchmedo` for development-time auto-reloading or directly calls `zimagi-gateway` to start the controller. The controller service is responsible for managing and orchestrating other Zimagi components and agents.

**app/scripts/celery-flower.sh**
     **Role:** This script starts the Celery Flower monitoring tool for the Zimagi task queues.
     **Detailed Description:** It ensures that the PostgreSQL and Redis services are available before launching Celery Flower. Flower provides a web-based interface to monitor the status of Celery workers and tasks, offering insights into the application's asynchronous processing.

**app/scripts/wait.sh**
     **Role:** A utility script to wait for TCP hosts and ports to become available.
     **Detailed Description:** This script is crucial for ensuring service dependencies are met before a service attempts to connect. It can wait for multiple hosts and ports, with configurable timeouts, and can optionally check for HTTP/HTTPS status codes. It's used by `gateway.sh` and `celery-flower.sh` to ensure database and message queue readiness.

**app/scripts/README.rst**
     **Role:** This file provides documentation for the `app/scripts` directory.
     **Detailed Description:** This file, which you are currently reading, explains the purpose, functionality, dependencies, and structure of the scripts within the `app/scripts` directory, aiding in understanding and maintenance.

**app/scripts/scheduler.sh**
     **Role:** This script starts the Zimagi scheduler service.
     **Detailed Description:** It uses `watchmedo` for development or directly calls `zimagi-gateway` to run the scheduler. The scheduler is responsible for executing periodic tasks and managing the timing of various operations within the Zimagi application.

**app/scripts/mcp.sh**
     **Role:** This script starts the Zimagi MCP (Management Control Plane) API service.
     **Detailed Description:** It conditionally uses `watchmedo` for automatic reloading during development or directly invokes `zimagi-gateway` to run the ASGI application for the MCP API. This service handles management and control plane operations.

**app/scripts/command.sh**
     **Role:** This script starts the Zimagi command API service.
     **Detailed Description:** It conditionally uses `watchmedo` for automatic reloading during development or directly invokes `zimagi-gateway` to run the WSGI application for the command API. This service processes and responds to commands issued to the Zimagi system.

**app/scripts/client.sh**
     **Role:** This script executes client-side commands for the Zimagi application.
     **Detailed Description:** It changes the directory to the Zimagi share location and then executes the main Python-based client script (`zimagi-client.py`) with any provided arguments. This script serves as the entry point for users interacting with the Zimagi CLI.

**app/scripts/worker.sh**
     **Role:** This script starts a Zimagi worker service for processing asynchronous tasks.
     **Detailed Description:** It uses `watchmedo` for development or directly calls `zimagi-gateway` to run a Celery worker. Workers are essential for offloading long-running or background tasks from the main API services, improving responsiveness and scalability.

**app/scripts/cli.sh**
     **Role:** This script is an alias or wrapper for executing Zimagi CLI commands.
     **Detailed Description:** It changes the directory to the Zimagi share location and then executes the main Python-based CLI script (`zimagi-cli.py`) with any provided arguments. It provides a consistent way to interact with the Zimagi command-line interface.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The typical execution flow often begins with `start`, which sets up the Docker Compose environment and then orchestrates the launch of various services. For individual services, scripts like `command.sh`, `data.sh`, `mcp.sh`, `controller.sh`, `scheduler.sh`, and `worker.sh` act as entry points. These service-specific scripts then delegate to `gateway.sh`, which handles common initialization tasks such as waiting for database and Redis availability using `wait.sh`, performing migrations, and then finally launching the core service process defined in the `app/scripts/config` directory. Client interactions typically go through `cli.sh` or `client.sh`, which directly execute the Python CLI.

**External Interfaces**
   The scripts in this directory interact extensively with Docker for container management and orchestration. They connect to PostgreSQL and Redis databases (whose hosts and ports are often configured via environment variables) to ensure data persistence and message queuing. The various API services (command, data, MCP) expose HTTP/HTTPS endpoints for external communication. Celery workers and the scheduler interact with Redis for task queuing and scheduling.