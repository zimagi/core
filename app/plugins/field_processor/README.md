# Zimagi Field Processor Plugin Directory

## Overview

The `app/plugins/field_processor` directory contains plugin implementations that provide data field transformation capabilities for the Zimagi platform's data processing system. These field processor plugins enable dynamic manipulation of data fields during import and processing workflows, allowing for complex data transformations without custom code.

This directory plays a critical architectural role by providing swappable field processing implementations that extend the platform's data transformation capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/field_processor.yml`. The plugins here are consumed by:

- **Developers** working on data processing and field transformations
- **System administrators** configuring data transformation workflows
- **AI models** analyzing and generating data processing components

## Directory Contents

### Files

| File              | Purpose                                                                                                  | Format |
| ----------------- | -------------------------------------------------------------------------------------------------------- | ------ |
| base.py           | Implements the base field processor provider class with core processing functionality                    | Python |
| bool_to_number.py | Implements boolean to number conversion field processor for transforming boolean values to numeric (1/0) | Python |
| combined_text.py  | Implements combined text field processor for concatenating multiple text fields with separators          | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Field processor plugin interfaces are defined in `app/spec/plugins/field_processor.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import and processing commands
- **Data Models**: Integrates with `app/data` for data field processing during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters

## Key Concepts and Patterns

### Plugin Architecture

The field processor plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/field_processor.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of field processing operations stored in this directory
- **Base Plugin** provides common functionality that all field processor providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Field Processing Operations

All field processor plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all field processor providers extend
- **Field Transformation**: Standardized field data transformation operations performed on input datasets
- **Parameter Handling**: Flexible parameter collection and validation from data records
- **Result Validation**: Processed field data validation through configured validator plugins

### Interface Definition

Based on the specification in `app/spec/plugins/field_processor.yml`, the field processor plugin implements:

- **exec method**: Takes dataset parameter (pandas.DataFrame) and field_data parameter (pandas.Series), returns pandas.Series
- **Providers**: bool_to_number and combined_text are the currently defined providers

### File Organization

Files are organized by field processing operation:

- Each field processor provider has its own file named by the operation (e.g., `bool_to_number.py`, `combined_text.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Field processor provider files are named by their specific operation (e.g., `bool_to_number.py`, `combined_text.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All field processor plugins extend base plugin classes from the dynamic generation system through `BaseProvider("field_processor", provider_name)`
- Plugins define processing logic in the `exec` method with typed parameters according to the specification
- Error handling uses custom exception classes for field processing operations
- Value validation and formatting are performed through external validator and formatter plugins

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/field_processor.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Field processor plugins are accessed through the indexing system using `BaseProvider("field_processor", provider_name)` function
- Implement field processors by creating Python files with Provider classes that extend BaseProvider
- Use existing field processors as templates for new implementations
- Follow established patterns for parameter processing and field transformation
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/field_processor.yml` for generation
- Validator and formatter plugins from `app/plugins/validator` and `app/plugins/formatter` for value processing

### AI Development Guidance

When generating or modifying field processor plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with field processing-specific exception classes
3. Follow established patterns for parameter processing and field transformation
4. Respect the separation of concerns between different field processing operations
5. Consider performance implications for field processing during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing field processors as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/field_processor.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires an `exec` method with dataset (pandas.DataFrame) and field_data (pandas.Series) parameters that returns a pandas.Series
