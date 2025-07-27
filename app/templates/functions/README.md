# Zimagi Template Functions Directory

## Overview

The `app/templates/functions` directory contains Python modules that provide utility functions for the Zimagi platform's template processing system. These functions are used within Jinja2 templates to perform common operations such as text processing, data manipulation, and class name formatting during the template generation process.

This directory plays a specialized role in the Zimagi template system by providing reusable function libraries that can be imported and used within templates to generate consistent and properly formatted code components. The functions here are consumed by:

- **Developers** working on template generation and component scaffolding
- **System administrators** creating new modules and data structures through templates
- **AI models** analyzing and generating template-based components

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| core_class.py | Provides class-related utility functions for name formatting and transformation | Python |
| core_list.py | Implements list processing functions for data manipulation in templates | Python |
| core_text.py | Contains text processing functions for string manipulation and pattern matching | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/templates` directory which contains Jinja2 templates for component generation
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Specifications**: Template functions are used in templates that generate specification files in `app/spec`
- **Commands**: Works with `app/commands/template` for template generation functionality

## Key Concepts and Patterns

### Function Categories

The template functions are organized by functional domain:

- **Class Functions** (`core_class.py`): Functions for class name manipulation and formatting
- **List Functions** (`core_list.py`): Functions for processing and manipulating list data structures
- **Text Functions** (`core_text.py`): Functions for string manipulation and text processing

### Naming Conventions

- Files are named by their functional domain with `core_` prefix (e.g., `core_class.py`, `core_list.py`)
- Function names are descriptive and indicate their specific purpose
- Functions follow Python naming conventions with snake_case

### File Organization

Files are organized by functional domain:
- Each file contains functions related to a specific data type or processing category
- Related functionality is grouped within the same file
- Functions are designed to be imported and used within Jinja2 templates

### Domain-Specific Patterns

- All functions are designed to be simple and stateless for use in template contexts
- Functions accept and return basic Python data types that can be easily serialized
- Error handling follows consistent patterns with clear error messages
- Functions are designed to be composable and reusable across different template contexts

## Developer Notes and Usage Tips

### Integration Requirements

These functions require:
- Python interpreter for execution within template contexts
- Access to the template processing system in `app/systems/manage/template.py`
- Proper function imports in Jinja2 templates where functionality is needed

### Usage Patterns

- Functions are imported into templates using the template system's function loading mechanism
- Use existing functions as examples for implementing new template utility functions
- Follow established patterns for function signatures and return value types
- Ensure functions are compatible with Jinja2's template execution environment

### Dependencies

- Standard Python libraries for data processing
- Template system from `app/systems/manage` for function registration and execution

### AI Development Guidance

When generating or modifying template functions:

1. Maintain consistency with existing function patterns and naming conventions
2. Ensure functions are simple, stateless, and focused on a single purpose
3. Follow established patterns for parameter handling and return value formatting
4. Respect the separation of concerns between different functional domains
5. Consider performance implications for template processing operations
6. Maintain consistency with existing naming and API patterns
7. Document all public functions with clear docstrings
8. Follow the established patterns for integration with the template system

## Function Reference

### Core Class Functions (core_class.py)

- `class_name(name)`: Converts a snake_case or space-separated string to PascalCase class name

### Core List Functions (core_list.py)

- `ensure_list(value)`: Ensures the input value is converted to a list format
- `comma_separated_value(value)`: Converts a list to a comma-separated string or returns the string value

### Core Text Functions (core_text.py)

- `split_text(text, pattern)`: Splits text using a regular expression pattern
