# Zimagi Data Client Package Directory

## Overview

The `package/zimagi/data` directory contains the Python SDK client library for interacting with Zimagi's data API endpoints. This package provides programmatic access to Zimagi's data models and enables CRUD operations through both Python applications and shell commands.

This directory serves as the client-side implementation that interacts with the Zimagi server's data layer housed in the `app/data` directory. It plays a critical architectural role by providing:
- A Python SDK for programmatic data model interactions
- Client libraries for performing CRUD operations on Zimagi data models
- Codec implementations for handling data serialization/deserialization
- Transport mechanisms for secure HTTP communication

The package is primarily used by:
- **Developers** building Python applications that integrate with Zimagi's data layer
- **System administrators** managing Zimagi data through programmatic interfaces
- **DevOps engineers** automating Zimagi data operations in deployment pipelines
- **AI models** understanding client-server data interactions and generating integration code

## Directory Contents

### Files

| File | Purpose | Format |
|------|---------|--------|
| __init__.py | Package initialization file that exposes the Data Client class | Python |
| client.py | Data API client implementation for interacting with Zimagi data models | Python |
| codecs.py | Codec implementations for handling data responses including CSV and OpenAPI JSON | Python |
| transports.py | HTTP transport implementation for data API requests | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `package/zimagi` directory which contains the Python SDK client library (see package/zimagi/README.md)
- **Server Integration**: Connects to `app/data` directory which contains the server-side data model implementations
- **CLI Integration**: Works with the main `zimagi` entrypoint script to provide data command functionality
- **Package Integration**: Integrates with core package modules in the parent `package/zimagi` directory

The `package/zimagi/data` directory serves as the client-side counterpart to the server-side data implementations in `app/data`, providing the tools needed to interact with Zimagi data models programmatically.

## Key Concepts, Conventions, and Patterns

### Package Architecture

The data package implements a client-based architecture for data interactions:

- **Data Client**: For interacting with data models and performing CRUD operations
- **Transport Layer**: Handles HTTP communication for data API requests
- **Codec System**: Manages data serialization and deserialization for API responses
- **Schema Integration**: Provides access to server-side data model schemas

### Naming Conventions

- Python modules use lowercase with underscores (e.g., `client.py`)
- Class names use PascalCase (e.g., `Client`, `DataHTTPTransport`)
- Private methods and attributes are prefixed with underscores
- Codec class names indicate their supported media types (e.g., `CSVCodec`)

### File Organization

Files are organized by functional domain following these patterns:

- **Client Implementation**: Located in `client.py` for primary data client functionality
- **Transport Layer**: Located in `transports.py` for HTTP communication handling
- **Codec Definitions**: Located in `codecs.py` for data serialization support
- **Package Initialization**: Located in `__init__.py` for module exposure

### Domain-Specific Patterns

- Data client inherits from a common `BaseAPIClient` base class
- Data serialization supports multiple formats (JSON, CSV, OpenAPI JSON)
- Transport implementation handles authentication and encryption automatically
- Codec system provides pluggable data format support
- Schema integration enables dynamic field and relationship discovery

## Developer Notes and Usage Tips

### Integration Requirements

The package requires:

- Python 3.8+ for execution
- Access to a running Zimagi server instance with data API enabled
- Proper authentication credentials (user token)
- Network connectivity to server data API endpoints

### Usage Patterns

- Import `zimagi.DataClient` for Python data integration
- Configure client through environment variables or constructor parameters
- Use client methods like `get`, `list`, `create`, `update`, and `delete` for data operations
- Handle responses using the provided data structures
- Follow the exception hierarchy for error handling

### Dependencies

- Python requests library for HTTP communication
- Pandas for CSV data processing
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
7. Maintain consistency with schema discovery and field handling
8. Follow the CRUD pattern for data operations (create, read, update, delete)
9. Respect the separation of concerns between different API domains
10. Use utility functions from the package rather than duplicating functionality
