# Zimagi Tests Directory

## Overview

The `app/tests` directory contains the comprehensive test framework and various test libraries for the Zimagi platform. This directory plays a critical architectural role by ensuring the reliability, correctness, and stability of the Zimagi application through automated testing capabilities across multiple layers of the system.

The testing framework supports both unit and integration testing with specialized test suites for different components including data APIs, command APIs, scheduled tasks, and system status checks. Tests are organized by functional domains and executed through Django's testing infrastructure.

This directory is primarily used by:

- **Developers** for validating code changes and ensuring feature quality
- **CI/CD systems** for automated testing in deployment pipelines
- **AI models** for understanding testing patterns and generating new test cases

## Directory Contents

### Files

| File             | Purpose                                                                                | Format |
| ---------------- | -------------------------------------------------------------------------------------- | ------ |
| base.py          | Base test class providing foundational testing capabilities and setup/teardown methods | Python |
| command_local.py | Local command test implementation extending the base command test framework            | Python |

### Subdirectories

| Directory  | Purpose                                                                               | Contents                                                 |
| ---------- | ------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| data       | Test data fixtures in YAML format used for initializing test scenarios                | YAML files containing test data for various entity types |
| mixins     | Test utility mixins providing additional assertion and validation capabilities        | Python modules with test helper methods                  |
| sdk_python | Python SDK tests covering API interactions, data operations, and system functionality | Python test modules organized by test domain             |
| command    | Command-based test framework components                                               | Python modules for command-oriented testing              |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Test Framework**: Built on Django's testing infrastructure and integrated with the project's API clients
- **Data Layer**: Uses test data fixtures from `app/tests/data` to initialize test scenarios
- **Command System**: Connects to `app/commands` for testing executable command implementations
- **API Layer**: Tests interact with both command and data APIs through the Python SDK clients

## Key Concepts, Conventions, and Patterns

### Test Architecture

The testing framework implements a multi-layered approach to validation:

- **Unit Testing**: Direct testing of individual components and functions
- **Integration Testing**: Testing interactions between multiple system components
- **API Testing**: Validation of API endpoints through SDK client interactions
- **Functional Testing**: End-to-end testing of complete workflows and operations

### Test Organization

Tests are organized by functional domains following these patterns:

- **Base Framework**: Foundational test classes and utilities in the root directory
- **Data Tests**: Located in `sdk_python/data` for testing data model operations
- **Command Tests**: Located in `sdk_python/command` for testing command functionality
- **Initialization Tests**: Located in `sdk_python/init` for testing system initialization
- **Test Data**: Stored in `data` directory as YAML fixtures for consistent test scenarios

### Naming Conventions

- Test classes use descriptive names ending with "Test" (e.g., `GroupTest`, `StatusTest`)
- Test methods are prefixed with "test\_" and use descriptive names (e.g., `test_group_list`)
- Test data files are named by their entity type (e.g., `group.yml`, `config.yml`)
- Test directories are organized by functional domain (e.g., `data`, `init`, `command`)

### File Organization

Files are organized by testing scope:

- Core test framework components at the root level
- SDK-based API tests in `sdk_python` subdirectory
- Test data fixtures in `data` subdirectory
- Command-based tests in `command` subdirectory
- Test utility mixins in `mixins` subdirectory

### Domain-Specific Patterns

- Tests use YAML data fixtures for consistent and reproducible test scenarios
- Test classes inherit from specialized base classes providing common functionality
- Tests are tagged for selective execution using Django's tagging system
- API tests use both command and data clients for comprehensive coverage
- Test assertions include custom methods for object comparison and validation

## Developer Notes and Usage Tips

### Integration Requirements

These tests require:

- Proper Django test environment setup
- Access to both command and data API endpoints
- Test data fixtures in the `data` directory
- Properly configured API clients with authentication credentials

### Usage Patterns

- Tests are executed through Django's test runner
- Use existing tests as templates for new test implementations
- Follow established patterns for test data fixture creation
- Implement proper test isolation using setup and teardown methods
- Use tagging to organize tests by functional area and execution context

### Dependencies

- Django testing framework for test execution and infrastructure
- Python SDK clients for API interactions
- YAML data fixtures for test data initialization
- Custom assertion mixins for specialized validation

### AI Development Guidance

When generating or modifying tests:

1. Maintain consistency with existing test class and method naming patterns
2. Follow established patterns for test data fixture usage and organization
3. Use appropriate tagging to categorize tests by functional domain
4. Implement proper test isolation and cleanup in setup/teardown methods
5. Follow existing patterns for API client usage and assertion methods
6. Reference existing tests as examples for new implementations
7. Ensure tests properly integrate with the Django testing framework
8. Use appropriate assertion methods for object comparison and validation
9. Maintain consistency with existing test organization by functional domain
10. Follow the data-driven approach where test scenarios are defined through YAML fixtures rather than hardcoded values
