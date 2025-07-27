# Zimagi Module Templates Directory

## Overview

The `app/templates/module` directory contains Jinja2 template files that provide scaffolding for creating new Zimagi modules. These templates enable rapid module generation by providing standardized structures and configurations that follow Zimagi's module development conventions.

This directory plays a critical architectural role by enabling developers and system administrators to quickly bootstrap new modules with consistent directory structures, configuration files, and deployment scripts. The templates work with the dynamic class generation system in `app/systems/manage/template.py` and are consumed by:

- **Developers** creating new Zimagi modules
- **System administrators** setting up standardized module environments
- **AI models** analyzing and generating module components through template processing

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| README.md | This documentation file | Markdown |

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| standard | Contains the standard module template structure | Template files for module creation including .gitignore, LICENSE, django.py, install.sh, requirements.txt, and zimagi.yml |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/templates` directory which contains Jinja2 templates for various component systems
- **Template Commands**: Works with `app/commands/template` for template generation functionality
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Module System**: Templates generate module structures that integrate with `app/commands/module` and `app/data/module`
- **Specifications**: Templates can generate specification files that drive code generation in `app/spec`

## Key Concepts and Patterns

### Template Architecture

The module template system implements a specification-driven approach to module generation:

- **Index Templates**: Define user inputs and mapping rules for template generation
- **Configuration Templates**: Generate YAML configuration files that define module metadata
- **Jinja2 Processing**: Templates use Jinja2 syntax for dynamic content generation
- **Variable Interpolation**: Templates support complex variable processing and conditional logic

### Template Types

The directory contains templates for standard module creation:

- **Standard Module Template**: Complete module structure with all required files and directories
- **Configuration Templates**: Module metadata and settings files
- **Dependency Templates**: Requirements and installation scripts
- **License Templates**: Standard licensing information

### Naming Conventions

- Template files use descriptive names that indicate their purpose
- Configuration files follow standard naming conventions (zimagi.yml, requirements.txt)
- Script files use appropriate extensions (.sh for bash scripts)
- Template variables follow snake_case convention for consistency

### File Organization

Files are organized to provide a complete module template structure:
- Root configuration and metadata files
- Installation and dependency management files
- Standard module directories and structure templates

### Domain-Specific Patterns

- All templates use Jinja2 syntax for dynamic content generation
- Templates define variables with help text for user guidance
- Templates use conditional logic to control output generation
- Templates support complex data structures through YAML formatting

## Developer Notes and Usage Tips

### Integration Requirements

These templates require:
- Access to the template command system in `app/commands/template`
- Proper template processing in `app/systems/manage/template.py`
- Utility functions from `app/utility` for template processing

### Usage Patterns

- Templates are executed through the `template generate` command
- Users provide variable values when generating templates
- Generated modules follow Zimagi's standard module structure
- Templates can be customized by modifying the template files

### Dependencies

- Jinja2 template engine for template processing
- YAML parser for configuration generation
- Template command system from `app/commands/template`
- Template management system from `app/systems/manage/template.py`

### AI Development Guidance

When generating or modifying module templates:

1. Maintain consistency with Zimagi's module structure patterns
2. Ensure proper variable definitions with clear help text
3. Follow established patterns for configuration and metadata templates
4. Respect the separation of concerns between different template components
5. Consider user experience when designing template interfaces
6. Maintain consistency with existing naming and structure patterns
7. Document all variables with clear help messages
8. Follow the established patterns for conditional logic and mapping
9. Reference existing templates as examples for new implementations
10. Ensure generated modules properly integrate with the Zimagi platform
