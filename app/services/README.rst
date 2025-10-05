=====================================================
README for Directory: app/services
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central hub for all core Zimagi application services, defining their configurations, entry points, and interconnections. It orchestrates the various components that make up the Zimagi platform, from API endpoints to background task processing.

**Key Functionality**
   *   Configuration and bootstrapping of various API services (Command, Data, MCP).
   *   Management of background task processing via Celery.
   *   Definition of WSGI and ASGI entry points for web servers.
   *   Centralized settings management for different service types.
   *   Orchestration of the Zimagi controller and scheduler components.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This codebase is primarily designed for execution within a Dockerized environment, leveraging Python 3.10+ and Django 5.2+. It is intended to run on Linux-based systems, with specific configurations for both standard and NVIDIA GPU-enabled environments.

**Local Dependencies**
   *   `Django`: The primary web framework used for building the services.
   *   `Celery`: Used for asynchronous task processing and scheduling.
   *   `Starlette`: A lightweight ASGI framework used for the MCP API.
   *   `mcp`: An internal library for managing streamable HTTP sessions.
   *   `docker-py`: Python client for the Docker Engine API, used for service management.
   *   `utility.data`, `utility.filesystem`, `utility.shell`, `utility.text`, `utility.parallel`: Internal Zimagi utility libraries providing common functionalities like data manipulation, file system operations, shell execution, text interpolation, and parallel processing.


File Structure and Descriptions
-------------------------------

**app/services/command**
     **Role:** Directory containing the settings and URL configurations for the Zimagi Command API service.
     **Detailed Description:** This subdirectory houses the `settings.py` and `urls.py` files specifically tailored for the Command API. `settings.py` defines the Django settings relevant to the Command API, including REST Framework configurations, authentication classes, and permission policies. `urls.py` maps the API endpoints for command execution and schema generation.

**app/services/tasks**
     **Role:** Directory containing the settings for the Zimagi background task services.
     **Detailed Description:** This subdirectory contains the `settings.py` file that defines the Django settings specifically for the Celery worker and scheduler tasks. It configures aspects related to task execution, queues, and other Celery-specific parameters.

**app/services/data**
     **Role:** Directory containing the settings and URL configurations for the Zimagi Data API service.
     **Detailed Description:** This subdirectory holds the `settings.py` and `urls.py` files for the Data API. `settings.py` configures the Django REST Framework for data access, including authentication, permissions, parsers, renderers, and filtering. `urls.py` defines the API endpoints for data interaction, schema access, and dataset downloads.

**app/services/cli**
     **Role:** Directory containing the settings for the Zimagi Command Line Interface (CLI) service.
     **Detailed Description:** This subdirectory contains the `settings.py` file, which defines the Django settings specifically for the Zimagi CLI. These settings might include configurations related to CLI commands, output formatting, and other CLI-specific behaviors.

**app/services/mcpapi**
     **Role:** Directory containing the settings for the Zimagi Message Control Protocol (MCP) API service.
     **Detailed Description:** This subdirectory contains the `settings.py` file, which defines the Django settings for the MCP API. These settings are crucial for configuring the behavior and security of the real-time communication and streaming capabilities provided by the MCP API.

**app/services/controller**
     **Role:** Directory containing the settings for the Zimagi Controller service.
     **Detailed Description:** This subdirectory contains the `settings.py` file, which defines the Django settings for the Zimagi Controller. The controller is responsible for orchestrating and managing various aspects of the Zimagi platform, and its settings govern its operational parameters.

**app/services/wsgi.py**
     **Role:** The WSGI entry point for Django applications within Zimagi services.
     **Detailed Description:** This file exposes the WSGI callable as a module-level variable named `application`. It is the standard entry point for WSGI-compatible web servers (like Gunicorn or uWSGI) to serve Django applications. It sets the `DJANGO_SETTINGS_MODULE` environment variable and initializes the Django application, also utilizing a `Mutex` for startup synchronization.

**app/services/mcp.py**
     **Role:** The ASGI entry point for the Zimagi Message Control Protocol (MCP) API service.
     **Detailed Description:** This file exposes the ASGI callable as a module-level variable named `application`. It is the entry point for ASGI-compatible web servers (like Uvicorn) to serve the MCP API, which handles real-time, streamable HTTP connections. It configures a Starlette application with routes for status checks and connection handling, integrating with an internal `mcp.server.lowlevel.Server` and `StreamableHTTPSessionManager`. It also includes authentication middleware.

**app/services/celery.py**
     **Role:** The main configuration and entry point for Zimagi's Celery asynchronous task processing.
     **Detailed Description:** This file initializes the Celery application, configures it from Django settings, and auto-discovers tasks. It includes signal handlers for `celeryd_init`, `before_task_publish`, and `worker_shutting_down` to manage worker lifecycle, ensure worker availability for tasks, and clean up resources. It also conditionally starts a worker manager based on environment variables.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow within `app/services` is highly dependent on the specific service being invoked.
   1.  **API Services (Command, Data, MCP):** For HTTP/HTTPS requests, `app/services/wsgi.py` (for traditional Django views) or `app/services/mcp.py` (for ASGI-based real-time communication) act as the initial entry points. These files bootstrap the Django or Starlette application, which then routes requests to appropriate views or handlers defined within their respective subdirectories (e.g., `app/services/command/urls.py`, `app/services/data/urls.py`). These handlers then interact with the core Zimagi application logic, which resides outside this `app/services` directory.
   2.  **Background Tasks:** When Celery tasks are initiated, `app/services/celery.py` is the central orchestrator. It configures the Celery application, loads tasks, and manages worker processes. The `before_task_publish` signal handler in `celery.py` plays a crucial role in ensuring that the necessary worker services are running before a task is dispatched.
   3.  **Controller and Scheduler:** The `app/services/controller` and `app/services/tasks` directories contain settings for the controller and scheduler components, respectively. These services are typically started as long-running processes within the Docker environment, managed by the overall Docker Compose setup.

**External Interfaces**
   The services within `app/services` interact with several external components:
   *   **Databases:** Services connect to PostgreSQL (for relational data), Redis (for caching and message brokering for Celery), and Qdrant (for vector search), as configured by environment variables and Docker Compose.
   *   **Docker Engine:** The `app/systems/manage/service.py` (which is part of the broader Zimagi system but interacts with these services) uses the `docker-py` library to manage Docker containers, images, and networks for the various Zimagi services.
   *   **Web Servers:** WSGI services (e.g., Command API, Data API) are designed to be served by WSGI-compatible web servers (like Gunicorn), while ASGI services (e.g., MCP API) are served by ASGI-compatible web servers (like Uvicorn).
   *   **External APIs/Services:** While not explicitly defined within these top-level files, the underlying Zimagi application logic (outside `app/services`) can interact with various external APIs and services as required by specific modules or commands.
