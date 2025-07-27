# Zimagi Parser Plugin Directory

## Overview

The `app/plugins/parser` directory contains plugin implementations that provide value parsing capabilities for the Zimagi platform's data processing system. These parser plugins enable dynamic parsing and interpolation of configuration values, state variables, conditional expressions, function calls, data references, and token generation during command execution and data processing workflows.

This directory plays a critical architectural role by providing swappable parsing implementations that extend the platform's data transformation capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/parser.yml`. The plugins here are consumed by:

- **Developers** working on data processing and value parsing
- **System administrators** configuring data transformation workflows
- **AI models** analyzing and generating parsing components

## Directory Contents

### Files

| File                 | Purpose                                                                                                  | Format |
| -------------------- | -------------------------------------------------------------------------------------------------------- | ------ |
| base.py              | Implements the base parser provider class with core parsing functionality and interpolation capabilities | Python |
| config.py            | Implements configuration variable parser for accessing settings and config values with @ syntax          | Python |
| conditional_value.py | Implements conditional value parser for evaluating conditional expressions with ?> syntax                | Python |
| function.py          | Implements function parser for executing functions with # syntax and parameter processing                | Python |
| reference.py         | Implements reference parser for accessing data model references with & syntax                            | Python |
| state.py             | Implements state variable parser for accessing runtime state values with $ syntax                        | Python |
| token.py             | Implements token parser for generating and managing unique tokens with % syntax                          | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Parser plugin interfaces are defined in `app/spec/plugins/parser.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/systems/commands` for command plugin integrations, particularly data import and processing commands
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and processing

## Key Concepts and Patterns

### Plugin Architecture

The parser plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/parser.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of parsing operations stored in this directory
- **Base Plugin** provides common functionality that all parser providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Parsing Operations

All parser plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all parser providers extend, providing core functionality like data interpolation
- **Pattern Matching**: Standardized pattern recognition for specific syntax elements (@, $, #, &, ?, %)
- **Value Processing**: Standardized value transformation operations performed on input data
- **Context Integration**: Access to command context and configuration for value resolution

### Provider Weight System

The parser system implements a weight-based priority system as defined in `app/spec/plugins/parser.yml`:

- **conditional_value**: Weight 1 (highest priority)
- **function**: Weight 2
- **token**: Weight 5
- **state**: Weight 5
- **config**: Weight 5
- **reference**: Weight 95 (lowest priority, processes last)

This ensures proper parsing order where higher weight parsers process after lower weight ones.

### File Organization

Files are organized by parsing operation:

- Each parser provider has its own file named by the operation it performs (e.g., `config.py`, `state.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Parser provider files are named by their specific operation (e.g., `config.py`, `state.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All parser plugins extend base plugin classes from the dynamic generation system through `BaseProvider("parser", provider_name)`
- Plugins define parsing logic in the `parse` method with typed parameters according to the specification
- Error handling uses custom exception classes for parsing operations
- Regular expressions are used for pattern matching specific to each parser type
- Integration with command options and configuration systems for context-aware parsing
- Support for complex value interpolation through the base class `interpolate` method

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/parser.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Parser plugins are accessed through the indexing system using `BaseProvider("parser", provider_name)` function
- Implement parsers by creating Python files with Provider classes that extend BaseProvider
- Use existing parsers as templates for new implementations
- Follow established patterns for pattern matching and value processing
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing and regular expressions
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/parser.yml` for generation

### AI Development Guidance

When generating or modifying parser plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with parser-specific exception classes
3. Follow established patterns for pattern matching and value processing
4. Respect the separation of concerns between different parsing operations
5. Consider performance implications for parsing during data processing
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing parsers as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/parser.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires a `parse` method with value (str) parameter that returns processed results
12. Maintain proper weight values in specifications to ensure correct parsing order
