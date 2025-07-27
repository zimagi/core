# Zimagi Module Plugin Directory

## Overview

The `app/plugins/module` directory contains plugin implementations that provide module management capabilities for the Zimagi platform's extensible module system. These module plugins enable dynamic module provisioning, version control, and deployment operations using various source control systems and local management strategies.

This directory plays a critical architectural role by providing swappable module provider implementations that extend the platform's module management capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/module.yml`. The plugins here are consumed by:

- **Developers** working on module management and deployment features
- **System administrators** configuring module provisioning workflows
- **AI models** analyzing and generating module management components

## Directory Contents

### Files

| File      | Purpose                                                                      | Format |
| --------- | ---------------------------------------------------------------------------- | ------ |
| base.py   | Implements the base module provider class with core module functionality     | Python |
| core.py   | Implements the core module provider for managing the main application module | Python |
| git.py    | Implements Git-based module provider for remote repository management        | Python |
| github.py | Implements GitHub-specific module provider with deploy key management        | Python |
| local.py  | Implements local module provider for development and testing                 | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Module plugin interfaces are defined in `app/spec/plugins/module.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands/module` for module command implementations
- **Settings**: Uses configurations defined in `app/settings` for module behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for filesystem operations and Git management

## Key Concepts and Patterns

### Plugin Architecture

The module plugin system implements a specification-driven approach to plugin generation:

- **Plugin Specification** defined in `app/spec/plugins/module.yml` that specifies the base plugin interface with profile and task management capabilities
- **Providers** are concrete implementations of module operations stored in this directory
- **Base Plugin** provides common functionality that all module providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Module Plugin Interface

Based on the specification in `app/spec/plugins/module.yml`, the module plugin implements:

- **get_profile_class method**: Returns systems.command.profile.CommandProfile class
- **get_profile method**: Takes profile_name (char) and show_options (bool) parameters, returns CommandProfile instance
- **run_profile method**: Takes profile_name (char), config (dict), components (list), display_only (bool), plan (bool), and ignore_missing (bool) parameters
- **export_profile method**: Takes components (list) parameter
- **destroy_profile method**: Takes profile_name (char), config (dict), components (list), display_only (bool), and ignore_missing (bool) parameters
- **import_tasks method**: Takes tasks_path (char) parameter, returns dict
- **get_task method**: Takes task_name (char) and show_options (bool) parameters, returns plugins.task.base.BaseProvider instance
- **exec_task method**: Takes task_name (char) and params (dict) parameters

### Provider Types

The directory implements several specialized module providers as defined in `app/spec/plugins/module.yml`:

- **Base Provider** (`base.py`): Provides core module functionality and serves as the foundation for all other providers
- **Core Provider** (`core.py`): Manages the core application module with special path handling
- **Git Provider** (`git.py`): Handles Git-based remote repositories with authentication support, implementing requirements for `remote` and options for `reference`, `username`, `password`, `public_key`, and `private_key`
- **GitHub Provider** (`github.py`): Specialized GitHub integration with deploy key management, extending the git provider with additional GitHub-specific functionality
- **Local Provider** (`local.py`): Local filesystem-based module management for development, implementing the `module_template` mixin

### File Organization

Files are organized by module provider implementation:

- Each module provider has its own file named by the provider type
- Base implementation is in `base.py`
- Specialized implementations are in provider-specific files

### Naming Conventions

- Module provider files are named by their specific implementation (e.g., `git.py`, `github.py`, `local.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All module plugins extend base plugin classes from the dynamic generation system through `BaseProvider("module", provider_name)`
- Plugins implement standardized interface methods for module operations as defined in the specification
- Error handling uses custom exception classes for module operations
- Integration with Git and GitHub APIs for remote repository management
- Template provisioning and file system operations for module initialization
- Authentication and credential management for remote providers
- Profile and task management for module orchestration

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/module.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for filesystem and Git operations
- Git libraries (pygit2) for repository operations
- GitHub API library for GitHub integration

### Usage Patterns

- Module plugins are accessed through the indexing system using `BaseProvider("module", provider_name)` function
- Implement module providers by creating Python files with Provider classes that extend BaseProvider
- Use existing module providers as templates for new implementations
- Follow established patterns for module path management and version control
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for filesystem and Git operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/module.yml` for generation
- Git libraries (pygit2) for repository operations
- GitHub API library (github) for GitHub integration
- PyYAML for configuration file parsing

### AI Development Guidance

When generating or modifying module plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with module-specific exception classes
3. Follow established patterns for module path management and template provisioning
4. Respect the separation of concerns between different module provider types
5. Consider performance implications for module operations during provisioning
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing module providers as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/module.yml` properly define the interface with correct parameter types and return values
11. Implement all required interface methods as specified: get_profile_class, get_profile, run_profile, export_profile, destroy_profile, import_tasks, get_task, exec_task
12. Use mixins where appropriate to share common functionality (e.g., module_template mixin)
