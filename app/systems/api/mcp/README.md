# Zimagi MCP API Systems Directory

## Overview

The `app/systems/api/mcp` directory contains Python modules that implement the Model Context Protocol (MCP) API functionality for the Zimagi platform. These modules provide the foundational systems for exposing Zimagi commands and tools through the MCP standard, enabling AI agents and external systems to interact with Zimagi services programmatically via a standardized protocol.

This directory plays a critical architectural role by centralizing all MCP API-related operations and providing consistent interfaces for AI integration across the Zimagi platform. The modules here are consumed by:

- **Developers** working on AI integration and MCP API endpoints
- **System administrators** managing API configurations and security
- **AI models** analyzing and generating MCP API components
- **External AI agents** interacting with Zimagi services through MCP

## Directory Contents

### Files

| File      | Purpose                                                          | Format |
| --------- | ---------------------------------------------------------------- | ------ |
| auth.py   | Implements authentication and permissions for MCP API endpoints  | Python |
| client.py | Implements client functionality for MCP server interactions      | Python |
| errors.py | Defines custom exception classes for MCP operations              | Python |
| routes.py | Implements URL routing and connection handling for MCP endpoints | Python |
| tools.py  | Implements tool indexing and execution for MCP integration       | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/systems/api` directory which contains integrated systems implementing API components
- **API Systems**: Connects to the broader API system in `app/systems/api` for consistent API behavior
- **Command Systems**: Integrates with `app/systems/commands` for exposing commands as MCP tools
- **Settings**: Uses configurations defined in `app/settings` for MCP API parameters
- **Utility Systems**: Leverages utilities in `app/utility` for data handling and response processing

## Key Concepts and Patterns

### MCP API Architecture

The MCP API system implements the Model Context Protocol standard for AI integration:

- Automatic generation of MCP tools based on Zimagi command specifications
- Authentication and authorization through Zimagi's user system
- Tool listing and execution endpoints compliant with MCP standards
- Integration with Zimagi's command execution framework

### Authentication Patterns

The MCP API implements consistent authentication mechanisms:

- Bearer token-based authentication with user validation
- Integration with the platform's user and group systems
- Role-based access control for tool execution permissions

### Tool Generation

MCP tools are automatically generated from Zimagi commands:

- Command parameters are converted to MCP tool input schemas
- Command execution results are formatted as MCP-compatible responses
- Access control is enforced based on user permissions

### Response Handling

MCP responses follow consistent patterns:

- Standardized error handling with descriptive messages
- Support for various content types including text and images
- Proper formatting of command output for AI consumption

### Naming Conventions

- Files are named by their functional domain (auth, client, routes, etc.)
- Classes follow descriptive naming with appropriate suffixes
- Methods use clear, descriptive names that indicate their purpose

### File Organization

Files are organized by MCP API functional domain:

- Core MCP functionality in top-level files
- Each file handles a specific aspect of MCP API operations

### Domain-Specific Patterns

- All MCP operations respect the Model Context Protocol standards
- Error handling uses custom exception classes for MCP-specific errors
- Integration with Zimagi's command system for tool execution
- Support for both synchronous and asynchronous MCP operations

## Developer Notes and Usage Tips

### Integration Requirements

These modules require:

- Django framework access for REST framework integration
- Proper command configurations in `app/systems/commands` for tool exposure
- Access to the authentication system for secure communications
- Utility functions from `app/utility` for data processing

### Usage Patterns

- Use the authentication classes to implement MCP API security
- Implement tool generation through the provided tool indexing functionality
- Follow the established patterns for response handling and error management
- Use the client functionality for testing MCP server interactions

### Dependencies

- Django framework for API functionality
- Model Context Protocol SDK for MCP compliance
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command system from `app/systems/commands` for tool execution

### AI Development Guidance

When generating or modifying MCP API systems:

1. Maintain consistency with the Model Context Protocol standards
2. Ensure proper error handling with MCP-specific exception classes
3. Follow established patterns for authentication and authorization
4. Respect the separation of concerns between different MCP domains
5. Consider performance implications for MCP operations that may be called frequently
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for tool generation and execution
