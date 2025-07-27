# Zimagi Templates Directory

## Overview

The `app/templates` directory contains Jinja2 template files that provide scaffolding and code generation capabilities for the Zimagi platform. These templates are used to generate various components including data models, fields, user roles, and module structures through the platform's template command system.

This directory plays a critical architectural role by enabling rapid development and consistent structure generation across the platform. The templates work with the dynamic class generation system to create standardized components based on user input, reducing boilerplate code and ensuring adherence to platform conventions. The templates here are consumed by:

- **Developers** working on extending platform functionality through standardized components
- **System administrators** creating new modules and data structures
- **AI models** analyzing and generating template-based components

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| README.md | This documentation file | Markdown |

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| cell | Contains templates for AI cell prompt generation | Prompt templates for chat, system, assistant, and tools |
| data | Contains templates for data model generation | Model templates for creating new data structures |
| field | Contains templates for field type generation | Field templates for various Django field types |
| functions | Contains templates for core utility functions | Function templates for text, list, and class operations |
| module | Contains templates for module creation | Module templates for standard module structures |
| user | Contains templates for user role generation | Role templates for defining user permissions |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files
- **Template Commands**: Works with `app/commands/template` for template generation functionality
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Specifications**: Templates generate specification files that drive code generation in `app/spec`
- **Data Models**: Field and data templates create data model specifications in `app/spec/data`
- **Commands**: Module templates can generate command structures in `app/spec/commands`

## Key Concepts and Patterns

### Template Architecture

The template system implements a specification-driven approach to component generation:

- **Index Templates**: Define user inputs and mapping rules for template generation
- **Specification Templates**: Generate YAML specification files that drive code generation
- **Jinja2 Processing**: Templates use Jinja2 syntax for dynamic content generation
- **Variable Interpolation**: Templates support complex variable processing and conditional logic

### Template Types

Each subdirectory contains templates for specific component types:

- **Cell Templates**: Generate AI prompt templates for different interaction modes
- **Data Templates**: Create data model specifications with customizable fields and relationships
- **Field Templates**: Generate field specifications for various Django field types
- **Function Templates**: Create utility function libraries for template processing
- **Module Templates**: Generate complete module structures with standard directories
- **User Templates**: Create user role specifications with permission definitions

### Naming Conventions

- Template directories are named by their functional domain (e.g., `field`, `data`, `module`)
- Index templates are named `index.yml` and define user inputs and mappings
- Specification templates are named `spec.yml` and generate specification files
- Template files use descriptive names that indicate their purpose
- Variable names follow snake_case convention for consistency

### File Organization

Files are organized by template domain or function:
- Each template type has its own subdirectory (e.g., `field/string`, `data/model`)
- Related templates are grouped in the same directory by functional domain
- Index templates define user interface and mapping rules
- Specification templates define the generated output structure

### Domain-Specific Patterns

- All templates use Jinja2 syntax for dynamic content generation
- Templates define variables with help text for user guidance
- Templates use conditional logic to control output generation
- Templates map generated content to specific specification locations
- Templates support complex data structures through YAML formatting

## Developer Notes and Usage Tips

### Integration Requirements

These templates require:
- Access to the template command system in `app/commands/template`
- Proper template processing in `app/systems/manage/template.py`
- Specification files in `app/spec` for generated content
- Utility functions from `app/utility` for template processing

### Usage Patterns

- Templates are executed through the `template generate` command
- Users provide variable values when generating templates
- Generated specifications are placed in the `spec/auto` directory
- Templates can be customized by modifying the template files
- New templates can be created by following existing patterns

### Dependencies

- Jinja2 template engine for template processing
- YAML parser for specification generation
- Template command system from `app/commands/template`
- Template management system from `app/systems/manage/template.py`

### AI Development Guidance

When generating or modifying templates:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper variable definitions with clear help text
3. Follow established patterns for index and specification templates
4. Respect the separation of concerns between different template domains
5. Consider user experience when designing template interfaces
6. Maintain consistency with existing naming and structure patterns
7. Document all variables with clear help messages
8. Follow the established patterns for conditional logic and mapping
9. Reference existing templates as examples for new implementations
10. Ensure generated specifications properly integrate with the code generation system
