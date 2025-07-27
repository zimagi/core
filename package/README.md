# Zimagi Python Package Directory

## Overview

The `package` directory contains the Zimagi Python SDK client library and command-line interface (CLI) executable. This package provides programmatic access to Zimagi server API endpoints and enables command execution through both Python applications and shell commands.

This directory serves as the client-side implementation that interacts with the Zimagi server application housed in the `app` directory. It plays a critical architectural role by providing:

- A Python SDK for programmatic API interactions
- A CLI tool for executing commands from the terminal
- Client libraries for both command and data API endpoints
- Encryption and authentication utilities for secure communication

The package is primarily used by:

- **Developers** building Python applications that integrate with Zimagi
- **System administrators** managing Zimagi installations through CLI
- **DevOps engineers** automating Zimagi operations in deployment pipelines
- **AI models** understanding client-server interactions and generating integration code

## Directory Contents

### Files

| File             | Purpose                                             | Format |
| ---------------- | --------------------------------------------------- | ------ |
| setup.py         | Python package setup configuration for distribution | Python |
| VERSION          | Contains the current version number of the package  | Text   |
| requirements.txt | Lists Python dependencies required by the package   | Text   |
| deploy.sh        | Script for deploying the package to PyPI repository | Bash   |

### Subdirectories

| Directory | Purpose                                          | Contents                       |
| --------- | ------------------------------------------------ | ------------------------------ |
| bin       | Contains executable scripts                      | CLI entrypoint scripts         |
| zimagi    | Main Python package module with client libraries | Python modules for API clients |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the root project directory which contains top-level project files
- **Server Integration**: Connects to `app` directory which contains the server application implementation
- **Docker Integration**: Works with `docker` directory for containerization of CLI tools
- **Development Platform**: Integrates with `reactor` directory for Kubernetes development
- **CI/CD Pipeline**: Deployed through configurations in `.circleci` directory

The `package` directory serves as the client-side counterpart to the server-side implementation in `app`, providing the tools needed to interact with the Zimagi platform programmatically and through command-line interfaces.

## Key Concepts, Conventions, and Patterns

### Package Architecture

The package implements a dual-client architecture:

- **Command Client**: For executing Zimagi commands and workflows
- **Data Client**: For interacting with data models and performing CRUD operations
- **Transport Layer**: Handles HTTP communication and message processing
- **Codec System**: Manages data serialization and deserialization
- **Security Layer**: Provides encryption and authentication capabilities

### Naming Conventions

- Python modules use lowercase with underscores (e.g., `command_client.py`)
- Class names use PascalCase (e.g., `CommandClient`)
- Private methods and attributes are prefixed with underscores
- Configuration files use descriptive names with appropriate extensions
- CLI scripts are named after their functional purpose

### File Organization

Files are organized by functional domain following these patterns:

- **Client Libraries**: Located in `zimagi` directory organized by API type
- **CLI Tools**: Located in `bin` directory as executable scripts
- **Core Utilities**: Located in `zimagi` root for shared functionality
- **Transport Implementations**: Located in API-specific subdirectories
- **Codec Definitions**: Located in API-specific subdirectories

### Domain-Specific Patterns

- API clients inherit from a common `BaseAPIClient` base class
- Message handling uses a streaming approach for command responses
- Data serialization supports multiple formats (JSON, CSV, YAML)
- Authentication uses token-based security with encryption support
- Error handling follows a consistent exception hierarchy
- Configuration management uses environment variables with defaults

## Developer Notes and Usage Tips

### Integration Requirements

The package requires:

- Python 3.8+ for execution
- Docker for containerized CLI operations
- Access to a running Zimagi server instance
- Proper authentication credentials (user token)
- Network connectivity to server API endpoints

### Usage Patterns

- Use `zimagi` script as the main CLI entrypoint
- Import `zimagi.CommandClient` or `zimagi.DataClient` for Python integration
- Configure clients through environment variables or constructor parameters
- Handle responses using the provided message and data structures
- Follow the exception hierarchy for error handling

### Dependencies

- Python requests library for HTTP communication
- PyCryptodome for encryption operations
- Pandas for data processing
- Terminaltables for formatted output
- Validators for URL validation
- Python-magic for file type detection

### AI Development Guidance

When generating or modifying files in this directory:

1. Maintain consistency with existing client architecture patterns
2. Follow established naming conventions for modules and classes
3. Implement functionality through appropriate API client methods
4. Use the transport and codec system for HTTP communication
5. Follow the exception handling patterns already established
6. Ensure proper integration with authentication and encryption systems
7. Maintain consistency with message handling and response processing
8. Follow the dual-client pattern for command and data operations
9. Respect the separation of concerns between different API domains
10. Use utility functions from the package rather than duplicating functionality
