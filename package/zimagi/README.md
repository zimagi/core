# Zimagi Python SDK Package Directory

## Overview

The `package/zimagi` directory contains the Python SDK client library for interacting with the Zimagi server API endpoints. This package provides programmatic access to Zimagi server functionality and enables command execution through both Python applications and shell commands.

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

| File                  | Purpose                                                                               | Format |
| --------------------- | ------------------------------------------------------------------------------------- | ------ |
| **init**.py           | Package initialization file that exposes core client classes and modules              | Python |
| auth.py               | Authentication implementation using token-based security for API requests             | Python |
| client.py             | Base API client class that provides common functionality for command and data clients | Python |
| codecs.py             | JSON codec implementation for decoding API responses                                  | Python |
| collection.py         | Collection classes for handling structured data objects                               | Python |
| command/**init**.py   | Command client module initialization                                                  | Python |
| command/client.py     | Command API client implementation for executing Zimagi commands                       | Python |
| command/codecs.py     | Zimagi JSON codec for parsing command API responses                                   | Python |
| command/messages.py   | Message classes for handling command response messages                                | Python |
| command/response.py   | Command response handling and processing                                              | Python |
| command/schema.py     | Schema definitions for command API structure                                          | Python |
| command/transports.py | HTTP transport implementation for command API requests                                | Python |
| data/**init**.py      | Data client module initialization                                                     | Python |
| data/client.py        | Data API client implementation for interacting with Zimagi data models                | Python |
| data/codecs.py        | Codecs for handling data API responses including CSV and OpenAPI JSON                 | Python |
| data/transports.py    | HTTP transport implementation for data API requests                                   | Python |
| datetime.py           | Time handling utilities with timezone support                                         | Python |
| encryption.py         | Encryption utilities implementing AES cipher for secure communication                 | Python |
| exceptions.py         | Exception hierarchy for handling client errors                                        | Python |
| parallel.py           | Parallel processing utilities for concurrent operations                               | Python |
| settings.py           | Configuration settings for the SDK including defaults and timeouts                    | Python |
| transports.py         | Base transport classes for HTTP communication                                         | Python |
| utility.py            | Utility functions for data handling, caching, formatting, and validation              | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `package` directory which contains the Python SDK client library (see package/README.md)
- **Server Integration**: Connects to `app` directory which contains the server application implementation
- **CLI Integration**: Works with the main `zimagi` entrypoint script to provide command-line functionality
- **Docker Integration**: Used by Docker configurations in the `docker` directory for containerized CLI operations

The `package/zimagi` directory serves as the client-side counterpart to the server-side implementation in `app`, providing the tools needed to interact with the Zimagi platform programmatically and through command-line interfaces.

## Key Concepts, Conventions, and Patterns

### Package Architecture

The package implements a dual-client architecture:

- **Command Client**: For executing Zimagi commands and workflows through the command API
- **Data Client**: For interacting with data models and performing CRUD operations through the data API
- **Transport Layer**: Handles HTTP communication and message processing for both APIs
- **Codec System**: Manages data serialization and deserialization for API responses
- **Security Layer**: Provides encryption and authentication capabilities for secure communication

### Naming Conventions

- Python modules use lowercase with underscores (e.g., `command_client.py`)
- Class names use PascalCase (e.g., `CommandClient`)
- Private methods and attributes are prefixed with underscores
- Configuration files use descriptive names with appropriate extensions

### File Organization

Files are organized by functional domain following these patterns:

- **Client Libraries**: Located at the root level for command and data API clients
- **API-Specific Modules**: Located in `command` and `data` subdirectories for API-specific functionality
- **Core Utilities**: Located at the root level for shared functionality
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
- Access to a running Zimagi server instance
- Proper authentication credentials (user token)
- Network connectivity to server API endpoints

### Usage Patterns

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
