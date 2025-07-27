# Zimagi Function Plugin Directory

## Overview

The `app/plugins/function` directory contains plugin implementations that provide executable function capabilities for the Zimagi platform's data processing system. These function plugins enable dynamic data transformation operations during import and processing workflows, allowing the platform to perform various computations, data manipulations, and value processing tasks.

This directory plays a critical architectural role by providing swappable function implementations that extend the platform's data transformation capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/function.yml`. The plugins here are consumed by:

- **Developers** working on data processing and value transformations
- **System administrators** configuring data transformation workflows
- **AI models** analyzing and generating data processing components

## Directory Contents

### Files

| File                            | Purpose                                                                                                               | Format |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------ |
| base.py                         | Implements the base function provider class with core execution functionality                                         | Python |
| capitalize.py                   | Implements capitalize function provider for capitalizing text values                                                  | Python |
| csv.py                          | Implements CSV function provider for parsing CSV-formatted strings into lists                                         | Python |
| data_atomic_fields.py           | Implements data atomic fields function provider for retrieving atomic fields from data models                         | Python |
| data_dynamic_fields.py          | Implements data dynamic fields function provider for retrieving dynamic fields from data models                       | Python |
| data_id.py                      | Implements data ID function provider for retrieving primary key field names from data models                          | Python |
| data_key.py                     | Implements data key function provider for retrieving unique key field names from data models                          | Python |
| data_query_fields.py            | Implements data query fields function provider for retrieving queryable fields from data models                       | Python |
| data_relation_fields.py         | Implements data relation fields function provider for retrieving relationship fields from data models                 | Python |
| data_reverse_relation_fields.py | Implements data reverse relation fields function provider for retrieving reverse relationship fields from data models | Python |
| data_scope_fields.py            | Implements data scope fields function provider for retrieving scope fields from data models                           | Python |
| default.py                      | Implements default function provider for providing default values when data is null or empty                          | Python |
| filter.py                       | Implements filter function provider for filtering dictionary data based on key-value criteria                         | Python |
| flatten.py                      | Implements flatten function provider for flattening nested list structures into single-level lists                    | Python |
| join.py                         | Implements join function provider for combining multiple elements into a single list                                  | Python |
| keys.py                         | Implements keys function provider for retrieving dictionary keys with optional prefixing                              | Python |
| lstrip.py                       | Implements left strip function provider for removing prefixes from string values                                      | Python |
| mock_data.py                    | Implements mock data function provider for loading mock data from YAML files                                          | Python |
| normalize.py                    | Implements normalize function provider for normalizing data values to standard formats                                | Python |
| prefix.py                       | Implements prefix function provider for adding prefixes to list values                                                | Python |
| random_keys.py                  | Implements random keys function provider for retrieving random dictionary keys                                        | Python |
| random_values.py                | Implements random values function provider for retrieving random values from lists                                    | Python |
| rstrip.py                       | Implements right strip function provider for removing suffixes from string values                                     | Python |
| split.py                        | Implements split function provider for splitting string values using regular expressions                              | Python |
| substitute.py                   | Implements substitute function provider for replacing text substrings                                                 | Python |
| time.py                         | Implements time function provider for generating formatted timestamp strings                                          | Python |
| time_range.py                   | Implements time range function provider for generating time period sequences                                          | Python |
| values.py                       | Implements values function provider for retrieving dictionary values with optional key paths                          | Python |
| value.py                        | Implements value function provider for retrieving nested dictionary values using dot notation                         | Python |
| calculations.py                 | Implements calculations function provider for retrieving calculation plugin names matching a pattern                  | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Function plugin interfaces are defined in `app/spec/plugins/function.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import and processing commands
- **Data Models**: Integrates with `app/data` for data processing during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and processing

## Key Concepts and Patterns

### Plugin Architecture

The function plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/function.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of function operations stored in this directory
- **Base Plugin** provides common functionality that all function providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Function Processing Operations

All function plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all function providers extend
- **Value Processing**: Standardized value transformation operations performed on input data
- **Parameter Handling**: Flexible parameter collection and validation from data records
- **Result Validation**: Processed value validation through configured validator plugins

### Interface Definition

Based on the specification in `app/spec/plugins/function.yml`, the function plugin implements:

- **exec method**: Takes variable parameters and returns processed results
- **Providers**: Multiple providers implementing different function operations including mock_data, data_id, data_key, data_atomic_fields, data_dynamic_fields, data_query_fields, data_scope_fields, data_relation_fields, data_reverse_relation_fields, calculations, flatten, keys, random_keys, random_values, filter, values, value, prefix, csv, join, split, lstrip, rstrip, capitalize, substitute, normalize, default, time, and time_range

### File Organization

Files are organized by function operation:

- Each function provider has its own file named by the operation it performs (e.g., `capitalize.py`, `split.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Function provider files are named by their specific operation (e.g., `capitalize.py`, `split.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All function plugins extend base plugin classes from the dynamic generation system through `BaseProvider("function", provider_name)`
- Plugins define processing logic in the `exec` method with typed parameters
- Error handling uses custom exception classes for function processing operations
- Value validation and formatting are performed through external validator and formatter plugins

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/function.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Function plugins are accessed through the indexing system using `BaseProvider("function", provider_name)` function
- Implement functions by creating Python files with Provider classes that extend BaseProvider
- Use existing functions as templates for new implementations
- Follow established patterns for parameter processing and value transformation
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/function.yml` for generation
- Validator and formatter plugins from `app/plugins/validator` and `app/plugins/formatter` for value processing

### AI Development Guidance

When generating or modifying function plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with function-specific exception classes
3. Follow established patterns for parameter processing and value transformation
4. Respect the separation of concerns between different function operations
5. Consider performance implications for function processing during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing functions as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/function.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires an `exec` method with variable parameters that returns processed results
