# Zimagi User Templates Directory

## Overview

The `app/templates/user` directory contains Jinja2 template files that provide scaffolding for generating user role specifications within the Zimagi platform. These templates enable rapid creation of role-based access control (RBAC) configurations by providing standardized structures that follow Zimagi's permission management conventions.

This directory plays a critical architectural role by enabling developers and system administrators to quickly bootstrap new user roles with consistent permission definitions that integrate seamlessly with the platform's dynamic code generation system. The templates work with the template processing system in `app/systems/manage/template.py` and are consumed by:

- **Developers** creating new Zimagi user roles and permissions
- **System administrators** setting up standardized role-based access control
- **AI models** analyzing and generating RBAC components through template processing

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| index.yml | Defines user role template variables and mapping rules for generation | YAML |
| spec.yml | Template for generating user role specification entries in the auto-generated roles file | YAML |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/templates` directory which contains Jinja2 templates for various component systems
- **Template Commands**: Works with `app/commands/template` for template generation functionality
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Specifications**: Templates generate specification files that drive code generation in `app/spec/auto/roles.yml`
- **Role Management**: Generated templates create role specifications that integrate with the platform's RBAC system in `app/settings/roles.py`
- **Settings**: Works with `app/settings/roles.py` which provides the MetaRoles metaclass for role validation and access

## Key Concepts and Patterns

### Template Architecture

The user role template system implements a specification-driven approach to role generation:

- **Index Template** (`index.yml`): Defines user inputs and mapping rules for template generation, including required variables like role name and help text
- **Specification Template** (`spec.yml`): Generates YAML specification entries that are merged into the auto-generated roles file using Jinja2 variable substitution
- **Jinja2 Processing**: Templates use Jinja2 syntax with custom delimiters (`<{` and `}>` for variables, `#%` and `%#` for blocks) for dynamic content generation
- **Variable Interpolation**: Templates support complex variable processing and conditional logic

### Template Processing System

The template system in `app/systems/manage/template.py` provides:

- **Template Engine**: Custom Jinja2 environment with specialized delimiters for variable substitution
- **Function Loading**: Automatic loading of template functions from `templates/functions` directories across all modules
- **File Operations**: Copying and merging of template files to destination locations
- **Module Integration**: Scans all module directories for template files and merges them

### Template Structure

The user role template consists of two key files:

- **index.yml**: Defines variables that users can provide when generating the template, including help text and required fields
- **spec.yml**: Contains the actual role specification template with Jinja2 variables that get substituted

### Naming Conventions

- Template files follow the standard naming convention for Zimagi templates (`index.yml`, `spec.yml`)
- Variables in templates use snake_case convention for consistency
- Generated roles follow Zimagi's role naming conventions (using dashes, not underscores)
- Role names are validated through the MetaRoles metaclass in `app/settings/roles.py`

### File Organization

Files are organized to provide complete user role template structures:
- Index template defines user interface and required variables
- Specification template defines the output structure for role definitions
- Templates are organized by domain (user) and template type (role)

### Domain-Specific Patterns

- All templates use Jinja2 syntax for dynamic content generation
- Templates define variables with clear help text for user guidance
- Templates use mapping rules to specify target locations for generated files (`app/spec/auto/roles.yml`)
- Templates support complex data structures through YAML formatting
- Generated roles integrate with Zimagi's role-based access control system through the Roles class in `app/settings/roles.py`

## Developer Notes and Usage Tips

### Integration Requirements

These templates require:
- Access to the template command system in `app/commands/template`
- Proper template processing in `app/systems/manage/template.py`
- Utility functions from `app/utility` for template processing
- Role validation through the MetaRoles metaclass in `app/settings/roles.py`

### Usage Patterns

- Templates are executed through the `template generate` command with module "user" and template "role"
- Users provide variable values when generating templates (name and help text)
- Generated role specifications are placed in `app/spec/auto/roles.yml` through the mapping rules in `index.yml`
- Templates can be customized by modifying the template files
- The system automatically handles file merging and conflict resolution

### Dependencies

- Jinja2 template engine for template processing
- YAML parser for configuration generation
- Template command system from `app/commands/template`
- Template management system from `app/systems/manage/template.py`
- Role validation system from `app/settings/roles.py`
- Template functions from `app/templates/functions` directory

### AI Development Guidance

When generating or modifying user role templates:

1. Maintain consistency with Zimagi's role definition structure patterns
2. Ensure proper variable definitions with clear help text
3. Follow established patterns for configuration and metadata templates
4. Respect the separation of concerns between different template components
5. Consider user experience when designing template interfaces
6. Maintain consistency with existing naming and structure patterns
7. Document all variables with clear help messages
8. Follow the established patterns for conditional logic and mapping
9. Reference existing templates as examples for new implementations
10. Ensure generated roles properly integrate with the Zimagi platform's RBAC system
11. Test templates with the `template generate` command to verify functionality
12. Ensure role names are valid and don't conflict with existing roles through the MetaRoles validation
13. Leverage template functions from `app/templates/functions` when implementing complex logic
14. Follow the custom Jinja2 delimiter patterns (`<{`/`}>` for variables, `#%`/`%#` for blocks)
