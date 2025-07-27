# Zimagi Help Directory

## Overview

The `app/help` directory contains language-based help information for Zimagi commands. This directory serves as the centralized location for all user-facing documentation that explains how to use various Zimagi commands and features.

This directory plays a critical role in the user experience by providing clear, structured help content that can be accessed through the CLI interface. The help system is organized by command domains, with each YAML file containing structured documentation for a specific command group.

The help content is consumed by:

- **End users** accessing command help through the Zimagi CLI
- **Developers** implementing new commands who need to understand existing help patterns
- **AI models** generating or updating help content for new functionality
- **Documentation systems** that may extract this content for external documentation

## Directory Contents

### Files

| File             | Purpose                                                    | Format |
| ---------------- | ---------------------------------------------------------- | ------ |
| cache.yml        | Help content for cache management commands                 | YAML   |
| config.yml       | Help content for environment configuration commands        | YAML   |
| dataset.yml      | Help content for environment dataset commands              | YAML   |
| db.yml           | Help content for database management commands              | YAML   |
| environment.yml  | Help content for environment information and host commands | YAML   |
| group.yml        | Help content for environment group management commands     | YAML   |
| import.yml       | Help content for data import commands                      | YAML   |
| log.yml          | Help content for command log entry management              | YAML   |
| module.yml       | Help content for environment module management commands    | YAML   |
| notification.yml | Help content for command notification management           | YAML   |
| schedule.yml     | Help content for command schedule management               | YAML   |
| service.yml      | Help content for local Zimagi service management           | YAML   |
| state.yml        | Help content for environment state management              | YAML   |
| user.yml         | Help content for system user management commands           | YAML   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app` directory which contains all server application files (see app/README.md)
- **Command System**: Connects to `app/commands` where executable commands are implemented
- **CLI Integration**: Works with the main `zimagi` entrypoint script to provide help content to users
- **API Documentation**: Provides the source content for command documentation in the API

## Key Concepts, Conventions, and Patterns

### Help Architecture

The help system implements a structured approach to command documentation:

- **YAML-based Definition**: Help content is defined using YAML syntax with a structured hierarchy
- **Command-based Organization**: Each file represents help content for a specific command domain
- **Multi-level Documentation**: Provides both overview and detailed descriptions for commands and subcommands
- **Consistent Structure**: All help files follow the same YAML structure for consistency

### File Organization

Files are organized by command domain:

- Each YAML file corresponds to a specific command group (e.g., `config.yml` for configuration commands)
- Files contain structured help content for commands and their subcommands
- Content is organized in a hierarchy that matches the command structure

### Naming Conventions

- Files are named after their corresponding command (e.g., `config.yml` for the `config` command)
- YAML keys follow the command hierarchy (e.g., `command.subcommand.property`)
- Property names are descriptive and consistent across files (overview, description, etc.)

### Domain-Specific Patterns

- Help files contain both `overview` (short description) and `description` (detailed explanation) for each command
- Parameter documentation follows the format `parameter_name` for required parameters
- Optional parameters are documented with the `Optional` prefix
- Command examples and usage patterns are included in descriptions where relevant

## Developer Notes and Usage Tips

### Integration Requirements

These help files require:

- Proper YAML syntax formatting
- Consistent structure across all files
- Accurate command and parameter names that match implementations
- Clear, user-focused language that explains functionality

### Usage Patterns

- Help content is automatically loaded by the CLI when users request help
- New commands should have corresponding help entries added to the appropriate YAML file
- Help content should be updated whenever command functionality changes
- Follow existing patterns when adding new help content

### Dependencies

- YAML parsing capabilities for help content loading
- CLI infrastructure that can display help content to users
- Command implementations in `app/commands` that the help documents

### AI Development Guidance

When generating or modifying help content:

1. Maintain consistency with existing YAML structure and formatting
2. Ensure all required command properties are documented
3. Follow established naming conventions for help file identifiers
4. Use clear, user-focused language that explains functionality without assuming expertise
5. Reference existing help files as examples for new implementations
6. Ensure parameter documentation matches actual command implementations
7. Maintain consistency with the structured approach to command documentation
8. Follow the pattern of providing both overview and detailed descriptions
9. Respect the separation of concerns between different command domains
10. Follow the specification-driven approach where help content is defined through structured YAML rather than free-form text
