# Zimagi Database Commands Directory

## Overview

The `app/commands/db` directory contains command implementations related to database management within the Zimagi platform. These commands provide functionality for database backup, restore, snapshot management, and cleanup operations, enabling administrators to maintain and manage the platform's data persistence layer effectively.

This directory plays a specialized role in the Zimagi command system by providing database-specific operations that help maintain data integrity, enable disaster recovery, and manage storage resources. The commands here are automatically exposed through both CLI interfaces and RESTful API endpoints, enabling consistent access to database management functionality regardless of the interaction method.

The directory is used by:

- **Developers** working on data management and database administration
- **System administrators** managing Zimagi deployments and data operations
- **AI models** analyzing and generating command components

## Directory Contents

### Files

| File         | Purpose                                                                                      | Format |
| ------------ | -------------------------------------------------------------------------------------------- | ------ |
| backup.py    | Implements the database backup command for creating snapshots of the current database state  | Python |
| clean.py     | Implements the database clean command for removing old snapshots based on retention policies | Python |
| restore.py   | Implements the database restore command for restoring database state from snapshots          | Python |
| snapshots.py | Implements the snapshots listing command for displaying available database snapshots         | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/commands` directory which contains executable commands and agents available through CLI or APIs
- **Specifications**: Command interfaces are defined in `app/spec/commands/database.yml` which drives the command system through YAML specifications
- **Command Systems**: Connects to `app/systems/commands` for command execution framework and dynamic class generation
- **API Systems**: Works with `app/systems/api/command` for REST API exposure of commands
- **Database Systems**: Integrates with `app/systems/db` for database management operations
- **Settings**: Uses configurations defined in `app/settings` for database behavior parameters

## Key Concepts and Patterns

### Command Architecture

The database command system implements a specification-driven approach to command generation:

- YAML specifications in `app/spec/commands/database.yml` define command structures and parameters
- The `app/systems/commands/index.py` module dynamically generates command classes at runtime
- Commands are created with appropriate parsing rules and execution logic
- Base command classes provide consistent interfaces for command extension operations

### Database Operations

The database system implements several critical operations:

- **Snapshots Command** (`snapshots.py`): Lists available database snapshots

  - Base: db
  - Priority: 50
  - Parse configurations: Uses the db mixin's parsing capabilities

- **Backup Command** (`backup.py`): Creates database snapshots for backup purposes

  - Base: db
  - Priority: 55
  - Parse configurations: Uses the db mixin's parsing capabilities

- **Restore Command** (`restore.py`): Restores database state from existing snapshots

  - Base: db
  - Priority: 60
  - Requires confirmation for execution
  - Parse configurations: Uses the db mixin's parsing capabilities
  - Parameters: snapshot_name, force

- **Clean Command** (`clean.py`): Removes old database snapshots based on retention policies
  - Base: db
  - Priority: 65
  - Parse configurations: Uses the db mixin's parsing capabilities
  - Parameters: keep_num (optional flag --keep, default from settings.DB_SNAPSHOT_RENTENTION)

### Naming Conventions

- Command files are named by their functional operation (e.g., `backup.py`, `restore.py`)
- Command classes extend the base command with the command name as a parameter using `Command("db.operation")`
- Method names follow Python conventions with descriptive names

### File Organization

Files are organized by database management operation:

- Each database operation has its own file
- Related database functionality is grouped in this directory

### Domain-Specific Patterns

- All database commands integrate with the command facade pattern through inheritance
- Error handling follows consistent patterns with custom exception classes
- Integration with database management systems for data operations
- Commands follow the priority-based execution model defined in the command specification

## Developer Notes and Usage Tips

### Integration Requirements

These commands require:

- Django framework access for settings and configuration management
- Proper command specification files in `app/spec/commands/database.yml` for command generation
- Access to database systems in `app/systems/db` for database operations
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Database commands are accessed through the indexing system in `app/systems/commands/index.py` using the `Command()` function
- Implement commands by extending base command classes
- Follow established patterns for database management operations
- Access command functionality through the standard Zimagi command execution system

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command specifications from `app/spec/commands/database.yml` for generation
- Database system from `app/systems/db` for database operations

### AI Development Guidance

When generating or modifying database commands:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with command-specific exception classes
3. Follow established patterns for database management operations
4. Respect the separation of concerns between different database operations
5. Consider performance implications for database operations
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing database commands as examples for new implementations
10. Ensure command specifications in `app/spec/commands/database.yml` properly define the interface with appropriate base commands and mixins
