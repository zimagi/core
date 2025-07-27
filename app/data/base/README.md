# Zimagi Base Data Models Directory

## Overview

The `app/data/base` directory contains foundational Django model base classes that serve as the building blocks for all data models within the Zimagi platform. These base classes implement core functionality such as resource identification, field management, and data persistence patterns that are shared across all platform entities.

This directory plays a critical architectural role by providing consistent, reusable base functionality that ensures data models throughout the platform follow standardized patterns for database interactions, serialization, and business logic implementation. The base models here are consumed by:

- **Developers** creating or extending data model classes in the Zimagi platform
- **AI models** analyzing and generating data model components
- **Build systems** that process specifications into database migrations

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| id_resource.py | Implements the IdentifierResourceBase class for models using UUID-based identifiers | Python |
| name_resource.py | Implements the NameResourceBase class for models using name-based primary keys | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/data` directory which contains Django data model applications that form the persistence layer of the Zimagi platform
- **Specifications**: Base models are defined in `app/spec/base/data.yml` and referenced by data model specifications in `app/spec/data`
- **Model Systems**: Connects to `app/systems/models` for dynamic model generation and facade implementation
- **Data Directory**: Serves as the foundation for all concrete data model implementations in `app/data/*/models.py`

## Key Concepts and Patterns

### Base Model Types

The directory provides two primary base model classes as defined in `app/spec/base/data.yml`:

1. **name_resource**: A base model for resources that use a name field as the primary key
   - Class: NameResourceBase
   - Primary key: name field (CharField, max_length: 256)
   - Mixins: resource
   - Ordering: by name

2. **id_resource**: A base model for resources that use a separate UUID identifier field as the primary key
   - Class: IdentifierResourceBase
   - Primary key: id field (CharField, max_length: 64, not editable)
   - Name field: separate name field (CharField, max_length: 256)
   - ID fields: name (used for generating the id)
   - Mixins: resource
   - Ordering: by name

### Core Functionality

Both base models implement essential functionality:

- **Save Method Override**: Custom save logic that prepares data before persistence
- **ID Generation**: Automatic generation of unique identifiers based on model fields
- **Field Management**: Standardized approaches to handling primary keys and unique identifiers

### Naming Conventions

- Files are named by their base model type (`id_resource.py`, `name_resource.py`)
- Class names follow the pattern `*Base` to indicate their foundational role
- Base model classes extend `BaseModel()` from the model indexing system

### File Organization

Files are organized by base model type:
- Name-based resource models in `name_resource.py`
- ID-based resource models in `id_resource.py`

### Domain-Specific Patterns

- All base models integrate with the model facade pattern through inheritance
- ID generation follows standardized patterns using utility functions
- Error handling follows consistent patterns with custom exception classes
- Field management respects Django ORM conventions

## Developer Notes and Usage Tips

### Integration Requirements

These modules require:
- Django framework access for ORM operations
- Proper model configurations in `app/data/*/models.py` for extension
- Access to utility functions from `app/utility` for ID generation
- Base model specifications from `app/spec/base/data.yml`

### Usage Patterns

- Extend base models when creating new data model classes
- Use NameResourceBase (`name_resource`) for simple named resources where the name serves as the primary key
- Use IdentifierResourceBase (`id_resource`) for complex resources requiring UUID identifiers where name is separate from the primary key
- Implement custom save logic by extending the _prepare_save() method

### Dependencies

- Django ORM for database interactions
- Standard Python libraries for data processing
- Utility functions from `app/utility` for ID generation
- Model systems from `app/systems/models` for dynamic generation

### AI Development Guidance

When generating or modifying base data models:

1. Maintain consistency with the base model architecture patterns defined in `app/spec/base/data.yml`
2. Ensure proper error handling with domain-specific exception classes
3. Follow established patterns for Django ORM integration
4. Respect the separation of concerns between different base model types
5. Consider performance implications for ID generation and save operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for facade and mixin usage
