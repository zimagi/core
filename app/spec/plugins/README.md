# Zimagi Plugin Specifications

## Overview

The `app/spec/plugins` directory contains YAML specification files that define the plugin architectures used throughout the Zimagi platform. These specifications serve as the foundation for the platform's meta-programming code generation system, enabling dynamic creation of plugin interfaces and provider implementations with minimal custom code.

This directory plays a critical role in Zimagi's "specification-driven development" approach, where YAML configurations are transformed into functional Python classes at runtime. The specifications defined here are consumed by the code generation system in `app/systems/plugins/meta` to create the plugin layer that powers extensible functionality across the platform.

The directory is used by:

- **Developers** to define and extend plugin functionality
- **Code generation systems** to create dynamic Python classes
- **AI models** analyzing and generating platform components

## Directory Contents

### Files

| File                | Purpose                                                                        | Format |
| ------------------- | ------------------------------------------------------------------------------ | ------ |
| calculation.yml     | Defines calculation plugin specifications for field value computations         | YAML   |
| channel_token.yml   | Specifies channel token plugin specifications for loading message data         | YAML   |
| config.yml          | Defines configuration plugin specifications                                    | YAML   |
| dataset.yml         | Specifies dataset plugin specifications for data collection and processing     | YAML   |
| encoder.yml         | Defines encoder plugin specifications for text encoding                        | YAML   |
| encryption.yml      | Specifies encryption plugin specifications for text encryption/decryption      | YAML   |
| field_processor.yml | Defines field processor plugin specifications for data field transformations   | YAML   |
| file_parser.yml     | Specifies file parser plugin specifications for parsing different file formats | YAML   |
| formatter.yml       | Defines formatter plugin specifications for value formatting                   | YAML   |
| function.yml        | Specifies function plugin specifications for executable functions              | YAML   |
| group.yml           | Defines group plugin specifications for role-based access control              | YAML   |
| language_model.yml  | Specifies language model plugin specifications for AI language processing      | YAML   |
| message_filter.yml  | Defines message filter plugin specifications for message filtering             | YAML   |
| module.yml          | Specifies module plugin specifications for module management                   | YAML   |
| parser.yml          | Defines parser plugin specifications for value parsing                         | YAML   |
| qdrant.yml          | Specifies qdrant plugin specifications for vector database operations          | YAML   |
| source.yml          | Defines source plugin specifications for data import sources                   | YAML   |
| task.yml            | Specifies task plugin specifications for executable tasks                      | YAML   |
| text_splitter.yml   | Defines text splitter plugin specifications for text segmentation              | YAML   |
| user.yml            | Specifies user plugin specifications                                           | YAML   |
| validator.yml       | Defines validator plugin specifications for value validation                   | YAML   |
| worker.yml          | Specifies worker plugin specifications for background processing               | YAML   |
| data_processor.yml  | Defines data processor plugin specifications for dataset transformations       | YAML   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory is part of the broader `app/spec` system which generates dynamic classes for the Zimagi platform. The plugin specifications defined here are consumed by:

- **Parent Context**: Part of the `app/spec` directory which contains all YAML specifications for the platform's meta-programming system
- **Code Generation**: Specifications are processed by systems in `app/systems/plugins/meta` to generate dynamic Python classes
- **Plugin Implementations**: Files in `app/plugins` reference these specifications in their definitions
- **Command Processing**: Command implementations in `app/commands` utilize plugin functionality
- **Data Import Systems**: Various modules implement source, validator, and formatter plugins based on these specifications

The generated classes are used throughout the application, particularly in:

- `app/systems/plugins` for plugin functionality
- `app/commands` for command execution with plugin integrations
- `app/data` for data processing with calculation and validation plugins

These specifications integrate with the meta-programming systems in `app/systems/plugins/meta` which transform YAML specifications into functional Python classes.

Additionally, plugin specifications work with:

- **Plugin Mixins**: The `app/spec/mixins/plugin.yml` file defines reusable parameter sets that can be included in plugin specifications
- **Base Plugins**: Files in `app/spec/base/` define foundational plugin structures that can be extended

## Key Concepts and Patterns

### Specification Structure

Each YAML file defines one or more plugin specifications that include:

- Plugin identification (plugin name, base plugin)
- Interface definitions (methods with parameters and return types)
- Required parameters (type, help message)
- Optional parameters with defaults
- Provider specifications with their own parameter sets
- Mixin references for shared functionality

### Base Plugins

Plugin specifications can extend base plugins defined in `app/spec/base/plugin.yml`:

- `base`: The most fundamental plugin interface with no predefined structure
- `data`: A plugin base that connects to data models
- `provider`: A plugin base that provides specific implementations

These base plugins provide common functionality that plugins inherit, ensuring consistency across the platform.

### Mixins

Plugins can include reusable parameter sets through mixins defined in `app/spec/mixins/plugin.yml`:

- `cli_task`: Provides parameters for command-line task execution with environment variables
- `ssh_task`: Adds parameters for SSH-based task execution including host, user, port, timeout, and authentication
- `csv_source`: Provides parameters for CSV data source handling
- `list_calculation`: Adds parameters for list-based calculations including minimum values and reverse ordering
- `module_template`: Provides parameters for module template handling including template usage and fields

These mixins allow plugins to compose functionality without duplicating parameter definitions.

### Providers

Each plugin specification defines a set of providers that implement the plugin interface with specific functionality. Providers can:

- Inherit from other providers using the `base` property
- Define their own required and optional parameters
- Include mixins for shared functionality
- Override default options with provider-specific values

### Naming Conventions

- Files are named by their primary plugin or domain (e.g., `source.yml`, `formatter.yml`)
- Specification identifiers use snake_case
- Parameter names follow Python conventions
- Provider names are descriptive and consistent with their function

### File Organization

Files are organized by plugin domain or function:

- Data processing plugins (source, formatter, validator, calculation)
- Task execution plugins (task, worker)
- AI and NLP plugins (encoder, language_model, text_splitter)
- System plugins (config, module, user, group)
- Specialized plugins (dataset, qdrant, channel_token, parser)

### Domain-Specific Patterns

- Plugins define interfaces that specify method signatures with typed parameters
- Parameters define type, help message, and optional default values
- Providers implement the plugin interface with specific functionality
- Mixins enable composition of common parameter sets across plugins

## Developer Notes and Usage Tips

### Usage Tips

- When creating new plugins, check existing specifications to understand inheritance patterns
- Plugin interfaces should define clear method signatures with well-documented parameters
- Use existing mixins when they match the intended functionality to maintain consistency
- Required parameters should have clear help messages for user guidance
- Provider parameters should be specific to the provider's implementation

### Integration Points

These specifications integrate with:

- Code generation in `app/systems/plugins/meta`
- Plugin implementations in `app/plugins`
- Command system in `app/commands`
- Data processing systems throughout the application

Changes to these files require restarting the development server to regenerate classes.

### AI Development Guidance

When generating or modifying plugin specifications:

- Maintain consistency with existing naming and structure patterns
- Ensure all required interface methods are properly specified
- Reference existing specifications as examples for new implementations
- Validate that parameter types and help messages are properly declared
- Use appropriate base plugins and mixins when they match the intended functionality
- Follow established patterns for provider inheritance and parameter definitions
