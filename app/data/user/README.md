# Zimagi User Data Model Directory

## Overview

The `app/data/user` directory contains the Django data model implementation for the Zimagi platform's user management functionality. This model is responsible for defining user structures, managing authentication credentials, storing user preferences, and providing role-based access control for user operations across the platform.

This directory plays a critical architectural role by implementing the persistence layer for user management, enabling the platform to handle user authentication, profile management, group memberships, and permission assignments. The user model works in conjunction with the user command system in `app/commands/user` to provide a complete user management solution.

The directory is used by:
- **Developers** working on user management and authentication features
- **System administrators** managing platform users and access control
- **AI models** analyzing and generating user management components

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| models.py | Implements the User Django model and facade for user management | Python |
| migrations/0001_initial.py | Initial database migration that creates the user table with all required fields | Python |
| migrations/0002_user_temp_token_user_temp_token_time.py | Migration that adds temporary token fields for user authentication | Python |
| migrations/0003_user_encoder_provider_user_encoder_provider_options_and_more.py | Migration that adds AI-related fields for language models, encoders, and text splitters | Python |
| migrations/0004_user_text_splitter_provider_options.py | Migration that adds text splitter provider options field | Python |

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| migrations | Contains Django database migration files for tracking schema changes to the user model | Database migration files for schema evolution |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/data` directory which contains Django data model applications that form the persistence layer of the Zimagi platform
- **Specifications**: The user data model is defined in `app/spec/data/user.yml` which drives the automatic generation of the model
- **Base Models**: Extends the `name_resource` base model defined in `app/spec/base/data.yml`
- **Mixins**: Incorporates the `provider` and `group` mixins from `app/spec/mixins/data.yml` for plugin-based user handling and access control
- **API Systems**: Connects to `app/systems/api/data` for REST API exposure of users
- **Command Systems**: Works with `app/commands/user` for user command implementations
- **Group System**: Integrates with `app/data/group` for role-based access control through group relationships
- **Settings**: Integrates with configurations defined in `app/settings` for user management parameters

## Key Concepts and Patterns

### User Model Structure

The User model implements a comprehensive user management mechanism based on the specifications in `app/spec/data/user.yml`:
- **name**: Primary key identifier for the user entry (CharField, max_length: 256)
- **config**: Dictionary field storing user metadata (DictionaryField, default: dict)
- **provider_type**: Specifies the user provider implementation (CharField, max_length: 128, default: "base")
- **variables**: Dictionary field storing provider-specific variables (DictionaryField, default: dict, not editable)
- **email**: User's email address (EmailField, null: True)
- **first_name**: User's first name (CharField, max_length: 30, null: True)
- **last_name**: User's last name (CharField, max_length: 150, null: True)
- **is_active**: Flag indicating if the user account is active (BooleanField, default: True)
- **password**: Hashed password for user authentication (CharField, max_length: 256, null: True, not editable)
- **encryption_key**: Key used for encrypting user-specific data (CharField, max_length: 256, null: True)
- **last_login**: Timestamp of the user's last login (DateTimeField, null: True, not editable)
- **groups**: Many-to-many relationship for role-based access control (ManyToManyField to Group model)
- **temp_token**: Temporary authentication token (CharField, max_length: 256, null: True, not editable)
- **temp_token_time**: Timestamp for temporary token creation (DateTimeField, null: True, not editable)
- **language_provider**: Language model provider for AI interactions (CharField, max_length: 256, null: True)
- **language_provider_options**: Configuration options for language model provider (DictionaryField, default: dict)
- **encoder_provider**: Text encoder provider for AI interactions (CharField, max_length: 256, null: True)
- **encoder_provider_options**: Configuration options for encoder provider (DictionaryField, default: dict)
- **text_splitter_provider**: Text splitter provider for document processing (CharField, max_length: 256, null: True)
- **text_splitter_provider_options**: Configuration options for text splitter provider (DictionaryField, default: dict)
- **search_limit**: Maximum number of search results to return (IntegerField, default: 1000)
- **search_min_score**: Minimum similarity score for search results (FloatField, default: 0.3)
- **created/updated**: Automatic timestamp fields for tracking entry lifecycle

### Model Generation Pattern

Following Zimagi's specification-driven approach:
- Model structure is defined in `app/spec/data/user.yml`
- Automatically generated by the model system in `app/systems/models`
- Based on the `name_resource` base model which uses the name field as the primary key
- Incorporates the `provider` and `group` mixins for plugin-based functionality and access control
- Manual extensions can be added in `models.py` if needed

### Provider Integration

The user model supports plugin-based providers through the provider mixin:
- Provider type selection enables different user storage backends
- Variables field stores provider-specific configuration parameters
- Integration with the plugin system in `app/systems/plugins` for provider implementations
- Config mixin provides standardized configuration field management

### Group Integration

The user model integrates with the group system through the group mixin:
- Groups field provides many-to-many relationship for role-based access control
- Integration with the group data model in `app/data/group` for permission management
- Support for automatic group assignment through specification triggers

### Access Control

The user model implements role-based access control as defined in `app/spec/data/user.yml`:
- **View permissions**: Available to users with user-auditor roles
- **Edit permissions**: Restricted to users with user-admin roles
- **Destroy operations**: Uses default behavior with proper access control

### Base Model Inheritance

The model extends the `name_resource` base model defined in `app/spec/base/data.yml`:
- Uses name as primary key for direct identification
- Provides automatic created/updated timestamp fields
- Implements consistent ordering by name field
- Provides resource mixin functionality

### Mixin Composition

The model incorporates mixins from `app/spec/mixins/data.yml`:
- **ProviderMixin**: Enables plugin-based provider functionality with config and variables fields
- **GroupMixin**: Provides group-based access control through many-to-many relationships
- **ResourceMixin**: Provides core resource functionality and metadata management

### Naming Conventions

- Model files are consistently named `models.py`
- Migration files follow Django's sequential naming pattern
- Class names use PascalCase and are descriptive of their domain (User, UserManager, UserFacade)
- Field names use snake_case following Django conventions
- Database table uses prefixed name (core_user)

### File Organization

Files are organized by Django application conventions:
- Model definition in `models.py`
- Database migrations in the `migrations` subdirectory
- One migration file per schema change

### Domain-Specific Patterns

- The model extends the `name_resource` base model from `app/spec/base/data.yml` for consistent resource behavior
- Uses facade pattern from `app/systems/models` for business logic implementation
- Integrates with Django's migration system for schema version control
- Implements the `provider` and `group` mixins for plugin-based functionality and access control
- Uses the `name_resource` base which uses name as the primary key
- Implements ordering by name for consistent user listing
- Supports dynamic fields for computed properties in API responses
- Implements custom UserManager for user-specific operations
- Provides methods for AI-related functionality (language models, encoders, text splitters)
- Implements specification triggers for automatic group assignment

## Developer Notes and Usage Tips

### Integration Requirements

This model requires:
- Django framework access for ORM operations
- Proper database configuration in settings
- Integration with the group data model in `app/data/group` for access control
- Specification file in `app/spec/data/user.yml` for model generation
- Plugin system access for provider functionality

### Usage Patterns

- The model is automatically used by user commands in `app/commands/user`
- Access through the facade rather than direct model interaction
- Business logic should be implemented in facade methods if extensions are needed
- Provider implementations should extend the base provider in `app/plugins/user`
- Migration files should be generated using Django's migration system when changes are made

### Dependencies

- Django ORM for database interactions
- Model systems from `app/systems/models` for dynamic generation
- Specification file from `app/spec/data/user.yml` for model definition
- Group model from `app/data/group` for access control relationships
- Plugin system from `app/systems/plugins` for provider functionality

### AI Development Guidance

When generating or modifying user model components:

1. Maintain consistency with specification-driven generation patterns
2. Follow established naming conventions for models and fields
3. Ensure proper integration with the provider plugin system
4. Consider performance implications for user retrieval operations
5. Maintain consistency with existing API and command integration patterns
6. Document all public methods with clear docstrings
7. Follow the established patterns for facade and base class usage
8. Respect the role-based access control configuration defined in the specification
9. Maintain the ordering configuration for proper user listing
10. Ensure proper integration with the group-based access control system
11. Implement proper AI-related fields and methods for language model integration
