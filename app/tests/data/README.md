# Zimagi Test Data Directory

## Overview

The `app/tests/data` directory contains YAML-based test data fixtures that provide consistent, reproducible test scenarios for the Zimagi platform's testing framework. These data files serve as the foundation for initializing test environments with predefined entities and configurations that validate platform functionality across various domains.

This directory plays a critical role in the testing infrastructure by ensuring test consistency and reliability through standardized data inputs. Rather than hardcoding test values within test cases, these YAML fixtures provide a declarative approach to defining test data that can be reused across multiple test scenarios.

The test data is consumed by:
- **Test developers** writing new test cases for platform features
- **QA engineers** validating platform functionality and behavior
- **AI models** analyzing testing patterns and generating new test implementations
- **CI/CD systems** executing automated test suites

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| config.yml | Test data for configuration management scenarios including various data types (dict, int, str, list, bool, float) with grouping capabilities | YAML |
| group.yml | Test data for group management scenarios including hierarchical group relationships and different group types (base, classification, role) | YAML |
| host.yml | Test data for host management scenarios including connection parameters, authentication credentials, and encryption keys for remote hosts | YAML |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/tests` directory which contains the comprehensive test framework
- **Test Framework**: Connects to `app/tests/base.py` which provides the base test class functionality
- **Test Mixins**: Works with enhanced assertion capabilities from `app/tests/mixins` for object comparison and validation
- **SDK Tests**: Provides data fixtures for API testing in `app/tests/sdk_python`

## Key Concepts, Conventions, and Patterns

### Data Fixture Architecture

Test data fixtures implement a declarative approach to test data definition:

- **YAML-based Definition**: Data is defined using YAML syntax with a structured hierarchy
- **Entity-based Organization**: Each file represents a specific entity type with multiple test scenarios
- **Consistent Naming**: Entities use a double underscore naming convention (e.g., `test__1`)
- **Complete Definitions**: Each entity includes all required fields for proper initialization

### Fixture Structure

Each data fixture follows a consistent structure with these key elements:

- **Entity Identifiers**: Keys like `test__1` that uniquely identify each test entity
- **Property Definitions**: Complete set of entity properties with appropriate test values
- **Relationship References**: References to other entities by their identifiers
- **Type Specifications**: Explicit data type information where applicable

### Naming Conventions

- Files are named by their entity type (e.g., `config.yml`, `group.yml`, `host.yml`)
- Entity identifiers use snake_case with double underscore separation (e.g., `test__config1`)
- Property names follow snake_case for consistency with Zimagi's naming conventions
- Test values are descriptive and clearly indicate their purpose

### File Organization

Files are organized by entity type:
- Configuration data in `config.yml`
- Group data in `group.yml`
- Host data in `host.yml`

### Domain-Specific Patterns

- Config entities include provider_type, value_type, value, and groups properties
- Group entities define provider_type and parent relationships
- Host entities contain connection parameters, authentication credentials, and encryption keys
- All entities use consistent identifier patterns for cross-referencing

## Developer Notes and Usage Tips

### Integration Requirements

These data fixtures require:
- Proper test class implementation that loads YAML fixtures
- Access to the testing framework in `app/tests/base.py` which provides base test class with command and manager access
- Integration with assertion mixins from `app/tests/mixins`
- Proper entity initialization in test scenarios

### Usage Patterns

- Data fixtures are loaded automatically by the test framework
- Use existing fixtures as templates for new test data
- Follow established patterns for entity property definitions
- Implement proper cross-referencing between related entities

### Dependencies

- YAML parsing capabilities for fixture loading
- Django testing framework for entity initialization
- Test base classes from `app/tests/base.py` for integration with command and manager systems
- Assertion mixins from `app/tests/mixins` for validation

### AI Development Guidance

When generating or modifying test data:

1. Maintain consistency with YAML-based fixture definition patterns
2. Ensure all required entity properties are included in each fixture
3. Follow established naming conventions for entity identifiers
4. Respect the separation of concerns between different entity types
5. Consider cross-referencing implications when defining entity relationships
6. Maintain consistency with existing data values and patterns
7. Reference existing fixtures as examples for new implementations
8. Ensure fixtures properly integrate with the testing framework through BaseTest class
9. Use descriptive test values that clearly indicate their purpose
10. Follow the data-driven approach where test scenarios are defined through YAML rather than hardcoded values
