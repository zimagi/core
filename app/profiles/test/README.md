# Zimagi Test Profiles Directory

## Overview

The `app/profiles/test` directory contains YAML command profiles specifically designed for testing the Zimagi platform's functionality. These profiles define orchestrated sequences of operations that validate different aspects of the platform including data management, module operations, user management, scheduling, and other core features.

This directory plays a critical role in the platform's quality assurance process by providing standardized test workflows that can be executed consistently across different environments. The test profiles leverage the same profile execution system used for production workflows but are focused on verification and validation rather than operational tasks.

The profiles are consumed by:

- **Developers** working on feature development and testing
- **QA engineers** running automated test suites
- **CI/CD systems** executing automated testing pipelines
- **AI models** analyzing and generating test scenarios

## Directory Contents

### Files

| File             | Purpose                                                              | Format |
| ---------------- | -------------------------------------------------------------------- | ------ |
| base.yml         | Defines base configuration and common settings for all test profiles | YAML   |
| cache.yml        | Profile for testing cache management operations                      | YAML   |
| config.yml       | Profile for testing configuration management operations              | YAML   |
| dataset.yml      | Profile for testing dataset operations                               | YAML   |
| dependency.yml   | Profile for testing dependency resolution and execution ordering     | YAML   |
| failure.yml      | Profile for testing failure scenarios and error handling             | YAML   |
| group.yml        | Profile for testing group management operations                      | YAML   |
| host.yml         | Profile for testing host management operations                       | YAML   |
| log.yml          | Profile for testing log management operations                        | YAML   |
| module.yml       | Profile for testing module management operations                     | YAML   |
| notification.yml | Profile for testing notification system operations                   | YAML   |
| schedule.yml     | Profile for testing scheduled task operations                        | YAML   |
| state.yml        | Profile for testing state management operations                      | YAML   |
| task.yml         | Profile for testing task execution operations                        | YAML   |
| user.yml         | Profile for testing user management operations                       | YAML   |

### Subdirectories

| Directory | Purpose                                                          | Contents           |
| --------- | ---------------------------------------------------------------- | ------------------ |
| data      | Contains data-specific test profiles for various data operations | See data/README.md |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/profiles` directory which contains YAML command profiles for orchestrated operations
- **Profile System**: Connects to `app/components` for profile component processors that execute the defined operations
- **Command Systems**: Works with `app/commands` for executable command implementations
- **Test Framework**: Integrates with `app/tests` for automated testing workflows
- **Specifications**: Uses command specifications defined in `app/spec/commands` for parameter validation

## Key Concepts and Patterns

### Profile Architecture

Test profiles implement a declarative approach to testing workflows:

- **YAML-based Definition**: Profiles are defined using YAML syntax with a structured hierarchy
- **Operation Chaining**: Commands are executed in a defined sequence with dependency management
- **Conditional Execution**: Support for conditional operation execution based on previous results
- **Parameter Interpolation**: Dynamic parameter substitution using configuration values and function results

### Test Profile Structure

Each test profile follows a consistent structure with these key sections:

- **Configuration**: Defines variables and settings used throughout the profile
- **Pre-run Operations**: Setup operations executed before main profile execution
- **Run Operations**: Main execution sequence of commands and operations
- **Post-run Operations**: Cleanup and finalization operations after execution
- **Destroy Operations**: Special operations for resource cleanup and teardown

### Naming Conventions

- Files are named by their functional domain (e.g., `cache.yml`, `log.yml`)
- Test profiles use descriptive names that indicate their testing focus
- Configuration keys and variables use snake_case for consistency
- Data-related test profiles are organized in the `data` subdirectory

### File Organization

Files are organized by functional domain:

- Core test profiles at the root level (base.yml, dependency.yml, failure.yml)
- Data testing profiles organized in the `data` subdirectory by functional area
- Related profiles are grouped by domain (cache, config, dataset, etc.)

### Domain-Specific Patterns

- Profiles use YAML anchors and references for configuration reuse
- Support for foreach loops and dynamic value generation through function calls
- Integration with Zimagi's command system for consistent operation execution
- Support for conditional execution using when clauses and requires dependencies
- Many profiles follow a pattern of creating, retrieving, and then removing test data

## Developer Notes and Usage Tips

### Integration Requirements

These profiles require:

- Proper command implementations in `app/commands` for profile operations
- Access to component processors in `app/components` for profile execution
- Command specifications in `app/spec/commands` for parameter validation
- Test framework in `app/tests` for automated profile execution

### Usage Patterns

- Profiles are executed through the module command system
- Use existing profiles as templates for new test implementations
- Follow established patterns for parameter definition and operation chaining
- Implement proper dependency management using requires clauses
- Clean up test data in destroy or post-run sections

### Dependencies

- Command system from `app/commands` for operation execution
- Component processors from `app/components` for profile processing
- Command specifications from `app/spec/commands` for parameter validation
- Test framework from `app/tests` for test profile execution

### AI Development Guidance

When generating or modifying test profiles:

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
11. Include proper cleanup operations to avoid test data pollution
12. Design tests to be idempotent and repeatable
