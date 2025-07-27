# Zimagi Task Plugin Directory

## Overview

The `app/plugins/task` directory contains plugin implementations that provide executable task capabilities for the Zimagi platform's automation and workflow system. These task plugins enable dynamic execution of various operations such as file uploads, remote commands, script execution, and custom tasks through a specification-driven plugin system.

This directory plays a critical architectural role by providing swappable task implementations that extend the platform's automation capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/task.yml`. The plugins here are consumed by:

- **Developers** working on automation and task execution features
- **System administrators** configuring task workflows
- **AI models** analyzing and generating task components

## Directory Contents

### Files

| File              | Purpose                                                                                    | Format |
| ----------------- | ------------------------------------------------------------------------------------------ | ------ |
| base.py           | Implements the base task provider class with core task functionality and result handling   | Python |
| command.py        | Implements command task provider for executing shell commands with environment variables   | Python |
| remote_command.py | Implements remote command task provider for executing commands on remote hosts via SSH     | Python |
| remote_script.py  | Implements remote script task provider for uploading and executing scripts on remote hosts | Python |
| script.py         | Implements script task provider for executing local scripts with arguments                 | Python |
| upload.py         | Implements upload task provider for uploading files to remote hosts via SSH                | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: Task plugin interfaces are defined in `app/spec/plugins/task.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly automation and workflow commands
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling, shell execution, and SSH operations
- **Mixin Systems**: Integrates with `app/plugins/mixins` for reusable functionality components like SSH task execution

## Key Concepts and Patterns

### Plugin Architecture

The task plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/task.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of task operations stored in this directory
- **Base Plugin** provides common functionality that all task providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### Task Execution Patterns

All task plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all task providers extend, providing core functionality like parameter interpolation, path resolution, and access control
- **Task Execution**: Standardized task execution operations that perform specific actions and return TaskResult objects
- **Parameter Handling**: Flexible parameter collection and interpolation from task configurations
- **Result Management**: Standardized TaskResult objects for consistent output handling
- **Error Handling**: Custom exception classes for task execution operations

### Provider Types

The directory implements several specialized task providers as defined in `app/spec/plugins/task.yml`:

- **Base Provider** (`base.py`): Provides core task functionality and serves as the foundation for all other providers, implementing interfaces like `get_fields` and `execute` with parameter validation and access control
- **Command Provider** (`command.py`): Executes shell commands locally with environment variable support and input handling, implementing requirements for `command` and options for `options`, `input`, `cwd`, `display`, `sudo`, and `lock`
- **Remote Command Provider** (`remote_command.py`): Executes commands on remote hosts via SSH with environment variable support, implementing requirements for `command` and options for `options`, `sudo`, and `lock`
- **Remote Script Provider** (`remote_script.py`): Uploads and executes scripts on remote hosts via SSH with argument interpolation, implementing requirements for `script` and options for `args`, `options`, `sudo`, and `lock`
- **Script Provider** (`script.py`): Executes local scripts with argument interpolation and environment variables, implementing requirements for `script` and options for `args`, `options`, `input`, `cwd`, `display`, `sudo`, and `lock`
- **Upload Provider** (`upload.py`): Uploads files to remote hosts via SSH with permission settings, implementing requirements for `file` and `remote_path` and options for `owner`, `group`, and `mode`

### Interface Implementation

According to the specification in `app/spec/plugins/task.yml`, task plugins implement the following interfaces:

- `get_fields()` - Returns a dictionary of field configurations for the task
- `execute(results, params)` - Core execution logic that performs the specific task operation and populates the results object

### File Organization

Files are organized by task provider implementation:

- Each task provider has its own file named by the provider type
- Base implementation is in `base.py`
- Specialized implementations are in provider-specific files

### Naming Conventions

- Task provider files are named by their specific implementation (e.g., `command.py`, `upload.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin file is named `base.py`

### Domain-Specific Patterns

- All task plugins extend base plugin classes from the dynamic generation system through `BaseProvider("task", provider_name)`
- Plugins define task logic in the `execute` method with typed parameters according to the specification
- Error handling uses custom exception classes for task operations
- Integration with SSH utilities for remote task execution
- Parameter interpolation and path resolution for file operations
- Access control through role-based permissions checking
- Result standardization through TaskResult objects
- Mixin integration for common functionality like CLI task execution and SSH operations

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/task.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for shell execution and SSH operations
- SSH libraries (paramiko) for remote operations

### Usage Patterns

- Task plugins are accessed through the indexing system using `BaseProvider("task", provider_name)` function
- Implement task providers by creating Python files with Provider classes that extend BaseProvider
- Use existing task providers as templates for new implementations
- Follow established patterns for parameter processing and task execution
- Access plugin functionality through the manager's get_provider() method or command.get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for shell execution and SSH operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/task.yml` for generation
- SSH libraries (paramiko) for remote operations
- Shell execution utilities for command execution

### AI Development Guidance

When generating or modifying task plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with task-specific exception classes
3. Follow established patterns for parameter processing and task execution
4. Respect the separation of concerns between different task types
5. Consider performance implications for task execution during automation workflows
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing task providers as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/task.yml` properly define the interface with correct parameter types and return values
11. Follow the interface specification that requires a `get_fields` method that returns dict, and an `execute` method with results (TaskResult) and params (dict) parameters that returns None
12. Use mixins where appropriate to share common functionality like CLI task execution and SSH operations
