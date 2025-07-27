# Zimagi Data Directory

## Overview

The `app/data` directory contains Django data model applications that form the persistence layer of the Zimagi platform. These models define the database schema, data relationships, and business logic for all platform entities including users, groups, configurations, modules, logs, and more.

This directory plays a critical architectural role by implementing the data persistence layer that powers Zimagi's dynamic, specification-driven framework. The models here are automatically generated from YAML specifications in `app/spec/data` through the meta-programming system in `app/systems/models`.

The directory is used by:
- **Developers** working on data models and persistence logic
- **AI models** analyzing and generating data components
- **Build systems** that process specifications into database migrations
- **System administrators** managing data schemas and relationships

## Directory Contents

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| base | Contains base model classes that other models inherit from | See base/README.md |
| cache | Implements cache tracking model for HTTP response caching | Model and migrations for cache entries |
| chat | Implements chat and messaging functionality models | Models for chats, dialogs, and messages with migrations |
| config | Implements configuration management models | Model and migrations for system configuration storage |
| dataset | Implements dataset management models | Model and migrations for data collection management |
| group | Implements user group and role-based access control models | Model, migrations, and cache for group management |
| host | Implements host connection management models | Model and migrations for remote host configurations |
| log | Implements system logging and audit models | Models and migrations for logs and log messages |
| mixins | Contains reusable model functionality components | See mixins/README.md |
| module | Implements extensible module system models | Model and migrations for module management |
| notification | Implements notification system models | Models and migrations for notifications and groups |
| schedule | Implements scheduled task management models | Models and migrations for task scheduling |
| scaling_event | Implements auto-scaling event tracking models | Model and migrations for worker scaling events |
| state | Implements runtime state variable models | Model and migrations for state management |
| user | Implements user management and authentication models | Model and migrations for user accounts and profiles |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Specifications**: Data models are generated from specifications in `app/spec/data`
- **Model Systems**: Connects to `app/systems/models` for dynamic model generation
- **API Systems**: Works with `app/systems/api/data` for REST API exposure
- **Command Systems**: Integrates with `app/commands` for data manipulation
- **Plugin Systems**: Connects to `app/plugins` for extensible functionality

## Key Concepts and Patterns

### Model Structure

Each subdirectory represents a distinct data domain and typically contains:
- `models.py`: Defines the Django model classes and facade logic
- `migrations/`: Contains database migration files for schema changes
- Additional domain-specific files (e.g., cache implementations)

### Specification-Driven Development

Data models follow Zimagi's specification-driven approach:
- YAML specifications in `app/spec/data` define model structure
- Code generation in `app/systems/models/meta` creates Django models
- Manual extensions can be added in `models.py` files

### Naming Conventions

- Subdirectories are named by their data domain (e.g., `user`, `config`, `module`)
- Model files are consistently named `models.py`
- Migration files follow Django's naming pattern with sequential numbers
- Class names use PascalCase and are descriptive of their domain

### File Organization

Files are organized by data domain:
- Each domain has its own subdirectory
- Related models may be grouped in the same directory
- Migrations are stored alongside their respective models

### Domain-Specific Patterns

- Models extend base classes from `app/data/base`
- Facade classes provide business logic and data access patterns
- Mixins from `app/data/mixins` compose reusable functionality
- Migrations track all schema changes for version control

## Developer Notes and Usage Tips

### Integration Requirements

These models require:
- Django framework access for ORM operations
- Proper database configuration in settings
- Access to model systems in `app/systems/models` for dynamic functionality
- Specification files in `app/spec/data` for model generation

### Usage Patterns

- Models are accessed through facade classes rather than directly
- Business logic should be implemented in facade methods
- New models should be defined in specifications first
- Migrations should be generated using Django's migration system

### Dependencies

- Django ORM for database interactions
- Model systems from `app/systems/models` for dynamic generation
- Specification files from `app/spec/data` for model definitions
- Utility functions from `app/utility` for common operations

### AI Development Guidance

When generating or modifying data models:

1. Maintain consistency with specification-driven generation patterns
2. Follow established naming conventions for models and fields
3. Reference existing models as examples for new implementations
4. Ensure proper relationships and constraints are defined
5. Consider performance implications for database operations
6. Maintain consistency with existing API and command integration patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for facade and mixin usage
