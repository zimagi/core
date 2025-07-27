# Zimagi Cell Templates Directory

## Overview

The `app/templates/cell` directory contains Jinja2 template files that provide scaffolding for generating AI cell prompt configurations within the Zimagi platform. These templates enable rapid creation of standardized prompt structures that follow Zimagi's conversational AI patterns and specification-driven development approach.

This directory plays a critical architectural role by enabling developers and system administrators to quickly bootstrap new AI cell configurations with consistent prompt structures that integrate seamlessly with the platform's dynamic code generation system. The templates work with the template processing system in `app/systems/manage/template.py` and are consumed by:

- **Developers** creating new Zimagi AI cell configurations
- **System administrators** setting up standardized AI prompt environments
- **AI models** analyzing and generating AI cell components through template processing

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| README.md | This documentation file | Markdown |

### Subdirectories

| Directory | Purpose | Contents |
|----------|---------|----------|
| prompt | Contains prompt template files for different AI interaction modes | Chat, system, assistant, tools, and default prompt templates |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/templates` directory which contains Jinja2 templates for various component systems
- **Template Commands**: Works with `app/commands/template` for template generation functionality
- **Template System**: Connects to `app/systems/manage/template.py` for template processing and rendering
- **Specifications**: Templates generate specification files that drive code generation in `app/spec`
- **Cell Systems**: Generated templates create AI cell configurations that integrate with `app/systems/cell`

## Key Concepts and Patterns

### Template Architecture

The cell template system implements a specification-driven approach to AI prompt generation:

- **Prompt Templates**: Define standardized structures for different AI interaction modes
- **Jinja2 Processing**: Templates use Jinja2 syntax for dynamic content generation
- **Variable Interpolation**: Templates support complex variable processing and conditional logic

### Template Types

The directory contains templates for various AI cell prompt types:

- **Chat Templates**: For interactive conversational interfaces
- **System Templates**: For primary system instructions and rule definitions
- **Assistant Templates**: For AI assistant interface configurations
- **Tools Templates**: For tool availability and execution patterns
- **Default Templates**: For general request handling patterns

### Naming Conventions

- Template files follow descriptive naming conventions that indicate their purpose
- Prompt templates use clear, domain-specific names
- Template variables follow snake_case convention for consistency
- Directory structures organize templates by functional domain

### File Organization

Files are organized to provide complete AI cell template structures:
- Each prompt type has its own template file
- Related prompt functionality is grouped by interaction mode
- Standard AI cell directory structure templates

### Domain-Specific Patterns

- All templates use Jinja2 syntax for dynamic content generation
- Templates define variables with help text for user guidance
- Templates use conditional logic to control output generation
- Templates support complex data structures through YAML formatting
- Generated prompts integrate with Zimagi's AI cell architecture

## Developer Notes and Usage Tips

### Integration Requirements

These templates require:
- Access to the template command system in `app/commands/template`
- Proper template processing in `app/systems/manage/template.py`
- Utility functions from `app/utility` for template processing

### Usage Patterns

- Templates are executed through the `template generate` command
- Users provide variable values when generating templates
- Generated AI cell configurations follow Zimagi's standard AI interaction patterns
- Templates can be customized by modifying the template files

### Dependencies

- Jinja2 template engine for template processing
- YAML parser for configuration generation
- Template command system from `app/commands/template`
- Template management system from `app/systems/manage/template.py`

### AI Development Guidance

When generating or modifying cell templates:

1. Maintain consistency with Zimagi's AI interaction patterns
2. Ensure proper variable definitions with clear help text
3. Follow established patterns for prompt and instruction templates
4. Respect the separation of concerns between different template components
5. Consider user experience when designing template interfaces
6. Maintain consistency with existing naming and structure patterns
7. Document all variables with clear help messages
8. Follow the established patterns for conditional logic and mapping
9. Reference existing templates as examples for new implementations
10. Ensure generated AI cell configurations properly integrate with the Zimagi platform's AI systems
