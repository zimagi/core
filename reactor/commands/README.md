# Zimagi Reactor Commands Directory

## Overview

The `reactor/commands` directory contains Bash script implementations that extend the Zimagi CLI with Kubernetes-specific command functionality. This directory serves as the command layer for the Reactor Kubernetes development platform, providing developers with specialized commands for containerized development workflows.

This directory plays a critical architectural role by bridging local development environments with Kubernetes-based deployments through Docker containerization. It enables developers to execute Zimagi operations within the reactor environment context without needing to manage complex Kubernetes configurations directly.

The command implementations are primarily used by:

- **Developers** working on Zimagi applications in Kubernetes environments
- **DevOps engineers** managing containerized deployments
- **AI models** understanding development platform integration and generating command implementations

## Directory Contents

### Files

| File      | Purpose                                                                                                | Format |
| --------- | ------------------------------------------------------------------------------------------------------ | ------ |
| zimagi.sh | Implements the `zimagi` command that executes Zimagi operations within the reactor environment context | Bash   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `reactor` directory which provides Kubernetes development and management platform integration (see reactor/README.md)
- **CLI Integration**: Connects to the main `zimagi` executable in the reactor directory for command extension
- **Docker Integration**: Works with `docker` directory for containerization of CLI tools and applications
- **Environment Configuration**: Uses environment setup from `reactor/utilities` for consistent execution contexts

The `reactor/commands` directory serves as the command implementation layer that extends the base zimagi CLI with Kubernetes-specific functionality, connecting to Docker containerization in `docker` and environment management in `reactor/utilities`.

## Key Concepts, Conventions, and Patterns

### Command Architecture

The command implementations follow a modular extension pattern:

- **Function-Based Implementation**: Commands are implemented as Bash functions that extend the base CLI
- **Environment Integration**: Commands automatically configure execution environments through utility functions
- **Docker Containerization**: Commands execute within Docker containers for consistent runtime environments
- **Pass-through Arguments**: Commands support passing arguments directly to underlying Zimagi operations

### Naming Conventions

- Bash scripts are named after the command they implement (e.g., `zimagi.sh`)
- Function names use descriptive verb-noun patterns with clear purposes
- Command descriptions use standardized documentation patterns
- File extensions follow Unix conventions with `.sh` for Bash scripts

### File Organization

Files are organized by command functionality:

- Each command implementation is contained in a separate script file
- Files are named to match the command they implement
- All command logic is contained within function definitions

### Domain-Specific Patterns

- Commands use standardized environment variable patterns for Docker integration
- Implementation follows consistent argument passing and execution patterns
- Commands automatically handle Docker image management and container setup
- Integration with the reactor platform through environment configuration utilities

## Developer Notes and Usage Tips

### Integration Requirements

The command implementations require:

- Docker for containerized execution of command operations
- Proper network connectivity to Docker Hub for image downloads
- Environment variables for configuration (automatically handled)
- Access to project directories for volume mounting in Docker containers

### Usage Patterns

- Commands are executed through the main `zimagi` script in the reactor directory
- Function implementations follow consistent patterns for environment setup and execution
- Commands automatically handle Docker container creation and cleanup
- Arguments are passed through to underlying Zimagi operations within containers

### Dependencies

- Docker for containerized execution
- Bash shell environment
- Network connectivity to Docker Hub
- Access to project directories for volume mounting

### AI Development Guidance

When generating or modifying command implementations in this directory:

1. Maintain consistency with existing command function patterns
2. Follow Unix conventions for executable script naming and structure
3. Ensure proper integration with Docker containerization and Kubernetes deployment
4. Implement environment variable handling through established patterns
5. Follow the pattern of providing both local development and production execution modes
6. Maintain consistency with error handling and exit code patterns
7. Ensure commands properly integrate with the zimagi CLI and reactor platform
8. Respect the separation between command implementation and environment configuration
9. Follow the client-driven approach where commands provide interfaces to development platform functionality
10. Use utility functions from `reactor/utilities` rather than duplicating functionality
