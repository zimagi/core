# Zimagi Log Commands Directory

## Overview

The `app/commands/log` directory contains specialized command implementations for managing and monitoring system logs within the Zimagi platform. These commands provide essential functionality for viewing, cleaning, aborting, and rerunning system logs and their associated command executions, enabling administrators to maintain system health, troubleshoot issues, and manage command execution history effectively.

This directory plays a critical architectural role by implementing the command interface for log management operations. The commands defined here are automatically exposed through both CLI interfaces and RESTful API endpoints, enabling consistent access to log management functionality regardless of the interaction method. The directory is used by:

- **Developers** working on system monitoring and debugging features
- **System administrators** managing Zimagi deployments and operations
- **AI models** analyzing and generating command components

## Directory Contents

### Files

| File     | Purpose                                                                                                      | Format |
| -------- | ------------------------------------------------------------------------------------------------------------ | ------ |
| abort.py | Implements the log abort command for canceling running tasks and waiting for their completion                | Python |
| clean.py | Implements the log clean command for removing old log entries based on retention policies                    | Python |
| get.py   | Implements the log get command for retrieving and displaying detailed information about specific log entries | Python |
| rerun.py | Implements the log rerun command for re-executing commands based on existing log configurations              | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/commands` directory which contains executable commands and agents available through CLI or APIs
- **Specifications**: Command interfaces are defined in `app/spec/commands/log.yml` which drives the command system through YAML specifications
- **Command Systems**: Connects to `app/systems/commands` for command execution framework and dynamic class generation
- **API Systems**: Works with `app/systems/api/command` for REST API exposure of commands
- **Log Data Models**: Integrates with `app/data/log` for log persistence and retrieval
- **Settings**: Uses configurations defined in `app/settings` for log behavior parameters

## Key Concepts and Patterns

### Command Architecture

The log command system implements a specification-driven approach to command generation:

- YAML specifications in `app/spec/commands/log.yml` define command structures and parameters
- The `app/systems/commands/index.py` module dynamically generates command classes at runtime
- Commands are created with appropriate parsing rules and execution logic
- Base command classes provide consistent interfaces for command extension operations

### Log Operations

The log system implements several critical operations based on the specification in `app/spec/commands/log.yml`:

- **Abort Command** (`abort.py`): Cancels running tasks and waits for their completion

  - Base: log
  - Priority: 50
  - Parse configurations: Uses the log mixin's parsing capabilities
  - Implements task cancellation with confirmation and completion waiting
  - Accepts parameters:
    - `log_keys`: Multiple string values representing log keys to abort

- **Clean Command** (`clean.py`): Removes old log entries based on retention policies

  - Base: log
  - Priority: 60
  - Parse configurations: Uses the log mixin's parsing capabilities
  - Implements log cleanup with configurable retention periods
  - Accepts parameters:
    - `log_days`: Integer representing number of days to keep logs (default from settings)
    - `log_message_days`: Integer representing number of days to keep log messages (default from settings)

- **Get Command** (`get.py`): Retrieves and displays detailed information about specific log entries

  - Base: log
  - Priority: 12
  - Parse configurations: Uses the log mixin's parsing capabilities
  - Implements log detail viewing with parameter display and real-time monitoring
  - Accepts parameters:
    - `log_key`: String representing the log key to retrieve

- **Rerun Command** (`rerun.py`): Re-executes commands based on existing log configurations
  - Base: log
  - Priority: 55
  - Parse configurations: Uses the log mixin's parsing capabilities
  - Implements command re-execution with configuration copying
  - Accepts parameters:
    - `log_keys`: Multiple string values representing log keys to rerun

### Command Generation Process

The command generation follows Zimagi's dynamic class generation pattern:

- Commands are generated dynamically at runtime through the indexing system in `app/systems/commands/index.py`
- The `Command("log.operation")` function creates the command class by processing the specification
- The command inherits from the base `log` command as defined in the specification
- Mixins and base commands are composed to provide shared functionality

### Naming Conventions

- Command files are named by their functional operation (e.g., `abort.py`, `clean.py`)
- Command classes are dynamically generated with appropriate naming following the pattern defined in `app/systems/commands/index.py`
- Method names follow Python conventions with descriptive names
- Command lookup paths follow the hierarchical structure defined in specifications

### File Organization

Files are organized by log management operation:

- Each log operation has its own file
- Related log functionality is grouped in this directory
- Files implement specific command operations as defined in the specifications

### Domain-Specific Patterns

- All log commands integrate with the command facade pattern through inheritance
- Error handling follows consistent patterns with custom exception classes
- Integration with log data models for persistence operations through the facade system
- Support for both synchronous and asynchronous execution patterns
- Parameter parsing follows specification-defined structures with typed parameters
- Commands use the resource command set pattern for consistent CRUD operations where applicable

## Developer Notes and Usage Tips

### Integration Requirements

These commands require:

- Django framework access for settings and configuration management
- Proper command specification files in `app/spec/commands/log.yml` for command generation
- Access to log data models in `app/data/log` for persistence operations
- Utility functions from `app/utility` for common operations
- Command system from `app/systems/commands` for dynamic generation and indexing

### Usage Patterns

- Log commands are accessed through the indexing system in `app/systems/commands/index.py` using the `Command()` function
- Implement commands by extending base command classes or using the specification-driven approach
- Follow established patterns for log management operations
- Access command functionality through the standard Zimagi command execution system
- Use `find_command()` function to retrieve command instances by name

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command specifications from `app/spec/commands/log.yml` for generation
- Log data models from `app/data/log` for persistence operations
- Command system from `app/systems/commands` for dynamic generation and execution

### AI Development Guidance

When generating or modifying log commands:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with command-specific exception classes
3. Follow established patterns for log management operations
4. Respect the separation of concerns between different log operations
5. Consider performance implications for log operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing log commands as examples for new implementations
10. Ensure command specifications in `app/spec/commands/log.yml` properly define the interface with appropriate base commands and mixins
11. Understand the two-stage class generation process (dynamic base classes and overlay classes)
12. Follow the metadata structure defined in command specifications for requirements and options
