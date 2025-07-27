# Zimagi Text Splitter Plugin Directory

## Overview

The `app/plugins/text_splitter` directory contains plugin implementations that provide text segmentation capabilities for the Zimagi platform's natural language processing functionality. These text splitter plugins enable dynamic text chunking operations using various algorithms and libraries, allowing the platform to process large documents into manageable segments for AI analysis and processing.

This directory plays a critical architectural role by providing swappable text splitting implementations that extend the platform's NLP capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/text_splitter.yml`. The plugins here are consumed by:

- **Developers** working on AI and NLP features
- **System administrators** configuring text processing workflows
- **AI models** analyzing and generating text processing components

## Directory Contents

### Files

| File     | Purpose                                                                                   | Format |
| -------- | ----------------------------------------------------------------------------------------- | ------ |
| base.py  | Implements the base text splitter provider class with core text splitting functionality   | Python |
| spacy.py | Implements spaCy-based text splitter provider for intelligent sentence boundary detection | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Text splitter plugin interfaces are defined in `app/spec/plugins/text_splitter.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly AI-related commands
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and processing

## Key Concepts and Patterns

### Plugin Architecture

The text splitter plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/text_splitter.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of text splitting operations stored in this directory
- **Base Plugin** provides common functionality that all text splitter providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Text Splitting Operations

All text splitter plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all text splitter providers extend
- **Text Segmentation**: Standardized text splitting operations that convert large texts into smaller chunks
- **Model Integration**: Support for NLP libraries and models for intelligent text processing
- **Error Handling**: Custom exception classes for text splitting operations

### Interface Definition

Based on the specification in `app/spec/plugins/text_splitter.yml`, the text splitter plugin implements:

- **split method**: Takes text parameter (str) and returns list
- **Required model parameter**: String specifying the text splitter model
- **Optional validate parameter**: Boolean for sentence validation (defaults to true)
- **Optional max_sentence_length parameter**: Integer for maximum sentence length (defaults to 2000)

### File Organization

Files are organized by text splitting algorithm or implementation:

- Each text splitter provider has its own file named by the algorithm or specific implementation (e.g., `spacy.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Text splitter provider files are named by their specific implementation (e.g., `spacy.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All text splitter plugins extend base plugin classes from the dynamic generation system through `BaseProvider("text_splitter", provider_name)`
- Plugins define splitting logic in the `split` method with typed parameters according to the specification
- Error handling uses custom exception classes for text splitting operations
- Model loading and initialization are handled through provider-specific methods
- Text validation and preprocessing ensure proper input handling

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/text_splitter.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Text splitter plugins are accessed through the indexing system using `BaseProvider("text_splitter", provider_name)` function
- Implement text splitters by creating Python files with Provider classes that extend BaseProvider
- Use existing text splitters as templates for new implementations
- Follow established patterns for model loading and text segmentation
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/text_splitter.yml` for generation
- NLP libraries (spaCy) for text processing operations

### AI Development Guidance

When generating or modifying text splitter plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with text splitting-specific exception classes
3. Follow established patterns for model loading and text segmentation
4. Respect the separation of concerns between different text splitting algorithms
5. Consider performance implications for text splitting during NLP operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing text splitters as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/text_splitter.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires a `split` method with text (str) parameter that returns a list
