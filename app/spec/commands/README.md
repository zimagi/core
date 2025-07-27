# Zimagi Command Specifications Directory

## Overview

The `app/spec/commands` directory contains YAML specification files that define the structure, parameters, and behavior of executable commands within the Zimagi platform. These specifications serve as the foundation for the platform's meta-programming code generation system, enabling dynamic creation of command interfaces and execution environments with minimal custom code.

This directory plays a critical role in Zimagi's "specification-driven development" approach, where YAML configurations are transformed into functional Python classes at runtime. The specifications defined here are consumed by the code generation system in `app/systems/commands/meta` to create the command layer that powers the platform's CLI and API command execution capabilities.

The directory is used by:

- **Developers** to define and extend command functionality
- **Code generation systems** to create dynamic Python classes
- **AI models** analyzing and generating platform components

## Directory Contents

### Files

| File             | Purpose                                                                             | Format |
| ---------------- | ----------------------------------------------------------------------------------- | ------ |
| ai.yml           | Defines AI-related commands including text encoding and language model interactions | YAML   |
| agents.yml       | Specifies agent command configurations for various service types                    | YAML   |
| cache.yml        | Defines cache management commands                                                   | YAML   |
| calculate.yml    | Specifies calculation execution commands and parameters                             | YAML   |
| chat.yml         | Defines chat-related commands and agent configurations                              | YAML   |
| config.yml       | Specifies configuration management commands                                         | YAML   |
| controller.yml   | Defines agent controller commands                                                   | YAML   |
| database.yml     | Specifies database management commands including backup and restore                 | YAML   |
| dataset.yml      | Defines dataset management commands                                                 | YAML   |
| group.yml        | Specifies user group management commands                                            | YAML   |
| gpu.yml          | Defines GPU resource management commands                                            | YAML   |
| host.yml         | Specifies host management commands                                                  | YAML   |
| import.yml       | Defines data import commands and specifications                                     | YAML   |
| log.yml          | Specifies log management and monitoring commands                                    | YAML   |
| message.yml      | Defines inter-service messaging commands                                            | YAML   |
| module.yml       | Specifies module management commands including creation and deployment              | YAML   |
| notification.yml | Defines notification system commands                                                | YAML   |
| platform.yml     | Specifies platform-level commands like version info and testing                     | YAML   |
| qdrant.yml       | Defines Qdrant vector database management commands                                  | YAML   |
| schedule.yml     | Specifies scheduled task management commands                                        | YAML   |
| scaling.yml      | Defines auto-scaling event commands                                                 | YAML   |
| service.yml      | Specifies service management commands including scaling and locking                 | YAML   |
| state.yml        | Defines state variable management commands                                          | YAML   |
| template.yml     | Specifies template generation commands                                              | YAML   |
| user.yml         | Defines user management commands                                                    | YAML   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory is part of the broader `app/spec` system which generates dynamic classes for the Zimagi platform. The command specifications defined here are consumed by:

- **Parent Context**: Part of the `app/spec` directory which contains all YAML specifications for the platform's meta-programming system
- **Code Generation**: Specifications are processed by systems in `app/systems/commands/meta` to generate dynamic Python classes
- **Command Implementations**: Files in `app/commands` reference these specifications in their definitions
- **API Endpoints**: Generated commands automatically create API endpoints in `app/systems/api/command`
- **Profile Components**: Command specifications are used in `app/profiles` to orchestrate workflows

The generated classes are used throughout the application, particularly in:

- `app/systems/commands` for command execution
- `app/systems/api/command` for API command endpoints
- `app/commands` for command implementations

These specifications integrate with the meta-programming systems in `app/systems/commands/meta` which transform YAML specifications into functional Python classes.

## Key Concepts and Patterns

### Specification Structure

Each YAML file defines one or more command specifications that include:

- Command identification (command name, base command)
- Parameter definitions (parsers, types, help messages)
- Parse configurations (determining how input is processed)
- Execution metadata (priority, confirmation requirements, background execution)
- Option configurations (access control, update/remove permissions)

### Base Commands

Command specifications can extend base commands defined in `app/spec/base/command.yml`:

