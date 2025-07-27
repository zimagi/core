# Zimagi Worker Plugin Directory

## Overview

The `app/plugins/worker` directory contains plugin implementations that provide worker management capabilities for the Zimagi platform's background processing system. These worker plugins enable dynamic scaling and management of background processing workers across different deployment environments including Docker and Kubernetes.

This directory plays a critical architectural role by providing swappable worker provider implementations that extend the platform's auto-scaling capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/worker.yml`. The plugins here are consumed by:

- **Developers** working on auto-scaling and worker management features
- **System administrators** configuring worker scaling workflows
- **AI models** analyzing and generating worker management components

## Directory Contents

### Files

| File          | Purpose                                                                                         | Format |
| ------------- | ----------------------------------------------------------------------------------------------- | ------ |
| base.py       | Implements the base worker provider class with core worker functionality and scaling operations | Python |
| docker.py     | Implements Docker-based worker provider for local container management                          | Python |
| kubernetes.py | Implements Kubernetes-based worker provider for cluster worker management                       | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Worker plugin interfaces are defined in `app/spec/plugins/worker.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly scaling and service management commands
- **Settings**: Uses configurations defined in `app/settings` for worker behavior parameters
- **Management Systems**: Integrates with `app/systems/manage` for service and cluster management operations
- **Kubernetes Systems**: Connects to `app/systems/kubernetes` for Kubernetes cluster operations

## Key Concepts and Patterns

### Plugin Architecture

The worker plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/worker.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of worker operations stored in this directory
- **Base Plugin** provides common functionality that all worker providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Worker Management Operations

All worker plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all worker providers extend, providing core functionality like agent checking, scaling, and worker management
- **Agent Management**: Standardized agent checking, starting, and stopping operations
- **Worker Scaling**: Support for scaling worker counts based on system load and task queues
- **Task Monitoring**: Integration with task queue systems to monitor workload and adjust worker counts accordingly
- **Error Handling**: Custom exception classes for worker operations

### Provider Types

The directory implements several specialized worker providers as defined in `app/spec/plugins/worker.yml`:

- **Base Provider** (`base.py`): Provides core worker functionality and serves as the foundation for all other providers, implementing interfaces like `check_agents`, `check_agent`, `scale_agents`, `start_agent`, `stop_agent`, `get_worker_count`, `get_task_count`, `ensure`, `check_workers`, `start_workers`, and `start_worker`
- **Docker Provider** (`docker.py`): Handles Docker-based worker management with container lifecycle operations
- **Kubernetes Provider** (`kubernetes.py`): Specialized Kubernetes integration with cluster-based worker deployment and management

### Interface Implementation

According to the specification in `app/spec/plugins/worker.yml`, worker plugins implement the following interfaces:

- `check_agents()` - Checks and manages running agent processes
- `check_agent(agent_name)` - Checks if a specific agent is running
- `scale_agents(count)` - Scales the number of agents to the specified count
- `start_agent(agent_name)` - Starts a specific agent
- `stop_agent(agent_name)` - Stops a specific agent
- `get_worker_count()` - Returns the current number of workers
- `get_task_count()` - Returns the current number of pending tasks
- `ensure()` - Ensures workers are running based on system requirements
- `check_workers()` - Checks worker status and scaling requirements
- `start_workers(count)` - Starts the specified number of workers
- `start_worker(name)` - Starts a specific worker by name

### Required Parameters

The worker plugin specification defines the following required parameters:

- **worker_type**: Worker processor machine type (string)
- **command_name**: Full command name to be executed by worker (string)
- **command_options**: Command options passed to the worker (dictionary)

### File Organization

Files are organized by worker provider implementation:

- Each worker provider has its own file named by the provider type
- Base implementation is in `base.py`
- Specialized implementations are in provider-specific files

### Naming Conventions

- Worker provider files are named by their specific implementation (e.g., `docker.py`, `kubernetes.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All worker plugins extend base plugin classes from `systems.plugins.base` through the dynamic generation system
- Plugins implement standardized interface methods for worker operations as defined in the specification
- Error handling uses custom exception classes for worker operations
- Integration with Redis for task queue monitoring and management
- Support for agent lifecycle management with state tracking
- Scaling event tracking and metrics reporting
- Provider-specific cluster or container management operations

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/worker.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations
- Redis connections for task queue management
- Docker or Kubernetes client libraries for container/cluster operations

### Usage Patterns

- Worker plugins are accessed through the indexing system using `BaseProvider("worker", provider_name)` function
- Implement worker providers by creating Python files with Provider classes that extend BaseProvider
- Use existing worker providers as templates for new implementations
- Follow established patterns for worker scaling and management operations
- Access plugin functionality through the manager's get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/worker.yml` for generation
- Redis client for task queue operations
- Docker client library for Docker-based operations
- Kubernetes client library for Kubernetes-based operations

### AI Development Guidance

When generating or modifying worker plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with worker-specific exception classes
3. Follow established patterns for worker scaling and management operations
4. Respect the separation of concerns between different worker provider types
5. Consider performance implications for worker operations during scaling
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing worker providers as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/worker.yml` properly define the interface
11. Implement all required interface methods as specified
12. Use mixins where appropriate to share common functionality
