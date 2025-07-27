# Zimagi Language Model Plugin Directory

## Overview

The `app/plugins/language_model` directory contains plugin implementations that provide language model capabilities for the Zimagi platform's AI functionality. These language model plugins enable dynamic text generation and processing operations using various AI models and services, allowing the platform to perform natural language processing tasks.

This directory plays a critical architectural role by providing swappable language model implementations that extend the platform's AI capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/language_model.yml`. The plugins here are consumed by:

- **Developers** working on AI and NLP features
- **System administrators** configuring AI processing workflows
- **AI models** analyzing and generating language processing components

## Directory Contents

### Files

| File           | Purpose                                                                                                      | Format |
| -------------- | ------------------------------------------------------------------------------------------------------------ | ------ |
| base.py        | Implements the base language model provider class with core language model functionality and result handling | Python |
| litellm.py     | Implements LiteLLM library-based language model provider with support for multiple model providers           | Python |
| transformer.py | Implements HuggingFace transformer-based language model provider with device-specific execution              | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Language model plugin interfaces are defined in `app/spec/plugins/language_model.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly AI-related commands
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and processing

## Key Concepts and Patterns

### Plugin Architecture

The language model plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/language_model.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of language model operations stored in this directory
- **Base Plugin** provides common functionality that all language model providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Language Model Processing

All language model plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all language model providers extend, providing core functionality like message formatting
- **Text Generation**: Standardized text generation operations that convert prompts to responses with proper message formatting
- **Model Interface**: Consistent interface implementation for context length, token counting, and execution
- **Result Handling**: Standardized LanguageModelResult objects for consistent output formatting
- **Error Handling**: Custom exception classes for language model operations

### Interface Definition

Based on the specification in `app/spec/plugins/language_model.yml`, the language model plugin implements:

- **exec method**: Takes messages parameter (list) and returns LanguageModelResult
- **get_context_length method**: Returns int representing model's maximum context length
- **get_token_count method**: Takes messages parameter (list|str) and returns int token count
- **get_max_new_tokens method**: Returns int representing maximum new tokens
- **get_max_tokens method**: Returns int representing maximum tokens
- **Required model parameter**: String specifying the model identifier
- **Optional output_token_percent parameter**: Float for output token percentage (defaults to 0.3)

### File Organization

Files are organized by language model implementation:

- Each language model provider has its own file named by the service or library it uses
- Base implementation is in `base.py`

### Naming Conventions

- Language model provider files are named by their specific implementation (e.g., `litellm.py`, `transformer.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All language model plugins extend base plugin classes from the dynamic generation system through `BaseProvider("language_model", provider_name)`
- Plugins implement standardized interface methods: `get_context_length`, `get_token_count`, `get_max_new_tokens`, `get_max_tokens`, and `exec`
- Error handling uses custom exception classes for language model operations
- Model initialization and caching is implemented for performance optimization
- Token counting and context management ensure proper input/output handling
- Message formatting standardizes input handling for different message formats

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/language_model.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Language model plugins are accessed through the indexing system using `BaseProvider("language_model", provider_name)` function
- Implement language models by creating Python files with Provider classes that extend BaseProvider
- Use existing language models as templates for new implementations
- Follow established patterns for model initialization and text generation
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/language_model.yml` for generation
- Third-party AI libraries (litellm, transformers, torch) for model execution

### AI Development Guidance

When generating or modifying language model plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with language model-specific exception classes
3. Follow established patterns for text generation and model initialization
4. Respect the separation of concerns between different language model implementations
5. Consider performance implications for language model processing during AI operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing language models as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/language_model.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires exec method with messages (list) parameter that returns LanguageModelResult, get_context_length method that returns int, get_token_count method with messages (list|str) parameter that returns int, get_max_new_tokens method that returns int, and get_max_tokens method that returns int
