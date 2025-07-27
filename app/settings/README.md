# Zimagi Settings Directory

## Overview

The `app/settings` directory contains Django settings files and configuration utilities that define the runtime behavior of the Zimagi platform. These settings control everything from core application parameters and service configurations to task definitions and role-based access controls.

This directory serves as the central configuration hub for the Zimagi server application, providing environment-specific settings, task definitions, and configuration utilities that are used across all components of the platform. It's consumed by both the Django framework at runtime and by developers configuring and extending the platform.

The settings directory plays a critical architectural role by centralizing all configuration concerns in one place, making it easier to manage different deployment scenarios while maintaining consistency across the platform's microservices.

## Directory Contents

### Files

| File          | Purpose                                                                                                           | Format |
| ------------- | ----------------------------------------------------------------------------------------------------------------- | ------ |
| `__init__.py` | Python package initializer that conditionally loads Celery service                                                | Python |
| `app.py`      | Django application configuration that initializes the settings manager when the app is ready                      | Python |
| `client.py`   | Settings specific to the CLI client, including host/port configurations for API connections                       | Python |
| `config.py`   | Configuration utility class for loading and managing environment variables and settings                           | Python |
| `core.py`     | Core application settings including directories, development flags, display configurations, and system parameters | Python |
| `full.py`     | Complete Django settings with database, Redis, API, and service configurations for full platform operation        | Python |
| `install.py`  | Minimal settings configuration used during installation processes                                                 | Python |
| `roles.py`    | Role-based access control definitions and meta-class implementation for permission management                     | Python |
| `tasks.py`    | Celery task definitions for asynchronous command execution and notification sending                               | Python |

### Subdirectories

This directory does not contain any subdirectories.

## Cross-Referencing

The settings directory is a foundational component of the Zimagi platform architecture:

- **Parent Context**: Part of the main `app` directory which contains all server application files
- **Framework Integration**: Settings are loaded by Django as part of the application initialization process
- **Service Configuration**: Settings define connections to external services like PostgreSQL, Redis, and Qdrant
- **Module System**: Settings work with the systems.manager.Manager to load module configurations
- **Task Processing**: Settings configure Celery for background job processing
- **Environment Configuration**: Works with files in the `env` directory to provide runtime configuration
- **Docker Integration**: Settings are used by Docker containers through environment variables defined in the `env` directory

## Key Concepts and Patterns

### Configuration Hierarchy

Settings follow a hierarchy where values are loaded from:

1. Environment variables (highest priority)
2. Default values defined in setting files

### Environment-Based Configuration

Settings support different runtime environments through:

- `ZIMAGI_ENVIRONMENT` variable to select configuration profiles
- Environment-specific Docker configurations
- Service-specific setting overrides

### Settings Categories

- **Core Settings**: Basic application parameters in `core.py`
- **Service Settings**: Database, Redis, and API configurations in `full.py`
- **Client Settings**: CLI-specific configurations in `client.py`
- **Installation Settings**: Minimal configuration for setup in `install.py`
- **Task Definitions**: Asynchronous operations in `tasks.py`
- **Role Management**: Access control definitions in `roles.py`

### Naming Conventions

- Settings variables use UPPER_CASE naming
- Environment variables are prefixed with `ZIMAGI_`
- Configuration classes use PascalCase
- Task functions use snake_case

### Configuration Loading Patterns

The settings directory implements several patterns for loading configuration:

- **Environment Variable Fallback**: All settings check for environment variables before using defaults
- **Type-Safe Configuration**: The `Config` class provides utilities for loading different data types safely
- **Dynamic Module Loading**: Settings can be extended through module configurations
- **Service-Specific Overrides**: Different service types can have customized settings

## Developer Notes and Usage Tips

### Environment Variables

Most settings can be overridden using environment variables prefixed with `ZIMAGI_`. For example:

- `ZIMAGI_DEBUG` controls debug mode
- `ZIMAGI_SECRET_KEY` sets the Django secret key
- `ZIMAGI_POSTGRES_*` variables configure database connections

### Configuration Loading

The `Config` class in `config.py` provides utilities for loading different data types:

- `Config.boolean()` for boolean values
- `Config.integer()` for integer values
- `Config.string()` for string values
- `Config.list()` for list values
- `Config.dict()` for dictionary values

### Task Definitions

Celery tasks are defined in `tasks.py` with retry policies and binding to the task class for access to task instance methods.

### Role System

The `Roles` class in `roles.py` provides meta-programming access to role definitions with runtime validation.

### Dynamic Module Configuration

The `zimagi` Django settings architecture allows for importing Zimagi module settings from `django.py` libraries in the top level module directory. These are then added to the core Django settings object for unified access throughout the application.

### AI Development Guidance

When generating or modifying settings:

- Maintain consistency with existing naming conventions
- Ensure environment variable overrides are properly supported
- Follow the established pattern of default values with environment fallback
- Respect the configuration hierarchy when adding new settings
- Consider performance implications of new configuration options
- Document all new settings with clear, descriptive names
- Follow the established patterns for type-safe configuration loading
