# Zimagi Base Specifications

## Overview

The `app/spec/base` directory contains foundational YAML specification files that define the core data models, commands, and plugins used throughout the Zimagi platform. These base specifications serve as the building blocks for the platform's meta-programming code generation system, enabling dynamic class creation for data models, command interfaces, and plugin architectures.

This directory plays a critical role in Zimagi's "specification-driven development" approach, where YAML configurations are transformed into functional Python classes and database models at runtime. The specifications here are extended and customized by modules to create specialized functionality without writing extensive custom code.

The base specifications are consumed by the Zimagi platform's code generation systems to create dynamic Python classes that power the data layer, command interfaces, and plugin architectures. This approach allows developers to define complex system components with minimal code while maintaining consistency and extensibility across the platform.

## Directory Contents

### Files

| File        | Purpose                                                                                                                | Format |
| ----------- | ---------------------------------------------------------------------------------------------------------------------- | ------ |
| command.yml | Defines base command specifications that establish foundational command structures and mixins used across the platform | YAML   |
| data.yml    | Contains base data model specifications that define foundational data structures and mixins for database models        | YAML   |
| plugin.yml  | Specifies base plugin definitions that provide foundational interfaces for extensible functionality                    | YAML   |

## Cross-Referencing

This directory is part of the broader `app/spec` system which generates dynamic classes for the Zimagi platform. The base specifications defined here are consumed by:

- Data models in `app/data/*/models.py` which reference these base specifications in their definitions
- Command implementations in `app/commands` that utilize base command structures
- Plugin systems in `app/plugins` that implement base plugin interfaces

The generated classes are used throughout the application, particularly in:

- `app/systems/api/data` for REST API endpoints
- `app/systems/commands` for command execution
- `app/systems/plugins` for plugin functionality

These specifications integrate with the meta-programming systems in `app/systems/models/meta`, `app/systems/commands/meta`, and `app/systems/plugins/meta` which transform YAML specifications into functional Python classes.

## Key Concepts and Patterns

### Specification Types

1. **Data Specifications** (`data.yml`): Define base data model structures including fields, relationships, and metadata for Django model generation. These specifications establish common patterns for data models such as named resources and identifier-based resources.

2. **Command Specifications** (`command.yml`): Establish base command structures with parameter definitions and metadata for executable commands. These include platform-level commands for user management, configuration, module management, and specialized commands for AI/chat functionality.

3. **Plugin Specifications** (`plugin.yml`): Provide base plugin interfaces with parameter sets for swappable functionality implementations. These define the contracts for various plugin types including data sources, validators, formatters, and task executors.

### Naming Conventions

- Files are named by their specification category (command, data, plugin)
- Specification identifiers use snake_case
- Field and parameter names follow Django conventions
- Class references use PascalCase

### File Organization

Files are organized by specification category:

- Data model related specifications in `data.yml`
- Command related specifications in `command.yml`
- Plugin related specifications in `plugin.yml`

Each YAML file contains a top-level key that categorizes the specifications (e.g., `command_base`, `data_base`, `plugin_base`), with individual specifications defined as nested objects.

### Domain-Specific Patterns

- Specifications can extend other specifications using the `base` property, allowing for inheritance
- Fields define type, options, and metadata for Django model generation
- Parameters specify command-line and API interface elements with parsers, types, and help text
- Meta sections provide additional context for code generation including data relationships and priorities

## Developer Notes and Usage Tips

### Usage Tips

- When creating new data models, check existing base specifications in `data.yml` to understand inheritance patterns and available mixins
- Command specifications in `command.yml` establish foundational command behaviors and parameter sets that can be extended
- Plugin specifications in `plugin.yml` define core interfaces that should be extended rather than modified directly
- Always restart the development server after modifying base specifications to regenerate classes
- Use existing specifications as templates when creating new ones to maintain consistency

### Integration Points

These specifications integrate with:

- Code generation in `app/systems/models/meta`, `app/systems/commands/meta`, and `app/systems/plugins/meta`
- Django model creation in `app/data`
- Command processing in `app/commands`
- Plugin system in `app/plugins`
- API endpoints in `app/systems/api/data`

### AI Development Guidance

When generating or modifying base specifications:

1. Maintain consistency with existing naming and structure patterns
2. Ensure all required fields for each specification type are properly specified
3. Reference existing specifications as examples for new implementations
4. Validate that specification dependencies are properly declared using the `base` or `mixins` properties
5. Follow established patterns for parameter definitions, field specifications, and meta information
6. Consider reusability and inheritance when designing new base specifications
