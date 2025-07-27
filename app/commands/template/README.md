# Zimagi Template Commands Directory

## Overview

The `app/commands/template` directory contains command implementations related to template management within the Zimagi platform. These commands provide functionality for generating templates that can be used to create new modules, components, or other structured content within the platform.

This directory plays a specialized role in the Zimagi command system by providing template-specific operations that help developers and administrators create standardized structures for new components. The commands here are automatically exposed through both CLI interfaces and RESTful API endpoints, enabling consistent access to template generation functionality regardless of the interaction method.

The directory is used by:

- **Developers** working on module and component creation
- **System administrators** managing platform templates and scaffolding
- **AI models** analyzing and generating template management components

## Directory Contents

### Files

| File        | Purpose                                                                                 | Format |
| ----------- | --------------------------------------------------------------------------------------- | ------ |
| generate.py | Implements the template generate command for creating new templates from specifications | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/commands` directory which contains executable commands and agents available through CLI or APIs
- **Specifications**: Command interfaces are defined in `app/spec/commands/template.yml` which drives the command system through YAML specifications
- **Command Systems**: Connects to `app/systems/commands` for command execution framework and dynamic class generation
- **API Systems**: Works with `app/systems/api/command` for REST API exposure of commands
- **Module Systems**: Integrates with `app/commands/module` for module template provisioning
- **Template Systems**: Works with `app/systems/manage/template.py` for template processing and rendering
- **Settings**: Uses configurations defined in `app/settings` for template behavior parameters

## Key Concepts and Patterns

### Command Architecture

The template command system implements a specification-driven approach to command generation:

- YAML specifications in `app/spec/commands/template.yml` define command structures and parameters
- The `app/systems/commands/index.py` module dynamically generates command classes at runtime
- Commands are created with appropriate parsing rules and execution logic
- Base command classes provide consistent interfaces for command extension operations

### Template Operations

The template system implements generation operations based on the specifications in `app/spec/commands/template.yml`:

- **Generate Command** (`generate.py`): Creates new templates from specifications
  - Base: module (inherits from module base command)
  - Priority: 10
  - Parse configurations: Uses module key, template selection, and field parsing
  - Implements template generation with module and template selection
  - Accepts parameters:
    - `module` (string): The module to generate templates for
    - `module_template` (string): The specific template to use
    - `template_fields` (fields): Additional configuration fields for template customization
    - `display_only` (flag): Display template content without actually generating files

### Command Generation Process

The command generation follows Zimagi's dynamic class generation pattern:

- Commands are generated dynamically at runtime through the indexing system in `app/systems/commands/index.py`
- The `Command("template.generate")` function creates the command class by processing the specification
- The command inherits from the base `module` command as defined in the specification
- Mixins and base commands are composed to provide shared functionality

### Naming Conventions

- Command files are named by their functional operation (e.g., `generate.py`)
- Command classes are dynamically generated with appropriate naming following the pattern defined in `app/systems/commands/index.py`
- Method names follow Python conventions with descriptive names
- Command lookup paths follow the hierarchical structure defined in specifications

### File Organization

Files are organized by template management operation:

- Each template operation has its own file
- Related template functionality is grouped in this directory
- Files implement specific command operations as defined in the specifications

### Domain-Specific Patterns

- All template commands integrate with the command facade pattern through inheritance
- Error handling follows consistent patterns with custom exception classes
- Integration with template management systems for rendering operations through the provision_template method
- Support for both synchronous and asynchronous execution patterns
- Parameter parsing follows specification-defined structures with typed parameters
- Commands use field-based parsing for flexible template configuration
- Template generation supports display-only mode for previewing without actual file creation

## Developer Notes and Usage Tips

### Integration Requirements

These commands require:

- Django framework access for settings and configuration management
- Proper command specification files in `app/spec/commands/template.yml` for command generation
- Access to template management systems in `app/systems/manage` for template processing
- Utility functions from `app/utility` for common operations
- Command system from `app/systems/commands` for dynamic generation and indexing

### Usage Patterns

- Template commands are accessed through the indexing system in `app/systems/commands/index.py` using the `Command()` function
- Implement commands by extending base command classes or using the specification-driven approach
- Follow established patterns for template management operations
- Access command functionality through the standard Zimagi command execution system
- Use `find_command()` function to retrieve command instances by name

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command specifications from `app/spec/commands/template.yml` for generation
- Template management system from `app/systems/manage` for template processing
- Command system from `app/systems/commands` for dynamic generation and execution

### AI Development Guidance

When generating or modifying template commands:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with command-specific exception classes
3. Follow established patterns for template management operations
4. Respect the separation of concerns between different template operations
5. Consider performance implications for template operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing template commands as examples for new implementations
10. Ensure command specifications in `app/spec/commands/template.yml` properly define the interface with appropriate base commands and mixins
11. Understand the two-stage class generation process (dynamic base classes and overlay classes)
12. Follow the metadata structure defined in command specifications for requirements and options
