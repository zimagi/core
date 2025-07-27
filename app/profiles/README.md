# Zimagi Profiles Directory

## Overview

The `app/profiles` directory contains YAML command profiles that define orchestrated sequences of operations within the Zimagi platform. These profiles enable users to execute complex workflows by chaining together multiple commands, configurations, and operations through a declarative syntax.

This directory plays a critical architectural role by providing a high-level abstraction layer for automation and system management. Rather than executing individual commands manually, profiles allow developers and system administrators to define comprehensive operational procedures that can be executed consistently across different environments.

The profiles are consumed by:

- **Developers** working on automation and testing workflows
- **System administrators** managing platform deployments and operations
- **AI models** analyzing and generating workflow components

## Directory Contents

### Files

| File                  | Purpose                                                                     | Format |
| --------------------- | --------------------------------------------------------------------------- | ------ |
| display.yml           | Defines field display configurations for various data types in the platform | YAML   |
| migrate.yml           | Profile for database migration operations during platform initialization    | YAML   |
| test.yml              | Main test profile orchestrating various test scenarios and configurations   | YAML   |
| test/base.yml         | Base test profile configuration with common test settings                   | YAML   |
| test/cache.yml        | Profile for testing cache management operations                             | YAML   |
| test/config.yml       | Profile for testing configuration management operations                     | YAML   |
| test/dataset.yml      | Profile for testing dataset operations                                      | YAML   |
| test/dependency.yml   | Profile for testing dependency resolution and execution ordering            | YAML   |
| test/failure.yml      | Profile for testing failure scenarios and error handling                    | YAML   |
| test/group.yml        | Profile for testing group management operations                             | YAML   |
| test/host.yml         | Profile for testing host management operations                              | YAML   |
| test/log.yml          | Profile for testing log management operations                               | YAML   |
| test/module.yml       | Profile for testing module management operations                            | YAML   |
| test/notification.yml | Profile for testing notification system operations                          | YAML   |
| test/schedule.yml     | Profile for testing scheduled task operations                               | YAML   |
| test/state.yml        | Profile for testing state management operations                             | YAML   |
| test/task.yml         | Profile for testing task execution operations                               | YAML   |
| test/user.yml         | Profile for testing user management operations                              | YAML   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Command Systems**: Profiles connect to `app/commands` for executable command implementations
- **Component Systems**: Works with `app/components` for profile component processors
- **Specifications**: Integrates with command specifications defined in `app/spec/commands`
- **Test Systems**: Connects to `app/tests` for automated testing workflows

## Key Concepts and Patterns

### Profile Architecture

Profiles implement a declarative approach to workflow orchestration:

- **YAML-based Definition**: Profiles are defined using YAML syntax with a structured hierarchy
- **Operation Chaining**: Commands are executed in a defined sequence with dependency management
- **Conditional Execution**: Support for conditional operation execution based on previous results
- **Parameter Interpolation**: Dynamic parameter substitution using configuration values and function results

### Profile Structure

Each profile follows a consistent structure with these key sections:

- **Configuration**: Defines variables and settings used throughout the profile
- **Pre-run Operations**: Setup operations executed before main profile execution
- **Run Operations**: Main execution sequence of commands and operations
- **Post-run Operations**: Cleanup and finalization operations after execution
- **Destroy Operations**: Special operations for resource cleanup and teardown

### Naming Conventions

- Files are named by their functional domain (e.g., `test/cache.yml`, `test/log.yml`)
- Profile identifiers use snake_case following Zimagi's naming conventions
- Test profiles are organized in the `test` subdirectory with descriptive names
- Configuration keys and variables use snake_case for consistency

### File Organization

Files are organized by functional domain:

- Core platform profiles at the root level (display.yml, migrate.yml)
- Test profiles organized in the `test` subdirectory by functional area
- Related profiles are grouped by domain (cache, config, dataset, etc.)

### Domain-Specific Patterns

- Profiles use YAML anchors and references for configuration reuse
- Support for foreach loops and dynamic value generation through function calls
- Integration with Zimagi's command system for consistent operation execution
- Support for conditional execution using when clauses and requires dependencies

## Developer Notes and Usage Tips

### Integration Requirements

These profiles require:

- Proper command implementations in `app/commands` for profile operations
- Access to component processors in `app/components` for profile execution
- Command specifications in `app/spec/commands` for command parameter definitions
- Test framework in `app/tests` for test profile execution

### Usage Patterns

- Profiles are executed through the module command system
- Use existing profiles as templates for new implementations
- Follow established patterns for parameter definition and operation chaining
- Implement proper dependency management using requires clauses

### Dependencies

- Command system from `app/commands` for operation execution
- Component processors from `app/components` for profile processing
- Command specifications from `app/spec/commands` for parameter validation
- Test framework from `app/tests` for test profile execution

### AI Development Guidance

When generating or modifying profiles:

1. Maintain consistency with YAML-based profile definition patterns
2. Ensure proper operation sequencing and dependency management
3. Follow established patterns for parameter definition and interpolation
4. Respect the separation of concerns between different profile domains
5. Consider execution order implications for operation dependencies
6. Maintain consistency with existing naming and structure patterns
7. Reference existing profiles as examples for new implementations
8. Ensure profiles properly integrate with the command system through BaseProvider access
9. Use appropriate function calls and conditional logic for dynamic behavior
10. Follow the specification-driven approach where profile behavior is defined through YAML rather than hardcoded implementations
