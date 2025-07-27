# Zimagi Reactor Directory

## Overview

The `reactor` directory contains files that integrate with the Reactor Kubernetes development and management platform. This directory provides essential infrastructure for Docker build processes, utility libraries, and a customized `zimagi` executable that integrates with the reactor CLI.

This directory serves as a bridge between local development environments and Kubernetes-based deployments, enabling developers to build, test, and manage Zimagi applications within containerized environments. It plays a critical architectural role by providing:

- Build configurations for Docker images used in development and deployment
- Utility scripts for environment setup and management
- Command-line integration with the reactor platform for streamlined development workflows

The reactor directory is primarily used by:

- **Developers** working on Zimagi applications in Kubernetes environments
- **DevOps engineers** managing containerized deployments
- **AI models** understanding development platform integration and generating build configurations

## Directory Contents

### Files

| File             | Purpose                                                                                   | Format |
| ---------------- | ----------------------------------------------------------------------------------------- | ------ |
| zimagi           | Custom zimagi executable that integrates with the reactor CLI for Kubernetes development  | Bash   |
| initialize.sh    | Project initialization script that sets up environment variables and directory structures | Bash   |
| hooks.sh         | Project hooks for managing module updates and CLI initialization                          | Bash   |
| requirements.txt | Development dependencies for code quality and linting tools                               | Text   |

### Subdirectories

| Directory | Purpose                                        | Contents                |
| --------- | ---------------------------------------------- | ----------------------- |
| build     | Docker build argument files and configurations | See build/README.md     |
| commands  | Reactor command implementations                | See commands/README.md  |
| utilities | Utility libraries for environment management   | See utilities/README.md |

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the root project directory which contains top-level project files
- **Docker Integration**: Works with `docker` directory for containerization of CLI tools and applications
- **Server Integration**: Connects to `app` directory which contains the server application implementation
- **Package Integration**: Integrates with `package` directory for CLI tool functionality
- **Environment Configuration**: Uses configurations from `env` directory for build processes

The `reactor` directory serves as the development platform integration layer that enables Kubernetes-based development workflows, connecting to the Docker build system in `docker` and the server application in `app`.

## Key Concepts, Conventions, and Patterns

### Architectural Patterns

The reactor directory follows a modular architecture based on platform integration principles:

- **Build Configuration**: Docker build arguments and configurations organized by component type
- **Command Integration**: CLI command implementations that extend the zimagi executable
- **Environment Management**: Utility functions for managing development environments
- **Platform Integration**: Scripts that connect local development with Kubernetes deployments

### Naming Conventions

- Bash scripts use descriptive names with underscores (e.g., `server.nvidia.sh`)
- Configuration files use domain-specific naming (e.g., `shared.sh`)
- Command implementations are named after their functional purpose (e.g., `zimagi.sh`)
- Utility functions use verb-noun naming patterns

### File Organization

Files are organized by functional domain following these patterns:

- **Build Configurations**: Located in `build` directory organized by component type
- **Command Implementations**: Located in `commands` directory by command type
- **Utility Functions**: Located in `utilities` directory by functional category
- **Core Infrastructure**: Located at the root level for essential setup and integration

### Domain-Specific Patterns

- Build scripts use standardized environment variable patterns for Docker integration
- Command implementations follow consistent argument passing and execution patterns
- Utility functions implement reusable environment setup and management logic
- Integration with Docker uses standardized volume mounting and network configurations

## Developer Notes and Usage Tips

### Integration Requirements

The reactor directory requires:

- Docker for containerized execution of build processes and CLI commands
- Proper network connectivity to Docker Hub for image downloads
- Environment variables for configuration (automatically handled by initialization scripts)
- Access to project directories for volume mounting in Docker containers

### Usage Patterns

- Developers execute the `zimagi` script directly from the command line for reactor integration
- Build configurations are used automatically by Docker build processes
- Environment utilities handle setup and configuration management
- Command implementations extend the base zimagi functionality for Kubernetes workflows

### Dependencies

- Docker for containerized execution
- Bash shell environment
- Network connectivity to Docker Hub
- Access to project directories for volume mounting

### AI Development Guidance

When generating or modifying files in this directory:

1. Maintain consistency with existing script architecture patterns
2. Follow Unix conventions for executable script naming and structure
3. Ensure proper integration with Docker containerization and Kubernetes deployment
4. Implement environment variable handling through established patterns
5. Follow the pattern of providing both local development and production execution modes
6. Maintain consistency with error handling and exit code patterns
7. Ensure scripts properly integrate with the zimagi CLI and reactor platform
8. Respect the separation between build configurations, command implementations, and utility functions
9. Follow the client-driven approach where scripts provide interfaces to development platform functionality
10. Use utility functions from the reactor platform rather than duplicating functionality
