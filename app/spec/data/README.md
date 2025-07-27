# Zimagi Data Specifications

## Overview

The `app/spec/data` directory contains YAML specification files that define the data models used throughout the Zimagi platform. These specifications serve as the foundation for the platform's meta-programming code generation system, enabling dynamic creation of Django models, database tables, and REST API endpoints with minimal custom code.

This directory plays a critical role in Zimagi's "specification-driven development" approach, where YAML configurations are transformed into functional Python classes and database models at runtime. The specifications defined here are consumed by the code generation system in `app/systems/models/meta` to create the data layer that powers the entire platform.

The directory is used by:
- **Developers** defining data models and database structures
- **Code generation systems** that transform YAML into Python classes
- **AI models** analyzing and generating data model components

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| cache.yml | Defines cache data model for storing cached data and tracking request counts | YAML |
| chat.yml | Specifies chat and messaging data models including chats, dialogs, and messages | YAML |
| config.yml | Defines configuration data model with value storage and type information | YAML |
| dataset.yml | Specifies dataset data model for managing data collections | YAML |
| group.yml | Defines group data model and group mixin for role-based access control | YAML |
| host.yml | Specifies host data model for managing host connections and credentials | YAML |
| log.yml | Defines log and log message data models for system auditing | YAML |
| module.yml | Specifies module data model for managing extensible platform modules | YAML |
| notification.yml | Defines notification data model and related group associations | YAML |
| schedule.yml | Specifies scheduled task data models including intervals, crontabs, and datetimes | YAML |
| scaling.yml | Defines scaling event data model for tracking worker scaling activities | YAML |
| state.yml | Specifies state data model for storing runtime state variables | YAML |
| user.yml | Defines user data model with authentication and profile information | YAML |

There are no subdirectories in this directory.

## Cross-Referencing

This directory is part of the broader `app/spec` system which generates dynamic classes for the Zimagi platform. The data specifications defined here are consumed by:

- **Parent Context**: Part of the `app/spec` directory which contains all YAML specifications for the platform's meta-programming system
- **Base Models**: Connects to `app/spec/base/data.yml` for foundational data model structures
- **Mixins**: Integrates with `app/spec/mixins/data.yml` for reusable field sets
- **Code Generation**: Specifications are processed by systems in `app/systems/models/meta` to generate dynamic Python classes
- **Data Models**: Files in `app/data/*/models.py` reference these specifications in their definitions
- **API Endpoints**: Generated data models automatically create REST API endpoints in `app/systems/api/data/`
- **Commands**: Command implementations in `app/commands` utilize the data models

The generated classes are used throughout the application, particularly in:
- `app/systems/api/data` for REST API endpoints
- `app/commands` for data manipulation commands
- `app/plugins` for plugin functionality that interacts with data

## Key Concepts and Patterns

### Specification Structure

Each YAML file defines one or more data model specifications that include:
- Model identification (class name, base model)
- Field definitions (type, options, relationships)
- Role-based access control (edit/view permissions)
- Meta information (ordering, dynamic fields, provider names)
- Triggers for model lifecycle events
- Mixins for reusable field sets

### Base Models

The data specifications extend base models defined in `app/spec/base/data.yml`:

- `name_resource`: A base model with a name field as the primary key, used for simple named resources
- `id_resource`: A base model with separate id and name fields, where id is the primary key

These base models provide common functionality that data models inherit, ensuring consistency across the platform.

### Mixins

Data models can include reusable field sets through mixins defined in `app/spec/mixins/data.yml`:

- `resource`: A basic mixin providing common resource functionality
- `config`: Adds a configuration dictionary field for storing system configuration data
- `provider`: Extends config mixin to add provider type and variables fields for plugin implementations
- `group`: Adds many-to-many relationship fields for group-based access control

These mixins allow data models to compose functionality without duplicating field definitions.

### Naming Conventions

- Files are named by their primary data model or domain (e.g., `user.yml`, `schedule.yml`)
- Specification identifiers use snake_case
- Field names follow Django conventions
- Class references use PascalCase
- Relation names are descriptive and consistent

### File Organization

Files are organized by data domain or model relationship:
- Core models in individual files (user, config, module)
- Related models in the same file (schedule, notification)
- Specialized models grouped by function (chat, log)

### Domain-Specific Patterns

- Models can extend base models defined in `app/spec/base/data.yml`
- Models can include mixins defined in `app/spec/mixins/data.yml`
- Fields define type, options, and metadata for Django model generation
- Relationships use Django foreign key and many-to-many patterns
- Meta sections provide ordering, constraints, and dynamic field information

## Developer Notes and Usage Tips

### Usage Tips

- When creating new data models, check existing specifications to understand inheritance patterns
- Field definitions should include appropriate options like null, max_length, and on_delete
- Role permissions should be carefully considered for security
- Dynamic fields in meta sections enable computed properties in API responses
- Use existing base models and mixins to maintain consistency and reduce code duplication

### Integration Requirements

These specifications require:
- Proper base model definitions in `app/spec/base/data.yml`
- Available mixins in `app/spec/mixins/data.yml`
- Code generation systems in `app/systems/models/meta` for Python class creation
- Django framework for model implementation

### Dependencies

- Code generation in `app/systems/models/meta`
- Django model creation in `app/data`
- REST API generation in `app/systems/api/data`
- Command system in `app/commands`

### AI Development Guidance

When generating or modifying data specifications:

1. Maintain consistency with existing naming and structure patterns
2. Ensure all required fields for each specification type are properly specified
3. Reference existing specifications as examples for new implementations
4. Validate that specification dependencies are properly declared using the `base` or `mixins` properties
5. Follow established patterns for field definitions, relationships, and meta information
6. Consider security implications of role permissions when defining edit/view access
7. Use appropriate base models and mixins when they match the intended functionality
8. Ensure dynamic fields in meta sections are properly documented and implemented
9. Maintain consistency with Django field naming and option conventions
10. Consider database performance implications of field types and relationships
