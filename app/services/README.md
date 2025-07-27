# Services Directory

## Overview

The `app/services` directory contains Django service gateway configurations and Celery integration files that define how the Zimagi platform's microservices operate. This directory plays a critical architectural role by providing the entry points and configuration for the platform's core services: Command API, Data API, Controller, MCP API, Scheduler, and Worker services.

This directory is primarily used by:

- **Docker containers** at runtime to initialize service configurations
- **Developers** working on service-level configurations
- **AI models** analyzing system architecture and service integration points

## Directory Contents

### Files

| File        | Purpose                                                              | Format |
| ----------- | -------------------------------------------------------------------- | ------ |
| `celery.py` | Celery service gateway configuration for distributed task processing | Python |
| `mcp.py`    | MCP (Model Context Protocol) ASGI application configuration          | Python |
| `wsgi.py`   | WSGI application entry point for synchronous web services            | Python |

### Subdirectories

| Directory    | Purpose                                           | Contents                                                            |
| ------------ | ------------------------------------------------- | ------------------------------------------------------------------- |
| `command`    | Command API service configuration and URL routing | Settings and URL configuration for the Command API service          |
| `controller` | Controller service configuration                  | Service configuration files                                         |
| `data`       | Data API service configuration and URL routing    | Settings, URL configuration, and API views for the Data API service |
| `mcpapi`     | MCP API service configuration                     | Service configuration for Model Context Protocol API                |
| `tasks`      | Task scheduler service configuration              | Service configuration for scheduled task execution                  |
| `cli`        | CLI service configuration                         | Command-line interface service configuration                        |

## Key Concepts and Patterns

### Service Architecture

The Zimagi platform follows a microservices architecture with each service having its own configuration:

- **Command API**: Handles streaming RPC commands for system management
- **Data API**: Provides RESTful data access endpoints
- **Scheduler**: Manages timed and recurring task execution
- **Worker**: Processes background tasks from the queue
- **Controller**: Manages all system agents
- **MCP API**: Model Context Protocol interface

### Configuration Patterns

- Each service has a dedicated settings module following Django settings conventions
- Services share common Django settings but can override service-specific configurations
- URL routing is defined per service to maintain clear API boundaries
- WSGI/ASGI configurations enable both synchronous and asynchronous service operation

### Naming Conventions

- Service directories match their functional names (command, data, controller, etc.)
- Configuration files follow Django settings naming patterns
- URL routing modules are consistently named `urls.py`
- Service entry points use descriptive names (`wsgi.py`, `mcp.py`)

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Docker Integration**: Works with `docker` directory for container configuration
- **Environment Configuration**: Connects to `env` directory for runtime environment variables
- **Scripts Integration**: Connects to `app/scripts` for service initialization and execution
- **Settings System**: Integrates with `app/settings` for global configuration management

## Developer Notes

### Service Initialization

Each service is initialized through its respective Docker container entry point which loads the appropriate settings module:

- Command API: `services.command.settings`
- Data API: `services.data.settings`
- Controller: `services.controller.settings`
- MCP API: `services.mcpapi.settings`
- Scheduler/Worker: `services.tasks.settings`

### Dependencies

- Django framework for web service functionality
- Celery for distributed task processing
- Redis for task queue management
- PostgreSQL database backend for persistent storage

### Environment Variables

Services rely on several key environment variables:

- `ZIMAGI_SERVICE`: Identifies the current service type
- `DJANGO_SETTINGS_MODULE`: Points to the appropriate settings module
- Service-specific variables for ports, security, and integration

### AI Development Guidance

When generating or modifying service configurations:

1. Maintain consistency with existing Django settings patterns
2. Ensure service isolation while allowing necessary cross-service communication
3. Follow established naming conventions for settings and configuration keys
4. Consider performance implications of service configurations
5. Maintain security best practices in authentication and permission settings
