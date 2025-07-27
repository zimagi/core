# Zimagi Specifications Directory

## Overview

The `app/spec` directory contains YAML specification files that define the core architectural components of the Zimagi platform. These specifications power the meta-programming code generation system, enabling dynamic creation of data models, commands, and plugins with minimal custom code.

This directory serves as the foundation for Zimagi's "specification-driven development" approach, where YAML configurations are transformed into functional Python classes and database models at runtime. The specifications defined here are consumed by code generation systems in `app/systems/models/meta`, `app/systems/commands/meta`, and `app/systems/plugins/meta` to create the platform's data layer, command interfaces, and plugin architectures.

The directory is used by:

- **Developers** to define and extend platform functionality
- **Build systems** to generate dynamic classes and database schemas
- **AI models** to understand and generate platform components

## Directory Contents

### Files

| File           | Purpose                                                         | Format |
| -------------- | --------------------------------------------------------------- | ------ |
| channels.yml   | Defines communication channels used for inter-service messaging | YAML   |
| encryption.yml | Defines encryption configurations for various system components | YAML   |
| roles.yml      | Defines user roles and their permissions within the system      | YAML   |
| services.yml   | Defines service configurations for Docker containers            | YAML   |
| users.yml      | Defines default user configurations and settings                | YAML   |
| workers.yml    | Defines worker configurations for background processing         | YAML   |

### Subdirectories

| Directory | Purpose                                                                     | Contents               |
| --------- | --------------------------------------------------------------------------- | ---------------------- |
| base      | Contains foundational specifications for data models, commands, and plugins | See base/README.md     |
| commands  | Contains command specifications that define executable CLI and API commands | See commands/README.md |
| data      | Contains data model specifications that define database structures          | See data/README.md     |
| mixins    | Contains reusable specification components for data, commands, and plugins  | See mixins/README.md   |
| plugins   | Contains plugin interface specifications for extensible functionality       | See plugins/README.md  |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi platform:

- **Code Generation**: Specifications are processed by systems in `app/systems/` to generate dynamic Python classes
- **Data Models**: Files in `app/data/` reference data specifications to create Django models
- **Commands**: Files in `app/commands/` implement command specifications
- **Plugins**: Files in `app/plugins/` implement plugin specifications
- **API Endpoints**: Generated data models automatically create REST API endpoints in `app/systems/api/data/`

## Key Concepts and Patterns

### Specification Structure

Specifications follow a hierarchical structure with three main categories:

- **Base specifications** define foundational components
- **Mixin specifications** provide reusable parameter sets
- **Implementation specifications** define concrete components

### Naming Conventions

- Files are named by their primary component or domain (e.g., `user.yml`, `source.yml`)
- Specification identifiers use snake_case
- Field and parameter names follow Django conventions
- Class references use PascalCase

### File Organization

Files are organized by component type:

- Data model specifications in `data/`
- Command specifications in `commands/`
- Plugin specifications in `plugins/`
- Shared components in `base/` and `mixins/`

### Domain-Specific Patterns

- Specifications can extend base components using the `base` property
- Fields define type, options, and metadata for Django model generation
- Parameters specify command-line and API interface elements
- Meta sections provide additional context for code generation

## Developer Notes

### Usage Tips

- When creating new components, check existing specifications to understand inheritance patterns
- Field definitions should include appropriate options like null, max_length, and on_delete
- Role permissions should be carefully considered for security
- Use existing base specifications and mixins to maintain consistency

### AI Generation Guidance

For AI models generating content in this directory:

- Maintain consistency with existing naming and structure patterns
- Ensure all required fields for each specification type are properly specified
- Reference existing specifications as examples for new implementations
- Validate that specification dependencies are properly declared

### Integration Points

These specifications integrate with:

- Code generation in `app/systems/`
- Django model creation in `app/data/`
- Command processing in `app/commands/`
- Plugin system in `app/plugins/`

Changes to these files require restarting the development server to regenerate classes.
