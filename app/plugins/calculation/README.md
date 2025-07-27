# Zimagi Calculation Plugin Directory

## Overview

The `app/plugins/calculation` directory contains plugin implementations that provide field value computation logic for the Zimagi platform's data processing system. These calculation plugins enable dynamic mathematical and statistical operations on data fields during import and processing workflows.

This directory plays a critical architectural role by providing swappable calculation implementations that extend the platform's data transformation capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/calculation.yml`. The plugins here are consumed by:

- **Developers** working on data processing and field calculations
- **System administrators** configuring data transformation workflows
- **AI models** analyzing and generating calculation components

## Directory Contents

### Files

| File              | Purpose                                                                                                     | Format |
| ----------------- | ----------------------------------------------------------------------------------------------------------- | ------ |
| base.py           | Implements the base calculation provider class with core calculation functionality and parameter processing | Python |
| addition.py       | Implements addition calculation provider for summing two values                                             | Python |
| cov.py            | Implements coefficient of variation calculation provider for statistical analysis                           | Python |
| division.py       | Implements division calculation provider for dividing two values                                            | Python |
| min_max_scale.py  | Implements min-max scaling calculation provider for normalizing values                                      | Python |
| multiplication.py | Implements multiplication calculation provider for multiplying two values                                   | Python |
| pchange.py        | Implements percentage change calculation provider for calculating relative differences                      | Python |
| stdev.py          | Implements standard deviation calculation provider for measuring data dispersion                            | Python |
| subtraction.py    | Implements subtraction calculation provider for finding differences between values                          | Python |
| zscore.py         | Implements z-score calculation provider for standardizing data points                                       | Python |

### Subdirectories

| Directory | Purpose                                                                 | Contents  |
| --------- | ----------------------------------------------------------------------- | --------- |
| functions | Contains mathematical function implementations for date/time operations | See below |

### Functions Subdirectory Contents

The `functions` subdirectory contains modules that implement mathematical functions for date and time operations:

| File    | Purpose                                                              | Format |
| ------- | -------------------------------------------------------------------- | ------ |
| date.py | Implements date and time parsing functions for temporal calculations | Python |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Calculation plugin interfaces are defined in `app/spec/plugins/calculation.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import and processing commands
- **Data Models**: Integrates with `app/data` for data field processing during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters

## Key Concepts and Patterns

### Plugin Architecture

The calculation plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/calculation.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of calculation operations stored in this directory
- **Base Plugin** provides common functionality that all calculation providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Calculation Processing

All calculation plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all calculation providers extend
- **Parameter Processing**: Standardized parameter collection and validation from data records
- **Value Computation**: Mathematical operations performed on input parameters
- **Result Validation**: Value validation through configured validator plugins
- **Result Formatting**: Optional value formatting through configured formatter plugins

### File Organization

Files are organized by calculation operation:

- Each calculation provider has its own file named by the operation (e.g., `addition.py`, `division.py`)
- Mathematical functions are grouped in the `functions` subdirectory
- Base implementation is in `base.py`

### Naming Conventions

- Calculation provider files are named by their specific operation (e.g., `addition.py`, `division.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Function files are named by their domain (e.g., `date.py`)
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All calculation plugins extend base plugin classes from `systems.plugins.base` through the dynamic generation system
- Plugins define calculation logic in the `calc` method with typed parameters
- Parameter data is processed through the ParameterData helper class
- Error handling uses custom exception classes for calculation operations (SilentException, ProcessException)
- Value validation and formatting are performed through external validator and formatter plugins

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/calculation.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Calculation plugins are accessed through the indexing system using `BaseProvider("calculation", provider_name)` function
- Implement calculations by creating Python files with Provider classes that extend BaseProvider
- Use existing calculations as templates for new implementations
- Follow established patterns for parameter processing and value computation
- Access plugin functionality through the manager's get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing and mathematical operations
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/calculation.yml` for generation
- Validator and formatter plugins from `app/plugins/validator` and `app/plugins/formatter` for value processing

### AI Development Guidance

When generating or modifying calculation plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with calculation-specific exception classes
3. Follow established patterns for parameter processing and value computation
4. Respect the separation of concerns between different calculation operations
5. Consider performance implications for calculation processing during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing calculations as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/calculation.yml` properly define the interface
