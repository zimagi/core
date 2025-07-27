# Zimagi Tasks Directory

## Overview

The `app/tasks` directory contains YAML configuration files that define executable tasks for the Zimagi platform. These task definitions provide a declarative approach to specifying command execution operations that can be run through the platform's task plugin system, enabling automation and routine operations without writing custom code.

This directory plays an architectural role by providing configuration-driven task execution capabilities, allowing developers and system administrators to define complex operations through YAML files. The tasks defined here integrate with the plugin system and are consumed by:

- **Developers** working on automation and testing workflows
- **System administrators** defining routine operational tasks
- **AI models** analyzing and generating task definitions

## Directory Contents

### Files

| File        | Purpose                                                                         | Format |
| ----------- | ------------------------------------------------------------------------------- | ------ |
| utility.yml | Defines utility tasks for common operations like echo, sleep, and wait commands | YAML   |
| zimagi.yml  | Defines Zimagi-specific tasks for testing migrations and database operations    | YAML   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Plugin Systems**: Tasks connect to `app/plugins/task` for provider implementations
- **Specifications**: Task definitions are based on specifications defined in `app/spec/plugins/task.yml`
- **Command Systems**: Integrates with `app/systems/commands` for execution context
- **Settings**: Uses configurations defined in `app/settings` for behavior parameters

## Key Concepts and Patterns

### Task Definition Structure

Each YAML file defines one or more task specifications that include:

- Task identification (task name)
- Provider specification that determines the execution method
- Requirements (mandatory parameters) and options (optional parameters with defaults)
- Default parameter values

### Provider-Based Execution

Tasks leverage the plugin system's task providers as defined in `app/spec/plugins/task.yml`:

- **command**: Executes shell commands with environment variable interpolation
- **script**: Runs local scripts with arguments and environment variables
- **remote_command**: Executes commands on remote hosts via SSH with environment variables
- **remote_script**: Uploads and executes scripts on remote hosts via SSH
- **upload**: Uploads files to remote hosts via SSH with permission settings

### Task Interface

All task providers implement a standardized interface:

- **get_fields()**: Returns a dictionary of field configurations for the task
- **execute(results, params)**: Core execution logic that performs the specific task operation

### Provider Requirements and Options

Each provider has specific requirements and options:

#### Command Provider

- **Requirement**: `command` (string) - The command string to execute
- **Options**:
  - `options` (dict, default: {}) - Command interpolation variables
  - `input` (string) - Command stdin string
  - `cwd` (string) - Current working directory for command execution
  - `display` (bool, default: true) - Whether to display command output
  - `sudo` (bool, default: false) - Run command with sudo permissions
  - `lock` (bool, default: false) - Lock task configuration options

#### Script Provider

- **Requirement**: `script` (string) - The script file name
- **Options**:
  - `args` (list, default: []) - Script arguments
  - `options` (dict, default: {}) - Script interpolation variables
  - `input` (string) - Script stdin string
  - `cwd` (string) - Current working directory for script execution
  - `display` (bool, default: true) - Whether to display script output
  - `sudo` (bool, default: false) - Run script with sudo permissions
  - `lock` (bool, default: false) - Lock task configuration options

#### Remote Command Provider

- **Requirement**: `command` (string) - The command string to execute
- **Options**:
  - `options` (dict, default: {}) - Command interpolation variables
  - `sudo` (bool, default: false) - Run command with sudo permissions
  - `lock` (bool, default: false) - Lock task configuration options

#### Remote Script Provider

- **Requirement**: `script` (string) - The script file name
- **Options**:
  - `args` (list, default: []) - Script arguments
  - `options` (dict, default: {}) - Command interpolation variables
  - `sudo` (bool, default: false) - Run script with sudo permissions
  - `lock` (bool, default: false) - Lock task configuration options

#### Upload Provider

- **Requirements**:
  - `file` (string) - Local file path
  - `remote_path` (string) - Remote file path
- **Options**:
  - `owner` (string) - File owner on remote machine
  - `group` (string) - File group on remote machine
  - `mode` (string, default: '644') - File mode on remote machine

### Mixins

Task providers can include reusable parameter sets through mixins:

- **cli_task**: Provides parameters for command-line task execution with environment variables
- **ssh_task**: Adds parameters for SSH-based task execution including host, user, port, timeout, and authentication

### Naming Conventions

- Files are named by their functional domain (e.g., `utility.yml`, `zimagi.yml`)
- Task identifiers use snake_case
- Provider names match the task plugin provider implementations
- Parameter names follow Python conventions

### File Organization

Files are organized by functional domain:

- Utility tasks in `utility.yml`
- Zimagi-specific tasks in `zimagi.yml`
- Domain-specific tasks in separate YAML files

### Domain-Specific Patterns

- Tasks define executable operations through YAML configuration following plugin specifications
- Parameters can have default values and are overridden at execution time
- Tasks support both local and remote execution contexts via SSH
- Task definitions integrate with the platform's plugin system for extensibility
- All tasks support common options like sudo permissions and parameter locking

## Developer Notes and Usage Tips

### Integration Requirements

These task definitions require:

- Proper plugin specification files in `app/spec/plugins/task.yml` for task generation
- Access to plugin systems in `app/systems/plugins` for provider loading
- Task provider implementations in `app/plugins/task` for execution functionality
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Define tasks by creating YAML files with task specifications following the plugin interface
- Use existing tasks as templates for new implementations
- Follow established patterns for provider selection and parameter definition
- Access task functionality through the command system or plugin manager

### Dependencies

- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Task provider implementations from `app/plugins/task` for execution
- Plugin specifications from `app/spec/plugins/task.yml` for generation
- Utility functions from `app/utility` for common operations

### AI Development Guidance

When generating or modifying task definitions:

1. Maintain consistency with the YAML-based task definition patterns following plugin specifications
2. Ensure proper provider selection for the intended execution method with appropriate requirements
3. Follow established patterns for parameter definition and default values as defined in specifications
4. Respect the separation of concerns between different task domains
5. Consider execution context requirements (local vs remote) and required mixins
6. Maintain consistency with existing naming and structure patterns
7. Reference existing task definitions as examples for new implementations
8. Ensure task definitions properly integrate with the plugin system through BaseProvider access
9. Follow the specification-driven approach where task behavior is defined through YAML rather than hardcoded implementations
10. Use appropriate mixins (cli_task, ssh_task) when they match the intended functionality
