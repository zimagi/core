# Zimagi User Commands Directory

## Overview

The `app/commands/user` directory contains specialized command implementations for managing user accounts within the Zimagi platform's authentication and authorization system. These commands provide essential functionality for user lifecycle management including secure token rotation, enabling administrators to maintain platform security and control access to platform resources and services.

This directory plays a critical architectural role by implementing the command interface for user management operations. The commands defined here are automatically exposed through both CLI interfaces and RESTful API endpoints, enabling consistent access to user management functionality regardless of the interaction method. The directory is used by:

- **Developers** working on authentication and user management features
- **System administrators** managing platform users and access control
- **AI models** analyzing and generating user management components

## Directory Contents

### Files

| File      | Purpose                                                                             | Format |
| --------- | ----------------------------------------------------------------------------------- | ------ |
| rotate.py | Implements the user token rotation command for generating new authentication tokens | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/commands` directory which contains executable commands and agents available through CLI or APIs
- **Specifications**: Command interfaces are defined in `app/spec/commands/user.yml` which drives the command system through YAML specifications
- **Command Systems**: Connects to `app/systems/commands` for command execution framework and dynamic class generation
- **API Systems**: Works with `app/systems/api/command` for REST API exposure of commands
- **User Data Models**: Integrates with `app/data/user` for user persistence and retrieval
- **Settings**: Uses configurations defined in `app/settings` for user behavior parameters

## Key Concepts and Patterns

### Command Architecture

The user command system implements a specification-driven approach to command generation:

- YAML specifications in `app/spec/commands/user.yml` define command structures and parameters
- The `app/systems/commands/index.py` module dynamically generates command classes at runtime
- Commands are created with appropriate parsing rules and execution logic
- Base command classes provide consistent interfaces for command extension operations

### User Operations

The user system implements critical operations based on the specifications in `app/spec/commands/user.yml`:

- **Rotate Command** (`rotate.py`): Generates new authentication tokens for user accounts
  - Base: user
  - Priority: 5
  - Parse configurations: Uses user_key parameter parsing
  - Implements token generation and password updating for security purposes
  - Accepts parameters: user_key (string)
  - When no user_key is provided, rotates the token for the currently active user

### Command Generation Process

The command generation follows Zimagi's dynamic class generation pattern:

- Commands are generated dynamically at runtime through the indexing system in `app/systems/commands/index.py`
- The `Command("user.rotate")` function creates the command class by processing the specification
- The command inherits from the base `user` command as defined in the specification
- Mixins and base commands are composed to provide shared functionality

### Naming Conventions

- Command files are named by their functional operation (e.g., `rotate.py`)
- Command classes are dynamically generated with appropriate naming following the pattern defined in `app/systems/commands/index.py`
- Method names follow Python conventions with descriptive names
- Command lookup paths follow the hierarchical structure defined in specifications

### File Organization

Files are organized by user management operation:

- Each user operation has its own file
- Related user functionality is grouped in this directory
- Files implement specific command operations as defined in the specifications

### Domain-Specific Patterns

- All user commands integrate with the command facade pattern through inheritance
- Error handling follows consistent patterns with custom exception classes
- Integration with user data models for persistence operations through the facade system
- Support for both synchronous and asynchronous execution patterns
- Parameter parsing follows specification-defined structures with typed parameters
- Commands use the resource command set pattern for consistent CRUD operations where applicable

## Developer Notes and Usage Tips

### Integration Requirements

These commands require:

- Django framework access for settings and configuration management
- Proper command specification files in `app/spec/commands/user.yml` for command generation
- Access to user data models in `app/data/user` for persistence operations
- Utility functions from `app/utility` for common operations
- Command system from `app/systems/commands` for dynamic generation and indexing

### Usage Patterns

- User commands are accessed through the indexing system in `app/systems/commands/index.py` using the `Command()` function
- Implement commands by extending base command classes or using the specification-driven approach
- Follow established patterns for user management operations
- Access command functionality through the standard Zimagi command execution system
- Use `find_command()` function to retrieve command instances by name

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command specifications from `app/spec/commands/user.yml` for generation
- User data models from `app/data/user` for persistence operations
- Command system from `app/systems/commands` for dynamic generation and execution

### AI Development Guidance

When generating or modifying user commands:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with command-specific exception classes
3. Follow established patterns for user management operations
4. Respect the separation of concerns between different user operations
5. Consider security implications for user management operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing user commands as examples for new implementations
10. Ensure command specifications in `app/spec/commands/user.yml` properly define the interface with appropriate base commands and mixins
11. Understand the two-stage class generation process (dynamic base classes and overlay classes)
12. Follow the metadata structure defined in command specifications for requirements and options
