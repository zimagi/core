# Zimagi Field Templates Directory

## Overview

The `app/templates/field` directory contains Jinja2 template files that provide scaffolding for generating data model field specifications within the Zimagi platform. These templates enable rapid creation of field definitions by providing standardized structures that follow Zimagi's data modeling conventions.

This directory plays a critical architectural role by enabling developers and system administrators to quickly bootstrap new field types with consistent configuration files. The templates work with the dynamic class generation system in `app/systems/manage/template.py` and are consumed by:

- **Developers** creating new Zimagi data model fields
- **System administrators** setting up standardized field configurations
- **AI models** analyzing and generating field components through template processing

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| README.md | This documentation file | Markdown |

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| big_integer | Contains templates for big integer field type generation | index.yml, spec.yml |
| binary | Contains templates for binary field type generation | index.yml, spec.yml |
| boolean | Contains templates for boolean field type generation | index.yml, spec.yml |
| date | Contains templates for date field type generation | index.yml, spec.yml |
| datetime | Contains templates for datetime field type generation | index.yml, spec.yml |
| dict | Contains templates for dictionary field type generation | index.yml, spec.yml |
| duration | Contains templates for duration field type generation | index.yml, spec.yml |
| float | Contains templates for float field type generation | index.yml, spec.yml |
| foreign_key | Contains templates for foreign key field type generation | index.yml, spec.yml |
| integer | Contains templates for integer field type generation | index.yml, spec.yml |
| list | Contains templates for list field type generation | index.yml, spec.yml |
| many_to_many | Contains templates for many-to-many field type generation | index.yml, spec.yml |
| string | Contains templates for string field type generation | index.yml, spec.yml |
| text | Contains templates for text field type generation | index.yml, spec.yml |
| url | Contains templates for URL field type generation | index.yml, spec.yml |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/templates` directory which contains Jinja2 templates for various component systems
- **Template Commands**: Works with `app/commands/template` for template generation functionality
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Specifications**: Templates generate specification files that drive code generation in `app/spec/data`
- **Data Models**: Field templates create data model specifications in `app/spec/data`

## Key Concepts and Patterns

### Template Architecture

The field template system implements a specification-driven approach to field generation:

- **Index Templates**: Define user inputs and mapping rules for template generation (`index.yml`)
- **Specification Templates**: Generate YAML specification files that drive code generation (`spec.yml`)
- **Jinja2 Processing**: Templates use Jinja2 syntax for dynamic content generation
- **Variable Interpolation**: Templates support complex variable processing and conditional logic

### Template Processing System

The template system in `app/systems/manage/template.py` provides:

- **Template Engine**: Custom Jinja2 environment with specialized delimiters (`<{` and `}>` for variables, `#%` and `%#` for blocks)
- **Function Loading**: Automatic loading of template functions from `templates/functions` directories
- **Module Integration**: Scans all module directories for template files and merges them
- **File Operations**: Copying and merging of template files to destination locations

### Template Types

Each subdirectory contains templates for specific field types:

- **Big Integer Field Template**: For big integer fields with nullability, default values, and primary key options
- **Binary Field Template**: For binary data fields with configurable max_length and nullability
- **Boolean Field Template**: For boolean data fields with nullability and default value options
- **Date Field Template**: For date fields with nullability, default values, and primary key options
- **Datetime Field Template**: For datetime fields with nullability, default values, and primary key options
- **Dictionary Field Template**: For dictionary fields with editable options
- **Duration Field Template**: For duration fields with nullability, default values, and editable options
- **Float Field Template**: For float fields with nullability, default values, and primary key options
- **Foreign Key Field Template**: For foreign key relationships with configurable deletion behavior
- **Integer Field Template**: For integer fields with nullability, default values, and primary key options
- **List Field Template**: For list fields with editable options
- **Many To Many Field Template**: For many-to-many relationships with configurable reverse relations
- **String Field Template**: For character fields with configurable max_length, choices, and nullability
- **Text Field Template**: For text fields with nullability and default value options
- **URL Field Template**: For URL fields with configurable max_length and nullability

### Template Structure

Each field template consists of two key files:

- **index.yml**: Defines variables that users can provide when generating the template, including help text and default values
- **spec.yml**: Contains the actual field specification template with Jinja2 variables that get substituted

### Naming Conventions

- Template directories are named by their field type (e.g., `binary`, `boolean`, `string`)
- Index files are consistently named `index.yml`
- Specification files are consistently named `spec.yml`
- Template variables follow snake_case convention for consistency
- Field type names match Django field types where applicable

### File Organization

Files are organized to provide a complete field template structure:
- Each field type has its own subdirectory
- Index and specification templates for each field type
- Standard field directory structure templates

### Domain-Specific Patterns

- All templates use Jinja2 syntax for dynamic content generation
- Templates define variables with help text for user guidance
- Templates use conditional logic to control output generation
- Templates support complex data structures through YAML formatting
- Generated specifications are placed in `spec/auto/data/` directory structure

## Developer Notes and Usage Tips

### Integration Requirements

These templates require:
- Access to the template command system in `app/commands/template`
- Proper template processing in `app/systems/manage/template.py`
- Utility functions from `app/utility` for template processing

### Usage Patterns

- Templates are executed through the `template generate` command
- Users provide variable values when generating templates
- Generated fields follow Zimagi's standard field structure
- Templates can be customized by modifying the template files
- The system automatically loads template functions from the `templates/functions` directory

### Dependencies

- Jinja2 template engine for template processing
- YAML parser for configuration generation
- Template command system from `app/commands/template`
- Template management system from `app/systems/manage/template.py`
- Utility functions from `app/utility` for filesystem operations

### AI Development Guidance

When generating or modifying field templates:

1. Maintain consistency with Zimagi's field structure patterns
2. Ensure proper variable definitions with clear help text
3. Follow established patterns for configuration and metadata templates
4. Respect the separation of concerns between different template components
5. Consider user experience when designing template interfaces
6. Maintain consistency with existing naming and structure patterns
7. Document all variables with clear help messages
8. Follow the established patterns for conditional logic and mapping
9. Reference existing templates as examples for new implementations
10. Ensure generated fields properly integrate with the Zimagi platform
11. Test templates with the `template generate` command to verify functionality
12. Ensure template functions are properly loaded through the ManagerTemplateMixin system
