# Zimagi Service Commands Directory

## Overview

The `app/commands/service` directory contains specialized command implementations that provide service management capabilities for the Zimagi platform. These commands enable administrators to perform essential operations such as scaling platform agents, monitoring communication channels, and managing distributed locking mechanisms that coordinate different platform components.

This directory plays a critical architectural role by implementing the command interface for service management operations. The commands defined here are automatically exposed through both CLI interfaces and RESTful API endpoints, enabling consistent access to service management functionality regardless of the interaction method. The directory is used by:

- **Developers** working on service management and orchestration features
- **System administrators** managing Zimagi deployments and service scaling
- **AI models** analyzing and generating service management components

## Directory Contents

### Files

| File      | Purpose                                                                                                         | Format |
| --------- | --------------------------------------------------------------------------------------------------------------- | ------ |
| follow.py | Implements the service follow command for monitoring communication channels and streaming messages in real-time | Python |
| scale.py  | Implements the service scale command for scaling platform agents to specified counts                            | Python |

### Subdirectories

| Directory | Purpose                                              | Contents                                                                |
| --------- | ---------------------------------------------------- | ----------------------------------------------------------------------- | ------------------ |
| lock      | Contains commands for distributed locking mechanisms | Set, wait, and clear lock commands with expiration and timeout handling | See lock/README.md |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/commands` directory which contains executable commands and agents available through CLI or APIs
- **Specifications**: Command interfaces are defined in `app/spec/commands/service.yml` which drives the command system through YAML specifications
- **Command Systems**: Connects to `app/systems/commands` for command execution framework and dynamic class generation
- **API Systems**: Works with `app/systems/api/command` for REST API exposure of commands
- **Management Systems**: Integrates with `app/systems/manage` for service scaling and management operations
- **Settings**: Uses configurations defined in `app/settings` for service behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility/mutex.py` for distributed locking mechanisms

The service command system is part of the broader Zimagi command architecture which provides a specification-driven approach to command generation. Commands in this directory follow the same patterns as other Zimagi commands and integrate with the platform's dynamic class generation system.

## Key Concepts, Conventions, and Patterns

### Command Architecture

The service command system implements a specification-driven approach to command generation:

- YAML specifications in `app/spec/commands/service.yml` define command structures and parameters
- The `app/systems/commands/index.py` module dynamically generates command classes at runtime
- Commands are created with appropriate parsing rules and execution logic
- Base command classes provide consistent interfaces for command extension operations

### Service Operations

Based on the actual implementation, the service system provides these operations:

- **Scale Command** (`scale.py`): Scales platform agents to a specified count

  - Base: scale (inherits from service)
  - Implements agent scaling by finding matching agents and updating configuration values
  - Uses the manager to collect agents and update their scale configuration
  - Displays a table of agent counts before and after scaling
  - Accepts parameters:
    - agent_name (multiple strings): Names of agents to scale
    - agent_count (string): New count for the specified agents

- **Follow Command** (`follow.py`): Monitors communication channels for messages
  - Base: service
  - Implements message monitoring with channel listening capabilities
  - Uses the listen method to monitor communication channels
  - Displays messages in a formatted table with time, sender, and message content
  - Accepts parameters:
    - channel (string): Communication channel to monitor
    - state_key (string): State variable key for tracking message state
    - timeout (integer): Wait timeout in seconds (default: 600)

### Lock Operations

The lock subdirectory implements distributed locking mechanisms through the mutex system:

- **Set Command**: Sets a distributed lock with an optional expiration time using `Mutex.set()`

  - Accepts parameters:
    - key (string): Service lock key
    - expires (integer): Key expiration in seconds (optional)

- **Wait Command**: Waits for distributed locks to be released with timeout handling using `Mutex.wait()`

  - Accepts parameters:
    - raise_error (flag): Raise error if timeout exceeded
    - keys (multiple strings): One or more service keys to wait for
    - timeout (integer): Wait timeout in seconds (default: 600)
    - interval (integer): Poll interval during wait period in seconds (default: 1)

- **Clear Command**: Clears distributed locks by their keys using `Mutex.clear()`
  - Accepts parameters:
    - keys (multiple strings): One or more service keys to clear

### Naming Conventions

- Command files are named by their functional operation (e.g., `scale.py`, `follow.py`)
- Command classes extend the base command with the command name as a parameter using `Command("command_name")`
- Method names follow Python conventions with descriptive names
- Command lookup paths follow the hierarchical structure defined in specifications

### File Organization

Files are organized by service management operation:

- Core service operations in the main directory (`follow.py`, `scale.py`)
- Distributed locking operations in the `lock` subdirectory
- Each operation has its own file implementing specific command functionality

### Domain-Specific Patterns

- All service commands integrate with the command facade pattern through inheritance
- Error handling follows consistent patterns with custom exception classes
- Integration with service management systems for orchestration operations through the manager
- Support for both synchronous and asynchronous execution patterns
- Parameter parsing follows specification-defined structures with typed parameters
- Commands use the resource command set pattern for consistent CRUD operations where applicable
- Distributed locking uses mutex implementations for coordination between concurrent operations via `app/utility/mutex.py`
- Agent scaling works by updating configuration values that control agent counts
- Communication channel monitoring uses the listen method with message formatting

## Developer Notes and Usage Tips

### Integration Requirements

These commands require:

- Django framework access for settings and configuration management
- Proper command specification files in `app/spec/commands/service.yml` for command generation
- Access to service management systems in `app/systems/manage` for orchestration operations
- Utility functions from `app/utility` for common operations
- Command system from `app/systems/commands` for dynamic generation and indexing
- Mutex system from `app/utility/mutex.py` for distributed locking

### Usage Patterns

- Service commands are accessed through the indexing system in `app/systems/commands/index.py` using the `Command()` function
- Implement commands by extending base command classes or using the specification-driven approach
- Follow established patterns for service management operations
- Access command functionality through the standard Zimagi command execution system
- Use `find_command()` function to retrieve command instances by name

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command specifications from `app/spec/commands/service.yml` for generation
- Service management systems from `app/systems/manage` for orchestration
- Command system from `app/systems/commands` for dynamic generation and execution
- Mutex system from `app/utility/mutex.py` for distributed locking
- Redis connections for distributed mutex operations

### AI Development Guidance

When generating or modifying service commands:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with command-specific exception classes
3. Follow established patterns for service management operations
4. Respect the separation of concerns between different service operations
5. Consider performance implications for service operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing service commands as examples for new implementations
10. Ensure command specifications in `app/spec/commands/service.yml` properly define the interface with appropriate base commands and mixins
11. Understand the two-stage class generation process (dynamic base classes and overlay classes)
12. Follow the metadata structure defined in command specifications for requirements and options
13. Leverage the Mutex utility class for distributed locking operations
14. Use proper error handling with MutexError and MutexTimeoutError exceptions
