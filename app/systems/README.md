# `app/systems` Directory Overview

## Purpose and Role

The `app/systems` directory contains integrated systems that implement core components of the Zimagi application. These systems provide foundational functionalities such as command execution, data modeling, API interfaces, plugin management, and task scheduling. This directory plays a central architectural role by housing the dynamic, specification-driven code generation logic that powers Zimagi's extensible framework.

This directory is primarily used by:

- **Developers** extending or maintaining Zimagi's core systems.
- **AI models** generating or analyzing code, as it defines the structure and behavior of Zimagi's dynamic components.
- **Build systems** that process specifications into executable code.

## Directory Contents

### Files

| File Name       | Purpose                                                                                    | Contents Summary                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `api`           | API-related components including command and data APIs, authentication, views, and schemas | Django REST framework and Model Context Protocol (MCP) integrations, authentication backends, viewsets, schemas, and response handlers |
| `cache`         | Caching middleware and utilities                                                           | Middleware for HTTP-level caching of API responses                                                                                     |
| `celery`        | Celery task queue integration                                                              | Task definitions, worker management, registry, and scheduler customizations                                                            |
| `cell`          | Core computational and AI-driven components                                                | Actor models, error handling, memory management, prompt engines, and state management for AI interactions                              |
| `client`        | Client-side command-line interface (CLI) components                                        | CLI command definitions, argument parsing, error handling, chat interface, and client execution logic                                  |
| `commands`      | Core command execution framework                                                           | Base command classes, mixins, factories, parsers, and execution logic for both local and API-driven commands                           |
| `communication` | Inter-service communication mechanisms                                                     | Tools for managing communication channels, events, and message passing                                                                 |
| `db`            | Database integration and management                                                        | Database router, manager, and migration utilities                                                                                      |
| `encryption`    | Data encryption and cipher management                                                      | Cipher classes and encryption provider integrations                                                                                    |
| `indexer.py`    | Core system indexer for modules, commands, models, and plugins                             | Central registry and dynamic class generation logic                                                                                    |
| `manage`        | Management utilities for services, clusters, tasks, and templates                          | Service lifecycle management, cluster orchestration, task queuing, template rendering                                                  |
| `manager.py`    | Main application manager coordinating all subsystems                                       | Entry point for initializing and managing all Zimagi subsystems                                                                        |
| `models`        | Data model framework including base classes, mixins, and dynamic generation                | ORM integrations, model facades, query parsers, field definitions, and serialization                                                   |
| `plugins`       | Plugin system base classes and indexers                                                    | Plugin provider base classes and dynamic loading logic                                                                                 |
| `kubernetes`    | Kubernetes integration components                                                          | Cluster management, agent scaling, worker deployment, and configuration handling for Kubernetes environments                           |

## Key Concepts and Patterns

### Dynamic Code Generation

Zimagi leverages specification files (YAML) to dynamically generate Python classes for models, commands, and plugins at runtime. The `systems` directory contains the core logic for this meta-programming approach.

### Modular Architecture

Each subdirectory represents a distinct functional domain:

- `commands` and `client` handle user interactions.
- `models` and `db` manage data persistence.
- `api` exposes functionality via HTTP.
- `plugins` allow for extensible behavior.
- `celery` and `manage` support background processing and system lifecycle.

### Specification-Driven Development

Much of Zimagi's behavior is defined in `app/spec` and processed by components in `systems` to generate executable code, reducing boilerplate and increasing maintainability.

## Developer Notes and AI Guidance

### For Developers

- Changes to core logic often require updates in both specification files (`app/spec`) and their corresponding processors in `systems`.
- The `manager.py` and `indexer.py` are central to bootstrapping the application; understand their role before making changes.
- Use the existing mixins and base classes to extend functionality consistently.

### For AI Models

- This directory contains the core logic for interpreting and executing Zimagi's dynamic components.
- When generating code, ensure it aligns with the patterns in `commands`, `models`, and `plugins`.
- Understand that many classes are generated at runtime; static analysis may not capture the full picture.
- Pay attention to the `spec` directory for understanding how to define new components that will be processed by this system.

### Dependencies

- Django (for models, commands, and APIs)
- Celery (for task management)
- Django REST Framework (for API views and serializers)
- Model Context Protocol SDK (for API views)
- Redis (for communication and task queues)
- Kubernetes client (for orchestration)

### Environment Variables

Several environment variables influence the behavior of systems components, particularly around service discovery, encryption, and runtime modes. Refer to `env/` for defaults and `app/settings/` for usage.
