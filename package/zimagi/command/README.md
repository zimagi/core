# Zimagi Command Package Directory

## Overview

The `package/zimagi/command` directory contains the Python SDK client library for interacting with Zimagi's command API endpoints. This package provides programmatic access to Zimagi's command execution system, enabling developers to execute Zimagi commands through Python applications and shell commands.

This directory serves as the client-side implementation that interacts with the Zimagi server's command system housed in the `app/commands` directory. It plays a critical architectural role by providing:

- A Python SDK for programmatic command execution
- Client libraries for performing command operations through HTTP transport
- Codec implementations for handling command response serialization/deserialization
- Message handling system for processing command execution results

The package is primarily used by:

- **Developers** building Python applications that integrate with Zimagi's command system
- **System administrators** managing Zimagi installations through programmatic interfaces
- **DevOps engineers** automating Zimagi operations in deployment pipelines
- **AI models** understanding client-server command interactions and generating integration code

## Directory Contents

### Files

| File          | Purpose                                                                                                   | Format |
| ------------- | --------------------------------------------------------------------------------------------------------- | ------ |
| **init**.py   | Package initialization file that exposes the Command Client class and related modules                     | Python |
| client.py     | Command API client implementation for executing Zimagi commands and workflows                             | Python |
| codecs.py     | Zimagi JSON codec for parsing command API responses and schema definitions                                | Python |
| messages.py   | Message classes for handling command response messages including status, data, info, warnings, and errors | Python |
| response.py   | Command response handling and processing including message aggregation and error management               | Python |
| schema.py     | Schema definitions for command API structure including root, router, action, field, and error definitions | Python |
| transports.py | HTTP transport implementation for command API requests with streaming message processing                  | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `package/zimagi` directory which contains the Python SDK client library
- **Server Integration**: Connects to `app/commands` directory which contains the server-side command implementations
- **CLI Integration**: Works with the main `zimagi` entrypoint script to provide command-line functionality
- **Package Integration**: Integrates with core package modules in the parent `package/zimagi` directory

The `package/zimagi/command` directory serves as the client-side counterpart to the server-side command implementations in `app/commands`, providing the tools needed to interact with Zimagi's command system programmatically.

## Key Concepts, Conventions, and Patterns

### Package Architecture

The command package implements a client-based architecture for command interactions:

- **Command Client**: For executing Zimagi commands and workflows through the command API
- **Transport Layer**: Handles HTTP communication and message processing for command API requests
- **Codec System**: Manages data serialization and deserialization for command API responses
- **Message Handling**: Processes streaming command responses with different message types
- **Schema Integration**: Provides access to server-side command schema and validation

### Naming Conventions

- Python modules use lowercase with underscores (e.g., `client.py`)
- Class names use PascalCase (e.g., `Client`, `CommandHTTPTransport`)
- Private methods and attributes are prefixed with underscores
- Codec class names indicate their supported media types (e.g., `ZimagiJSONCodec`)
- Message class names indicate their purpose (e.g., `ErrorMessage`, `DataMessage`)

### File Organization

Files are organized by functional domain following these patterns:

- **Client Implementation**: Located in `client.py` for primary command client functionality
- **Transport Layer**: Located in `transports.py` for HTTP communication handling
- **Codec Definitions**: Located in `codecs.py` for data serialization support
- **Message Handling**: Located in `messages.py` for response message processing
- **Response Processing**: Located in `response.py` for command response aggregation
- **Schema Definitions**: Located in `schema.py` for command API structure definitions
- **Package Initialization**: Located in `__init__.py` for module exposure

### Domain-Specific Patterns

- Command client inherits from a common `BaseAPIClient` base class
- Message handling uses a streaming approach for command responses
- Data serialization supports Zimagi-specific JSON format
- Transport implementation handles authentication and encryption automatically
- Codec system provides pluggable data format support
- Schema integration enables dynamic command discovery and validation
- Response processing aggregates multiple message types into a single result

## Developer Notes and Usage Tips

### Integration Requirements

The package requires:

- Python 3.8+ for execution
- Access to a running Zimagi server instance with command API enabled
- Proper authentication credentials (user token)
- Network connectivity to server command API endpoints

### Usage Patterns

- Import `zimagi.command.Client` for Python command integration
- Configure client through environment variables or constructor parameters
- Use client methods like `execute` for command operations
- Handle responses using the provided message and response structures
- Follow the exception hierarchy for error handling

### Dependencies

- Python requests library for HTTP communication
- PyCryptodome for encryption operations
- Package core modules from parent `package/zimagi` directory

### AI Development Guidance

When generating or modifying files in this directory:

1. Maintain consistency with existing client architecture patterns
2. Follow established naming conventions for modules and classes
3. Implement functionality through appropriate client methods
4. Use the transport and codec system for HTTP communication
5. Follow the exception handling patterns already established
6. Ensure proper integration with authentication and encryption systems
7. Maintain consistency with message handling and response processing
8. Follow the client-driven approach where client methods provide interfaces to SDK functionality
9. Respect the separation of concerns between different API domains
10. Use utility functions from the package rather than duplicating functionality
