# Zimagi Mixins Specifications

## Overview

The `app/spec/mixins` directory contains YAML specification files that define reusable components used in Zimagi's meta-programming code generation system. These mixins provide modular, composable building blocks that can be combined to create complex data models, commands, and plugins without writing extensive custom code.

This directory plays a critical role in Zimagi's architecture by enabling the platform's "specification-driven development" approach, where YAML configurations are transformed into functional Python classes and database models at runtime. The mixins defined here serve as templates that encapsulate common functionality which can be inherited by concrete implementations throughout the system.

The directory is used by:

- **Developers** to define reusable components for data models, commands, and plugins
- **Code generation systems** in `app/systems/models/meta`, `app/systems/commands/meta`, and `app/systems/plugins/meta` to create dynamic Python classes
- **AI models** analyzing and generating platform components

## Directory Contents

### Files

| File        | Purpose                                                                                        | Format |
| ----------- | ---------------------------------------------------------------------------------------------- | ------ |
| command.yml | Defines command mixins that provide parameter sets and metadata for executable commands        | YAML   |
| data.yml    | Defines data model mixins that encapsulate common field sets and behaviors for database models | YAML   |
| plugin.yml  | Specifies plugin mixins that define interfaces and parameter sets for extensible functionality | YAML   |

## Cross-Referencing

This directory is part of the broader `app/spec` system which generates dynamic classes for the Zimagi platform. The mixins defined here are consumed by:

- **Parent Context**: Part of the `app/spec` directory which contains all YAML specifications for the platform's meta-programming system
- **Data Models**: Files in `app/data/*/models.py` reference data mixins in `data.yml` in their specifications
- **Commands**: Command implementations in `app/commands` utilize command mixins from `command.yml`
- **Plugins**: Plugin systems in `app/plugins` implement plugin mixins defined in `plugin.yml`
- **Code Generation**: Specifications are processed by systems in `app/systems/` to generate dynamic Python classes

The generated classes are used throughout the application, particularly in:

- `app/systems/api/data` for REST API endpoints
- `app/systems/commands` for command execution
- `app/systems/plugins` for plugin functionality

## Key Concepts and Patterns

### Mixin Types

1. **Data Mixins** (`data.yml`): Define reusable field sets for Django models including relationships, configuration fields, and provider patterns. These mixins encapsulate common database model structures that can be shared across multiple data models.

2. **Plugin Mixins** (`plugin.yml`): Specify parameter interfaces for swappable plugin implementations such as CLI tasks, SSH connections, and data sources. These define the contract that plugin implementations must follow.

3. **Command Mixins** (`command.yml`): Provide parameter definitions and metadata for command-line and API-executable commands. These mixins allow commands to inherit common parameters and functionality.

### Naming Conventions

- Files are named by their mixin category (data, plugin, command)
- Mixin identifiers use snake_case
- Field and parameter names follow Django conventions
- Class references use PascalCase
- Configuration names use UPPER*CASE with ZIMAGI* prefix when referenced as environment variables

### File Organization

Files are organized by mixin category:

- Data model related mixins in `data.yml`
- Plugin interface mixins in `plugin.yml`
- Command parameter mixins in `command.yml`

Each YAML file contains a top-level key that categorizes the mixins (e.g., `data_mixins`, `plugin_mixins`, `command_mixins`), with individual mixins defined as nested objects.

### Domain-Specific Patterns

- Mixins can extend other mixins using the `mixins` property, allowing for composition
- Fields define type, options, and metadata for Django model generation
- Parameters specify command-line and API interface elements with parsers, types, and help text
- Meta sections provide additional context for code generation including data relationships and priorities
- Requirements and options define mandatory and optional parameters with types and defaults

## Developer Notes and Usage Tips

### Usage Tips

- When creating new data models, check existing mixins in `data.yml` to avoid duplication and ensure consistency
- Command mixins in `command.yml` should focus on specific functionality domains to maintain modularity
- Plugin mixins in `plugin.yml` should define clear interfaces with well-documented parameters
- Always restart the development server after modifying mixin specifications to regenerate classes
- Use existing mixins as templates when creating new ones to maintain consistency

### Integration Points

These specifications integrate with:

- Code generation in `app/systems/models/meta`, `app/systems/commands/meta`, and `app/systems/plugins/meta`
- Django model creation in `app/data`
- Command processing in `app/commands`
- Plugin system in `app/plugins`
- API endpoints in `app/systems/api/data`

### AI Development Guidance

When generating or modifying mixin specifications:

- Maintain consistency with existing naming and structure patterns
- Ensure all required fields for each mixin type are properly specified
- Reference existing mixins as examples for new implementations
- Validate that mixin dependencies are properly declared using the `mixins` property
- Follow established patterns for parameter definitions, field specifications, and meta information
- Consider reusability and composition when designing new mixins
