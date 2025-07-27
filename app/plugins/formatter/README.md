# Zimagi Formatter Plugin Directory

## Overview

The `app/plugins/formatter` directory contains plugin implementations that provide value formatting capabilities for the Zimagi platform's data processing system. These formatter plugins enable dynamic transformation of data values during import and processing workflows, allowing the platform to standardize, clean, and structure data according to specific requirements.

This directory plays a critical architectural role by providing swappable formatting implementations that extend the platform's data transformation capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/formatter.yml`. The plugins here are consumed by:

- **Developers** working on data processing and value formatting
- **System administrators** configuring data transformation workflows
- **AI models** analyzing and generating data formatting components

## Directory Contents

### Files

| File             | Purpose                                                                                 | Format |
| ---------------- | --------------------------------------------------------------------------------------- | ------ |
| base.py          | Implements the base formatter provider class with core formatting functionality         | Python |
| capitalize.py    | Implements capitalize formatter provider for capitalizing text values                   | Python |
| date.py          | Implements date formatter provider for parsing and formatting date values               | Python |
| date_time.py     | Implements date/time formatter provider for parsing and formatting datetime values      | Python |
| integer.py       | Implements integer formatter provider for converting values to integers                 | Python |
| joiner.py        | Implements joiner formatter provider for combining list/tuple values into strings       | Python |
| lower.py         | Implements lower formatter provider for converting text to lowercase                    | Python |
| number.py        | Implements number formatter provider for formatting numeric values                      | Python |
| remove_suffix.py | Implements remove suffix formatter provider for removing specified suffixes from values | Python |
| string.py        | Implements string formatter provider for converting values to strings                   | Python |
| title.py         | Implements title formatter provider for converting text to title case                   | Python |
| upper.py         | Implements upper formatter provider for converting text to uppercase                    | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Formatter plugin interfaces are defined in `app/spec/plugins/formatter.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import and processing commands
- **Data Models**: Integrates with `app/data` for data field processing during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters

## Key Concepts and Patterns

### Plugin Architecture

The formatter plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/formatter.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of formatting operations stored in this directory
- **Base Plugin** provides common functionality that all formatter providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Formatting Operations

All formatter plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all formatter providers extend
- **Value Formatting**: Standardized value transformation operations performed on input data
- **Record Context**: Access to complete record data for contextual formatting
- **Error Handling**: Custom exception classes for formatting operations

### Interface Definition

Based on the specification in `app/spec/plugins/formatter.yml`, the formatter plugin implements:

- **format method**: Takes value parameter (any type) and record parameter (dict), returns formatted value
- **Required id parameter**: String identifier for the formatter
- **Providers**: capitalize, date, date_time, integer, joiner, lower, number, remove_suffix, string, title, and upper are the currently defined providers

### File Organization

Files are organized by formatting operation:

- Each formatter provider has its own file named by the operation (e.g., `capitalize.py`, `number.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Formatter provider files are named by their specific operation (e.g., `capitalize.py`, `number.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All formatter plugins extend base plugin classes from the dynamic generation system through `BaseProvider("formatter", provider_name)`
- Plugins define formatting logic in the `format` method with typed parameters according to the specification
- Error handling uses custom exception classes for formatting operations
- Value validation and error reporting are performed through the formatter's error method

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/formatter.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Formatter plugins are accessed through the indexing system using `BaseProvider("formatter", provider_name)` function
- Implement formatters by creating Python files with Provider classes that extend BaseProvider
- Use existing formatters as templates for new implementations
- Follow established patterns for value formatting and error handling
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/formatter.yml` for generation

### AI Development Guidance

When generating or modifying formatter plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with formatter-specific exception classes
3. Follow established patterns for value formatting and transformation
4. Respect the separation of concerns between different formatting operations
5. Consider performance implications for formatting during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing formatters as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/formatter.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires a `format` method with value (any) and record (dict) parameters that returns a formatted value
12. Remember that all formatters require an 'id' parameter as specified in the base requirements
