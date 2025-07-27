# Zimagi Python SDK Tests Directory

## Overview

The `app/tests/sdk_python` directory contains the Python SDK test suite for the Zimagi platform. This directory provides comprehensive testing capabilities for validating the Python SDK client interactions with both command and data APIs, ensuring proper functionality of API endpoints, data operations, system initialization, and scheduled tasks.

This directory plays a critical role in the testing infrastructure by enabling automated validation of Python SDK functionality through direct API interactions. Rather than testing individual components in isolation, these tests focus on end-to-end validation of SDK operations that represent complete API workflows.

The SDK tests are consumed by:

- **Test developers** writing integration tests for SDK functionality
- **QA engineers** validating platform API operations and behavior
- **CI/CD systems** executing automated test suites for SDK validation
- **AI models** analyzing testing patterns and generating new test implementations

## Directory Contents

### Files

| File      | Purpose                                                                                                                          | Format |
| --------- | -------------------------------------------------------------------------------------------------------------------------------- | ------ |
| base.py   | Base SDK test class providing foundational SDK testing capabilities including API client initialization and data loading methods | Python |
| runner.py | Custom test runner implementation extending Django's DiscoverRunner for SDK test execution                                       | Python |

### Subdirectories

| Directory | Purpose                                                                                              | Contents                                     |
| --------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| data      | Data API tests covering data model operations, list/retrieve functionality, and data transformations | See app/tests/sdk_python/data/README.md      |
| init      | Initialization and system tests covering API schemas, system status, and scheduled task execution    | Python test modules organized by test domain |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/tests` directory which contains the comprehensive test framework (see app/tests/README.md)
- **Test Framework**: Built on Django's testing infrastructure and integrated with the project's API clients
- **Data Layer**: Uses test data fixtures from `app/tests/data` to initialize test scenarios (see app/tests/data/README.md)
- **API Layer**: Tests interact with both command and data APIs through the Python SDK clients in `package/zimagi`
- **Test Mixins**: Integrates with enhanced assertion capabilities from `app/tests/mixins` for object comparison and validation (see app/tests/mixins/README.md)

## Key Concepts, Conventions, and Patterns

### SDK Test Architecture

SDK tests implement an API interaction-based approach to testing platform operations:

- **Client-Based Testing**: Tests use Python SDK clients to interact with command and data APIs
- **End-to-End Validation**: Tests validate complete API workflows rather than individual components
- **Data Fixture Integration**: Tests utilize YAML data fixtures for consistent test scenarios
- **Enhanced Assertions**: Tests leverage custom assertion methods for object comparison and validation

### Test Structure

SDK tests follow a consistent structure with these key components:

- **API Client Initialization**: Automatic initialization of command and data API clients
- **Data Fixture Loading**: Integration with YAML data fixtures for test data initialization
- **Enhanced Assertions**: Custom assertion methods for object comparison and validation
- **Resource Management**: Proper setup and teardown operations for test resource management

### Naming Conventions

- Files are named by their functional domain with descriptive names (e.g., `base.py`, `runner.py`)
- Test classes use descriptive names ending with "Test" (e.g., `GroupTest`, `StatusTest`)
- Test methods are prefixed with "test\_" and use descriptive names (e.g., `test_group_list`)
- Module references use consistent naming aligned with platform conventions

### File Organization

Files are organized by testing functionality:

- Core SDK test framework components in `base.py` and `runner.py`
- Data API tests organized in the `data` subdirectory by entity type
- Initialization and system tests in the `init` subdirectory by functional area

### Domain-Specific Patterns

- Tests use Python SDK clients for API interactions with both command and data endpoints
- Implementation follows Django's testing framework with custom extensions
- Support for both data operations and command execution through SDK clients
- Integration with platform testing through BaseTest inheritance

## Developer Notes and Usage Tips

### Integration Requirements

These SDK tests require:

- Proper inheritance from BaseTest for access to SDK client methods
- Access to test data fixtures in `app/tests/data` for data initialization
- Integration with assertion mixins from `app/tests/mixins` for validation
- Properly configured API clients with authentication credentials

### Usage Patterns

- SDK tests are executed through Django's test runner
- Use existing base classes as templates for new SDK test implementations
- Follow established patterns for API client usage and data fixture integration
- Implement proper test isolation using setup and teardown methods

### Dependencies

- Django testing framework for test execution and infrastructure
- Python SDK clients from `package/zimagi` for API interactions
- Test data fixtures from `app/tests/data` for test data initialization
- Custom assertion mixins from `app/tests/mixins` for specialized validation

### AI Development Guidance

When generating or modifying SDK tests:

1. Maintain consistency with existing SDK test class and method patterns
2. Follow established patterns for API client usage and data fixture integration
3. Ensure proper test isolation and cleanup in setup/teardown methods
4. Reference existing base classes as examples for new implementations
5. Maintain consistency with the API interaction-based testing approach
6. Follow the data-driven approach where test scenarios are defined through YAML fixtures rather than hardcoded values
7. Use appropriate assertion methods for object comparison and validation
8. Ensure tests properly integrate with the Django testing framework
9. Respect the separation of concerns between different testing domains
10. Follow the client-driven testing pattern where test behavior is validated through SDK client interactions
