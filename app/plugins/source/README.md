# Zimagi Source Plugin Directory

## Overview

The `app/plugins/source` directory contains plugin implementations that provide data import source capabilities for the Zimagi platform's data processing system. These source plugins enable dynamic data ingestion from various sources such as CSV files, databases, APIs, and other data formats during import workflows.

This directory plays a critical architectural role by providing swappable source implementations that extend the platform's data import capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/source.yml`. The plugins here are consumed by:

- **Developers** working on data import and source management features
- **System administrators** configuring data import workflows
- **AI models** analyzing and generating data import components

## Directory Contents

### Files

| File        | Purpose                                                                                                   | Format |
| ----------- | --------------------------------------------------------------------------------------------------------- | ------ |
| base.py     | Implements the base source provider class with core data import functionality and processing capabilities | Python |
| csv_file.py | Implements CSV file source provider for importing data from CSV files with customizable parsing options   | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Source plugin interfaces are defined in `app/spec/plugins/source.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import commands
- **Data Models**: Integrates with `app/data` for data processing during import operations
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and processing

## Key Concepts and Patterns

### Plugin Architecture

The source plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/source.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of source operations stored in this directory
- **Base Plugin** provides common functionality that all source providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Source Processing Operations

All source plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all source providers extend, providing core functionality like data loading, validation, and saving
- **Data Loading**: Standardized data loading operations that retrieve data from various sources
- **Context Management**: Support for context-based data processing with load_contexts, load_items, and load_item methods
- **Data Processing**: Comprehensive data processing pipeline with update_series, validate, and save methods
- **Field Mapping**: Support for field mapping and relationship management through get_map and get_relations methods

### File Organization

Files are organized by source type:

- Each source provider has its own file named by the source type it handles
- Base implementation is in `base.py`

### Naming Conventions

- Source provider files are named by their specific source type (e.g., `csv_file.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All source plugins extend base plugin classes from `systems.plugins.base` through the dynamic generation system
- Plugins define processing logic in methods like `load`, `load_contexts`, `load_items`, and `load_item`
- Error handling uses custom exception classes for source processing operations
- Data validation and field mapping are performed through configured validator and formatter plugins
- Support for batch processing and pagination through page_count configuration
- Integration with model facade pattern for data persistence

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/source.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Source plugins are accessed through the indexing system using `BaseProvider("source", provider_name)` function
- Implement sources by creating Python files with Provider classes that extend BaseProvider
- Use existing sources as templates for new implementations
- Follow established patterns for data loading and processing
- Access plugin functionality through the manager's get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/source.yml` for generation
- Validator and formatter plugins from `app/plugins/validator` and `app/plugins/formatter` for value processing
- Pandas library for data manipulation and DataFrame operations

### AI Development Guidance

When generating or modifying source plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with source-specific exception classes
3. Follow established patterns for data loading and processing operations
4. Respect the separation of concerns between different source types
5. Consider performance implications for data import processing
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing sources as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/source.yml` properly define the interface
