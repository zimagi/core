# Zimagi Message Filter Plugin Directory

## Overview

The `app/plugins/message_filter` directory contains plugin implementations that provide message filtering capabilities for the Zimagi platform's communication system. These message filter plugins enable dynamic filtering of message data during inter-service communication workflows, allowing for selective processing of messages based on specific criteria.

This directory plays a critical architectural role by providing swappable message filter implementations that extend the platform's messaging capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/message_filter.yml`. The plugins here are consumed by:

- **Developers** working on communication and messaging features
- **System administrators** configuring inter-service communication workflows
- **AI models** analyzing and generating messaging components

## Directory Contents

### Files

| File           | Purpose                                                                                                   | Format |
| -------------- | --------------------------------------------------------------------------------------------------------- | ------ |
| base.py        | Implements the base message filter provider class with core filtering functionality                       | Python |
| mentions_me.py | Implements mentions me message filter provider for filtering messages that mention the current agent user | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend the Zimagi platform's core functionality
- **Specifications**: Message filter plugin interfaces are defined in `app/spec/plugins/message_filter.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Communication Systems**: Works with `app/systems/communication` for inter-service messaging functionality
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters

## Key Concepts and Patterns

### Plugin Architecture

The message filter plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/message_filter.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of message filtering operations stored in this directory
- **Base Plugin** provides common functionality that all message filter providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Message Filter Interface

Based on the specification in `app/spec/plugins/message_filter.yml`, the message filter plugin implements:

- **filter method**: Takes message parameter (dict) and value parameter (int|float|str|bool), returns dict|null
- **Providers**: mentions_me is the currently defined provider

### Message Filter Processing

All message filter plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all message filter providers extend
- **Message Filtering**: Standardized message filtering operations performed on input data
- **Error Handling**: Custom exception handling for message filter operations (MessageFilterParseError)

### File Organization

Files are organized by message filter operation:

- Each message filter provider has its own file named by the operation it performs
- Base implementation is in `base.py`

### Naming Conventions

- Message filter provider files are named by their specific operation (e.g., `mentions_me.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`
- Exception classes follow the pattern `*Error` (e.g., `MessageFilterParseError`)

### Domain-Specific Patterns

- All message filter plugins extend base plugin classes from the dynamic generation system through `BaseProvider("message_filter", provider_name)`
- Plugins define filtering logic in the `filter` method with typed parameters according to the specification
- Error handling uses custom exception classes for message filter operations
- Message data filtering follows standardized patterns for communication processing

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/message_filter.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Message filter plugins are accessed through the indexing system using `BaseProvider("message_filter", provider_name)` function
- Implement message filters by creating Python files with Provider classes that extend BaseProvider
- Use existing message filters as templates for new implementations
- Follow established patterns for message filtering and data processing
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/message_filter.yml` for generation

### AI Development Guidance

When generating or modifying message filter plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with message filter-specific exception classes
3. Follow established patterns for message filtering and data processing operations
4. Respect the separation of concerns between different message filter operations
5. Consider performance implications for message filtering during communication workflows
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing message filters as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/message_filter.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires a `filter` method with message (dict) and value (int|float|str|bool) parameters that returns dict|null
