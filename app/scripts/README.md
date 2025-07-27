# Zimagi Scripts Directory

## Overview

The `app/scripts` directory contains Docker entrypoint scripts, command configurations, server configurations, and helper scripts that power the Zimagi platform's execution environment. These scripts serve as the primary interface between Docker containers and the Zimagi application, handling service initialization, command execution, and inter-service communication.

This directory is essential for both development and production environments, as it defines how services are started, how they interact with dependencies, and how commands are executed within the Zimagi ecosystem. The scripts are used by both human operators and automated systems (CI/CD, Kubernetes deployments).

## Directory Contents

### Files

| File             | Purpose                                                                          | Format            |
| ---------------- | -------------------------------------------------------------------------------- | ----------------- |
| cli.sh           | CLI command execution entrypoint                                                 | Bash shell script |
| client.sh        | Client command execution entrypoint                                              | Bash shell script |
| command.sh       | Entrypoint script for command execution with auto-update file watching           | Bash shell script |
| controller.sh    | Controller service entrypoint with auto-update file watching                     | Bash shell script |
| data.sh          | Entrypoint script for data operations with auto-update file watching             | Bash shell script |
| gateway.sh       | Main service gateway script that initializes and starts various Zimagi services  | Bash shell script |
| install.sh       | Module installation script with debug environment setup                          | Bash shell script |
| mcp.sh           | MCP (Model Context Protocol) service entrypoint with auto-update file watching   | Bash shell script |
| scheduler.sh     | Scheduler service entrypoint with auto-update file watching                      | Bash shell script |
| wait.sh          | TCP host/port availability testing script with HTTP status checking capabilities | Bash shell script |
| worker.sh        | Worker service entrypoint with auto-update file watching                         | Bash shell script |
| celery-flower.sh | Celery Flower monitoring tool startup script with dependency waiting             | Bash shell script |

### Subdirectories

| Directory | Purpose                           | Contents                                                   |
| --------- | --------------------------------- | ---------------------------------------------------------- |
| config    | Service configuration definitions | Bash shell scripts defining service process configurations |

## Config Subdirectory

The `config` directory contains service-specific configuration files that define how different Zimagi services should be executed.

### Configuration Files

| File          | Purpose                                                            |
| ------------- | ------------------------------------------------------------------ |
| controller.sh | Defines controller service process configuration                   |
| mcp.sh        | Defines MCP (Model Context Protocol) service process configuration |
| scheduler.sh  | Defines Celery scheduler service process configuration             |
| wsgi.sh       | Defines WSGI service process configuration for web APIs            |
| worker.sh     | Defines Celery worker service process configuration                |

## Key Concepts and Patterns

### Service Initialization Pattern

Most service scripts follow a common pattern:

1. Wait for required dependencies (PostgreSQL, Redis)
2. Initialize service-specific requirements (migrations, module initialization)
3. Switch to service execution mode
4. Start the actual service process

### Auto-Update Feature

Several scripts support an auto-update mode controlled by the `ZIMAGI_AUTO_UPDATE` environment variable. When enabled, they use `watchmedo` to automatically restart the service when relevant files change, which is useful for development.

### Environment Variable Conventions

Scripts use standardized environment variables following the `ZIMAGI_` prefix pattern:

- `ZIMAGI_SERVICE_*` for service-specific configurations
- `ZIMAGI_*_HOST` and `ZIMAGI_*_PORT` for service dependencies
- `ZIMAGI_LOG_LEVEL` for logging configuration
- `ZIMAGI_AUTO_UPDATE` for development auto-restart functionality

### Service Types

The scripts support various service types that correspond to different Zimagi platform components:

- **command**: Command API service for streaming RPC operations
- **controller**: Controller service for system management
- **data**: Data API service for REST operations
- **mcp**: Model Context Protocol service for AI integration
- **scheduler**: Celery scheduler for timed operations
- **worker**: Celery worker for background task processing
- **wsgi**: WSGI service gateway for web APIs

## Cross-Referencing

This directory integrates with:

- Docker configurations in the `docker` directory
- Environment variables defined in the `env` directory
- Zimagi service implementations in `app/services`
- The main zimagi executable in the project root
- Reactor Kubernetes development platform integration
- The top-level `start` script which uses these scripts to initialize and run services
- The top-level `zimagi` script which executes commands through these entrypoints

The root-level `start` script sources the Reactor initialization and sets up the environment before calling Docker Compose to bring up services. It uses scripts from this directory to build the client Docker image and initialize service dependencies.

## Developer Notes

### Dependencies

Scripts require:

- Bash shell environment
- Docker (for containerized execution)
- Standard Unix utilities (curl, timeout, etc.)
- Python environment with Zimagi packages installed

### Usage Tips

1. Scripts are designed to be executed within Docker containers, not directly on host systems
2. Service-specific configurations should be defined in the `config` subdirectory
3. The `wait.sh` script is a critical dependency for ensuring services start in the correct order
4. Auto-update functionality should only be used in development environments
5. Gateway script is the main entrypoint that other scripts typically delegate to
6. The `start` script in the project root uses these scripts to initialize the development environment

### AI Development Guidance

When generating or modifying scripts in this directory:

1. Maintain consistency with existing environment variable naming conventions
2. Follow the service initialization pattern for new service types
3. Ensure proper signal handling for graceful shutdowns
4. Use the wait.sh script to handle service dependencies appropriately
5. Implement auto-update functionality using the established watchmedo pattern
6. Maintain consistency with process configuration definitions in the config directory
7. Follow the established naming conventions for service types
8. Ensure all scripts properly handle Zimagi service initialization and execution modes
9. Reference existing scripts as templates for new service implementations
10. Maintain compatibility with the top-level initialization scripts (`start` and `zimagi`)