- `platform`: Base command for platform-level operations with admin access
- `host`: Base command for host management operations
- `user`: Base command for user management with user-admin access
- `group`: Base command for group management with user-admin and config-admin access
- `config`: Base command for configuration management with config-admin access
- `state`: Base command for state variable management with config-admin access
- `module`: Base command for module management with module-admin access
- `schedule`: Base command for scheduled task management with schedule-admin access
- `notification`: Base command for notification system with notification-admin access
- `service`: Base command for service management with admin access
- `db`: Base command for database management with db-admin access
- `qdrant_admin`: Base command for Qdrant vector database management
- `cache`: Base command for cache management
- `log`: Base command for log management
- `scaling_event`: Base command for auto-scaling events with admin access
- `import`: Base command for data import operations
- `calculate`: Base command for calculation operations
- `dataset`: Base command for dataset management with data-admin access
- `gpu`: Base command for GPU resource management
- `ai`: Base command for AI operations with chat-user access
- `chat`: Base command for chat operations with chat-user access
- `agent`: Base command for service agents with admin access
- `cell`: Base command for cell agents (specialized agents with chat and AI capabilities)

These base commands provide common functionality and access control that commands inherit, ensuring consistency across the platform.

### Mixins

Commands can include reusable parameter sets through mixins defined in `app/spec/mixins/command.yml`:

- `service`: Provides parameters for background service management
- `log`: Adds parameters for log management and retention
- `scaling_event`: Provides scaling event functionality
- `db`: Adds parameters for database operations
- `qdrant`: Provides parameters for Qdrant vector database operations
- `config`: Adds parameters for configuration value management
- `platform`: Provides platform-level parameters
- `language_model`: Adds parameters for language model operations
- `agent`: Provides agent lifecycle parameters
- `cell`: Adds parameters for cell agent configuration
- `group`: Provides parameters for group management
- `module`: Adds parameters for module management and profiles
- `notification`: Provides parameters for notification system
- `message`: Adds parameters for inter-service messaging
- `chat`: Provides parameters for chat operations
- `schedule`: Adds parameters for scheduled task management
- `user`: Provides parameters for user management
- `dataset`: Adds parameters for dataset operations

These mixins allow commands to compose functionality without duplicating parameter definitions.

### Naming Conventions

- Files are named by their primary command or domain (e.g., `user.yml`, `module.yml`)
- Command identifiers use snake_case
- Parameter names follow Python conventions
- Flag names use kebab-case with double dashes (e.g., `--ignore-req`)

### File Organization

Files are organized by command domain or function:

- System commands (platform, config, state)
- Resource management (user, group, host, module)
- Data operations (import, calculate, dataset)
- Service management (service, agent, scaling)
- Monitoring (log, cache, qdrant)
- Communication (chat, message)
- Scheduling (schedule, notification)
- AI operations (ai, gpu)

### Domain-Specific Patterns

- Commands define parse configurations that specify which parameters to process
- Parameters define parsers (variable, variables, flag, fields) that determine input handling
- Priority values control command execution order in the command tree
- Background execution flags enable asynchronous processing through Celery
- Confirmation requirements protect destructive operations
- Access control is defined through groups_allowed properties
- Mixins provide reusable parameter sets for common functionality

## Developer Notes and Usage Tips

### Usage Tips

- When creating new commands, check existing specifications to understand inheritance patterns
- Command parameters should include clear help messages for user guidance
- Use existing mixins when they match the intended functionality to maintain consistency
- Priority values should be chosen to ensure proper command tree organization
- Background execution should be used for long-running operations to improve responsiveness
- Access control groups should be carefully considered for security

### Integration Points

These specifications integrate with:

- Code generation in `app/systems/commands/meta`
- Command processing in `app/commands`
- API endpoints in `app/systems/api/command`
- Profile orchestration in `app/profiles`

Changes to these files require restarting the development server to regenerate classes.

### AI Development Guidance

When generating or modifying command specifications:

- Maintain consistency with existing naming and structure patterns
- Ensure all required fields for each command type are properly specified
- Reference existing specifications as examples for new implementations
- Validate that parameter parsers and types are properly declared
- Use appropriate base commands and mixins when they match the intended functionality
- Follow established patterns for parse configurations and execution metadata
- Consider access control implications when defining groups_allowed properties
- Maintain proper priority values to ensure correct command tree organization
