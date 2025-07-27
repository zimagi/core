# Zimagi Dataset Plugin Directory

## Overview

The `app/plugins/dataset` directory contains plugin implementations that provide dataset collection and processing capabilities for the Zimagi platform's data management system. These dataset plugins enable dynamic data collection operations, time-series data handling, and data aggregation workflows during import and processing operations.

This directory plays a critical architectural role by providing swappable dataset implementations that extend the platform's data collection capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/dataset.yml`. The plugins here are consumed by:

- **Developers** working on data collection and dataset management
- **System administrators** configuring data collection workflows
- **AI models** analyzing and generating data collection components

## Directory Contents

### Files

| File          | Purpose                                                                                                     | Format |
| ------------- | ----------------------------------------------------------------------------------------------------------- | ------ |
| base.py       | Implements the base dataset provider class with core dataset functionality and data processing capabilities | Python |
| collection.py | Implements collection dataset provider for basic data collection operations                                 | Python |
| period.py     | Implements period dataset provider for time-series data handling and temporal data processing               | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Dataset plugin interfaces are defined in `app/spec/plugins/dataset.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import and dataset commands
- **Data Models**: Integrates with `app/data` for dataset management and data processing during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters

## Key Concepts and Patterns

### Plugin Architecture

The dataset plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/dataset.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of dataset operations stored in this directory
- **Base Plugin** provides common functionality that all dataset providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Dataset Processing

All dataset plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all dataset providers extend
- **Data Collection**: Standardized data collection operations from various sources
- **Time Series Handling**: Specialized temporal data processing capabilities
- **Data Aggregation**: Data combination and processing workflows

### File Organization

Files are organized by dataset operation:

- Each dataset provider has its own file named by the operation (e.g., `collection.py`, `period.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Dataset provider files are named by their specific operation (e.g., `collection.py`, `period.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All dataset plugins extend base plugin classes from the dynamic generation system through `BaseProvider("dataset", provider_name)`
- Plugins define processing logic in the `exec` method with typed parameters according to the specification
- Error handling uses custom exception classes for dataset operations
- Data processing follows standardized patterns for temporal and collection operations

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/dataset.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Dataset plugins are accessed through the indexing system using `BaseProvider("dataset", provider_name)` function
- Implement datasets by creating Python files with Provider classes that extend BaseProvider
- Use existing datasets as templates for new implementations
- Follow established patterns for data collection and processing
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing and mathematical operations
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/dataset.yml` for generation

### AI Development Guidance

When generating or modifying dataset plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with dataset-specific exception classes
3. Follow established patterns for data collection and processing operations
4. Respect the separation of concerns between different dataset operations
5. Consider performance implications for dataset processing during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing datasets as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/dataset.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires an `exec` method with dataset (pandas.DataFrame) and options (dict) parameters that returns a pandas.DataFrame
