# Zimagi Plugins Directory

## Overview

The `app/plugins` directory contains plugin implementations that extend the Zimagi platform's core functionality through a dynamic, specification-driven plugin system. These plugins provide swappable implementations for various features such as data import sources, field validation, value formatting, calculations, and more.

This directory plays a critical architectural role by providing a modular extension system that allows Zimagi to be customized and enhanced without modifying core code. The plugins work with the dynamic class generation system in `app/systems/plugins/index.py` to create runtime plugin classes based on specifications in `app/spec/plugins`. The plugins here are consumed by:

- **Developers** working on extending platform functionality
- **System administrators** configuring plugin-based features
- **AI models** analyzing and generating plugin components

## Directory Contents

### Files

| File    | Purpose                                                              | Format |
| ------- | -------------------------------------------------------------------- | ------ |
| base.py | Implements base plugin classes and foundational plugin functionality | Python |
| data.py | Implements data plugin functionality for model instance management   | Python |

### Subdirectories

| Directory         | Purpose                                                                     | Contents                                                                            |
| ----------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| calculation       | Contains calculation plugin providers for field value computations          | Calculation providers like addition, subtraction, division, etc.                    |
| channel_token     | Contains channel token plugin providers for loading message data            | Channel token providers for data type parsing                                       |
| dataset           | Contains dataset plugin providers for data collection and processing        | Dataset providers like period, collection                                           |
| encoder           | Contains encoder plugin providers for text encoding                         | Text encoding providers like transformer, deepinfra, litellm                        |
| encryption        | Contains encryption plugin providers for text encryption/decryption         | Encryption providers like aes256, aes256_user                                       |
| field_processor   | Contains field processor plugin providers for data field transformations    | Field processing providers like combined_text, bool_to_number                       |
| file_parser       | Contains file parser plugin providers for parsing different file formats    | File parsing providers like txt, pdf, docx, binary                                  |
| formatter         | Contains formatter plugin providers for value formatting                    | Formatting providers like string, number, date, capitalize, etc.                    |
| function          | Contains function plugin providers for executable functions                 | Function providers like default, split, time, mock_data, etc.                       |
| group             | Contains group plugin providers for role-based access control               | Base group provider implementation                                                  |
| language_model    | Contains language model plugin providers for AI language processing         | Language model providers like litellm, transformer                                  |
| message_filter    | Contains message filter plugin providers for message filtering              | Message filtering providers like mentions_me                                        |
| mixins            | Contains reusable plugin functionality components                           | Plugin mixins like cli_task, ssh_task, list_calculation, module_template            |
| module            | Contains module plugin providers for module management                      | Module providers like git, github, local, core                                      |
| notification      | Contains notification plugin providers for notification system              | Base notification provider implementation                                           |
| parser            | Contains parser plugin providers for value parsing                          | Parsing providers like state, function, conditional_value, reference, config, token |
| qdrant            | Contains qdrant plugin providers for vector database operations             | Base qdrant provider implementation                                                 |
| qdrant_collection | Contains qdrant collection plugin providers for vector database collections | Qdrant collection providers like chat                                               |
| source            | Contains source plugin providers for data import sources                    | Data source providers like csv_file                                                 |
| task              | Contains task plugin providers for executable tasks                         | Task providers like upload, remote_command, command, script, etc.                   |
| text_splitter     | Contains text splitter plugin providers for text segmentation               | Text splitting providers like spacy                                                 |
| user              | Contains user plugin providers for user management                          | Base user provider implementation                                                   |
| validator         | Contains validator plugin providers for value validation                    | Validation providers like string, number, exists, unique, date_time                 |
| worker            | Contains worker plugin providers for background processing                  | Worker providers like base, docker, kubernetes                                      |
| data_processor    | Contains data processor plugin providers for dataset transformations        | Data processing providers like base, shuffle, drop_duplicates, sort                 |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Specifications**: Plugin interfaces are defined in `app/spec/plugins` which drive the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins/index.py` for dynamic plugin generation and provider loading using the BasePlugin, BaseProvider, and ProviderMixin functions
- **Command Systems**: Works with `app/commands` for command plugin integrations
- **Data Models**: Integrates with `app/data` for data plugin functionality
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters

## Key Concepts and Patterns

### Plugin Architecture

The plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins` that specify interfaces and provider structures
- **Providers** are concrete implementations of plugin types with specific functionality stored in this directory
- **Base Plugins** provide common functionality that plugins inherit through the BasePlugin and BaseProvider classes
- **Mixins** enable composition of shared functionality across plugins through the ProviderMixin system
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Plugin Generation System

The plugin system uses dynamic class generation through the indexing system:

- **BasePlugin(plugin_name)**: Creates or retrieves base plugin classes for plugin types
- **BaseProvider(plugin_name, provider_name)**: Creates or retrieves provider implementations for specific plugin providers
- **ProviderMixin(mixin_name)**: Creates or retrieves plugin mixin classes for shared functionality
- **Specification-Driven**: Plugin behavior is defined through YAML specifications in `app/spec/plugins` rather than hardcoded implementations

The indexing system in `app/systems/plugins/index.py` handles:

- Parsing plugin specifications from YAML files
- Dynamically generating Python classes at runtime
- Managing class inheritance hierarchies
- Handling plugin dependencies and base classes
- Providing access to plugin metadata and interfaces

### File Organization

Files are organized by plugin domain or function:

- Each plugin type has its own subdirectory (e.g., `formatter`, `validator`, `source`)
- Related plugins are grouped in the same directory by functional domain
- Mixins are stored in the `mixins` subdirectory for shared functionality
- Base implementations are in top-level plugin directories

### Naming Conventions

- Plugin directories are named by their functional domain (e.g., `source`, `formatter`, `validator`)
- Plugin provider files are named by their specific implementation (e.g., `csv_file.py`, `string.py`, `addition.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Mixin files are suffixed with the functional area they support (e.g., `cli_task.py`, `ssh_task.py`)
- Base plugin files are named `base.py` in each plugin type directory
- Class names follow PascalCase conventions with dynamic suffixes (e.g., `Dynamic`, `BaseProvider`, `Provider`)

### Domain-Specific Patterns

- All plugins extend base plugin classes from `systems.plugins.base` through the dynamic generation system
- Plugins define interfaces in specifications that specify method signatures with typed parameters
- Providers implement plugin interfaces with specific functionality
- Mixins enable composition of common functionality across plugins using the ProviderMixin system
- Error handling uses custom exception classes for plugin operations
- Plugin configurations are processed through specification-defined requirements and options
- Dynamic class generation follows a two-stage process: base class creation and overlay class creation

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins` for plugin generation
- Access to plugin systems in `app/systems/plugins/index.py` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Plugins are accessed through the indexing system using `BasePlugin()`, `BaseProvider()`, and `ProviderMixin()` functions from `app/systems/plugins/index.py`
- Implement providers by creating Python files in the appropriate plugin type directory
- Use existing plugins as templates for new implementations
- Follow established patterns for provider configuration and initialization through the spec system
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins/index.py` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins` for generation

### AI Development Guidance

When generating or modifying plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with plugin-specific exception classes
3. Follow established patterns for provider-based plugin implementations
4. Respect the separation of concerns between different plugin domains
5. Consider performance implications for plugin loading and execution
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing plugins as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins` properly define the interface
11. Understand the two-stage class generation process (dynamic base classes and overlay classes)
12. Follow the metadata structure defined in plugin specifications for requirements and options
