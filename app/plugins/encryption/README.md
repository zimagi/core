# Zimagi Encryption Plugin Directory

## Overview

The `app/plugins/encryption` directory contains plugin implementations that provide text encryption and decryption capabilities for the Zimagi platform's security functionality. These encryption plugins enable dynamic encryption operations using various algorithms and providers, allowing the platform to securely handle sensitive data during transmission and storage.

This directory plays a critical architectural role by providing swappable encryption implementations that extend the platform's security capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/encryption.yml`. The plugins here are consumed by:

- **Developers** working on security features and data protection
- **System administrators** configuring encryption workflows
- **AI models** analyzing and generating security components

## Directory Contents

### Files

| File           | Purpose                                                                                             | Format |
| -------------- | --------------------------------------------------------------------------------------------------- | ------ |
| base.py        | Implements the base encryption provider class with core encryption functionality and key management | Python |
| aes256.py      | Implements AES-256 encryption provider for symmetric key encryption operations                      | Python |
| aes256_user.py | Implements user-specific AES-256 encryption provider that uses user-based keys                      | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Encryption plugin interfaces are defined in `app/spec/plugins/encryption.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Encryption Systems**: Works with `app/systems/encryption` for cipher management and provider integration
- **Settings**: Uses configurations defined in `app/settings` for encryption behavior parameters
- **Command Systems**: Integrates with `app/commands` for command plugin integrations, particularly security-related commands

## Key Concepts and Patterns

### Plugin Architecture

The encryption plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/encryption.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of encryption operations stored in this directory
- **Base Plugin** provides common functionality that all encryption providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Encryption Interface

Based on the specification in `app/spec/plugins/encryption.yml`, the encryption plugin implements:

- **encrypt method**: Takes plain_text parameter (str|bytes) and returns bytes
- **decrypt method**: Takes cipher_text parameter (str) and decode parameter (bool), returns str|bytes
- **Required type parameter**: String specifying type of text being encrypted/decrypted (api, data, etc.)
- **Optional key parameter**: String encryption key (file path or string)
- **Optional decoder parameter**: String decoder to use when decoding encrypted text from byte arrays (defaults to utf-8)
- **Optional binary_marker parameter**: String binary marker for encoding/decoding binary content (defaults to <<<<-->BINARY<-->>>>)

### Encryption Processing

All encryption plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all encryption providers extend
- **Key Management**: Standardized key generation and handling from various sources (strings, files)
- **Text Encryption**: Standardized text encryption operations that convert strings to encrypted bytes
- **Text Decryption**: Standardized text decryption operations that convert encrypted bytes back to strings
- **Error Handling**: Custom exception classes for encryption operations

### File Organization

Files are organized by encryption algorithm or implementation:

- Each encryption provider has its own file named by the algorithm or specific implementation (e.g., `aes256.py`, `aes256_user.py`)
- Base implementation is in `base.py`

### Naming Conventions

- Encryption provider files are named by their specific implementation (e.g., `aes256.py`, `aes256_user.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All encryption plugins extend base plugin classes from the dynamic generation system through `BaseProvider("encryption", provider_name)`
- Plugins define encryption logic in the `encrypt` and `decrypt` methods with typed parameters according to the specification
- Key management and initialization are handled through the `initialize` method
- Error handling uses custom exception classes for encryption operations (EncryptionError)
- Value preprocessing and postprocessing handle binary data encoding/decoding

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/encryption.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Encryption plugins are accessed through the indexing system using `BaseProvider("encryption", provider_name)` function
- Implement encryption providers by creating Python files with Provider classes that extend BaseProvider
- Use existing encryption providers as templates for new implementations
- Follow established patterns for key management and text encryption/decryption
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing and cryptographic operations (pycryptodome)
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/encryption.yml` for generation

### AI Development Guidance

When generating or modifying encryption plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with encryption-specific exception classes
3. Follow established patterns for key management and text encryption/decryption
4. Respect the separation of concerns between different encryption algorithms
5. Consider performance implications for encryption processing during data operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing encryption providers as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/encryption.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires encrypt method with plain_text (str|bytes) parameter that returns bytes, and decrypt method with cipher_text (str) and decode (bool) parameters that returns str|bytes
