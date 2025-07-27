# Zimagi Data Templates Directory

## Overview

The `app/templates/data` directory contains Jinja2 template files that provide scaffolding for generating data model specifications within the Zimagi platform. These templates enable rapid creation of data models by providing standardized structures that follow Zimagi's data modeling conventions and specification-driven development approach.

This directory plays a critical architectural role by enabling developers and system administrators to quickly bootstrap new data models with consistent configuration files that integrate seamlessly with the platform's dynamic code generation system. The templates work with the template processing system in `app/systems/manage/template.py` and are consumed by:

- **Developers** creating new Zimagi data models
- **System administrators** setting up standardized data model configurations
- **AI models** analyzing and generating data model components through template processing

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| README.md | This documentation file | Markdown |
| model | Template for generating data model specifications | Directory containing index.yml and spec templates |

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| model | Contains templates for data model generation | index.yml, data.yml, command.yml, plugin.yml |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/templates` directory which contains Jinja2 templates for various component systems
- **Template Commands**: Works with `app/commands/template` for template generation functionality
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Specifications**: Templates generate specification files that drive code generation in `app/spec/data`
- **Data Models**: Generated templates create data model specifications in `app/spec/data` which are then processed by `app/systems/models`

## Key Concepts and Patterns

### Template Architecture

The data template system implements a specification-driven approach to data model generation:

- **Index Templates**: Define user inputs and mapping rules for template generation (`index.yml`)
- **Specification Templates**: Generate YAML specification files that drive code generation (`data.yml`, `command.yml`, `plugin.yml`)
- **Jinja2 Processing**: Templates use Jinja2 syntax with custom delimiters (`<{` and `}>` for variables, `#%` and `%#` for blocks)
- **Variable Interpolation**: Templates support complex variable processing and conditional logic

### Template Structure

The model template directory contains:

- **index.yml**: Defines variables that users can provide when generating the template, including help text and default values
- **data.yml**: Contains the data model specification template with Jinja2 variables that get substituted
- **command.yml**: Contains command specification template for generating CRUD commands for the model
- **plugin.yml**: Contains plugin specification template for making the model pluggable

### Naming Conventions

- Template directories are named by their functional domain (e.g., `model`)
- Index files are consistently named `index.yml`
- Specification files are named to match the target specification directory (`data.yml`, `command.yml`, `plugin.yml`)
- Template variables follow snake_case convention for consistency
- Generated files follow Zimagi's specification naming conventions

### File Organization

Files are organized to provide complete data model template structures:
- Each template type has its own subdirectory
- Index and specification templates for each template type
- Standard data model directory structure templates

### Domain-Specific Patterns

- All templates use Jinja2 syntax with custom delimiters for dynamic content generation
- Templates define variables with help text for user guidance
- Templates use conditional logic to control output generation
- Templates support complex data structures through YAML formatting
- Generated specifications are placed in `spec/auto/` directory structure

## Developer Notes and Usage Tips

### Integration Requirements

These templates require:
- Access to the template command system in `app/commands/template`
- Proper template processing in `app/systems/manage/template.py`
- Utility functions from `app/utility` for template processing

### Usage Patterns

- Templates are executed through the `template generate` command
- Users provide variable values when generating templates (e.g., model name, base model, etc.)
- Generated specifications follow Zimagi's standard specification structure
- Templates can be customized by modifying the template files

### Dependencies

- Jinja2 template engine for template processing
- YAML parser for configuration generation
- Template command system from `app/commands/template`
- Template management system from `app/systems/manage/template.py`
- Utility functions from `app/utility` for filesystem operations

### AI Development Guidance

When generating or modifying data templates:

1. Maintain consistency with Zimagi's specification structure patterns
2. Ensure proper variable definitions with clear help text
3. Follow established patterns for configuration and metadata templates
4. Respect the separation of concerns between different template components
5. Consider user experience when designing template interfaces
6. Maintain consistency with existing naming and structure patterns
7. Document all variables with clear help messages
8. Follow the established patterns for conditional logic and mapping
9. Reference existing templates as examples for new implementations
10. Ensure generated specifications properly integrate with the Zimagi platform's specification-driven generation system
11. Test templates with the `template generate` command to verify functionality
12. Ensure template functions are properly loaded through the ManagerTemplateMixin system
