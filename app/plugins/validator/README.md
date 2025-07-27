# Zimagi Validator Plugin Directory

## Overview

The `app/plugins/validator` directory contains plugin implementations that provide data validation capabilities for the Zimagi platform's data processing system. These validator plugins enable dynamic validation of data values during import and processing workflows, ensuring data integrity and consistency across the platform.

This directory plays a critical architectural role by providing swappable validation implementations that extend the platform's data quality assurance capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/validator.yml`. The plugins here are consumed by:

- **Developers** working on data processing and value validation
- **System administrators** configuring data quality workflows
- **AI models** analyzing and generating data validation components

## Directory Contents

### Files

| File         | Purpose                                                                                            | Format |
| ------------ | -------------------------------------------------------------------------------------------------- | ------ |
| base.py      | Implements the base validator provider class with core validation functionality and warning system | Python |
| date_time.py | Implements date/time validator provider for validating datetime values against specified formats   | Python |
| exists.py    | Implements existence validator provider for checking if referenced data exists                     | Python |
| number.py    | Implements number validator provider for validating numeric values with min/max constraints        | Python |
| string.py    | Implements string validator provider for validating string values with pattern matching            | Python |
| unique.py    | Implements uniqueness validator provider for ensuring values are unique within a dataset           | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Validator plugin interfaces are defined in `app/spec/plugins/validator.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import and processing commands
- **Data Models**: Integrates with `app/data` for data validation during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and processing

## Key Concepts and Patterns

### Plugin Architecture

The validator plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/validator.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of validation operations stored in this directory
- **Base Plugin** provides common functionality that all validator providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Validation Operations

All validator plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all validator providers extend
- **Value Validation**: Standardized value validation operations performed on input data
- **Record Context**: Access to complete record data for contextual validation
- **Error Handling**: Custom exception classes for validation operations

### Interface Definition

Based on the specification in `app/spec/plugins/validator.yml`, the validator plugin implements:

- **validate method**: Takes value parameter (any type) and record parameter (dict), returns boolean
- **Required id parameter**: String identifier for the validator
- **Providers**: date_time, exists, number, string, unique are the currently defined providers

### File Organization

Files are organized by validation operation:

- Each validator provider has its own file named by the operation (e.g., `string.py`, `number.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Validator provider files are named by their specific operation (e.g., `string.py`, `number.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All validator plugins extend base plugin classes from the dynamic generation system through `BaseProvider("validator", provider_name)`
- Plugins define validation logic in the `validate` method with typed parameters according to the specification
- Error handling uses custom exception classes for validation operations
- Value validation and error reporting are performed through the validator's warning method

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/validator.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Validator plugins are accessed through the indexing system using `BaseProvider("validator", provider_name)` function
- Implement validators by creating Python files with Provider classes that extend BaseProvider
- Use existing validators as templates for new implementations
- Follow established patterns for value validation and error handling
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/validator.yml` for generation

### AI Development Guidance

When generating or modifying validator plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with validator-specific exception classes
3. Follow established patterns for value validation and error reporting
4. Respect the separation of concerns between different validation operations
5. Consider performance implications for validation during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing validators as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/validator.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires a `validate` method with value (any) and record (dict) parameters that returns a boolean
12. Remember that all validators require an 'id' parameter as specified in the base requirements
