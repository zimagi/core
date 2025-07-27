# Zimagi Reactor Build Directory

## Overview

The `reactor/build` directory contains Docker build argument configuration files that define environment variables and build parameters for Zimagi's containerized components. This directory plays a critical role in the Reactor Kubernetes development platform by providing standardized build configurations that ensure consistent container creation across different deployment environments.

This directory serves as the configuration layer that connects the Reactor development platform with Docker's containerization system. It enables developers to build Zimagi server and client images with appropriate environment settings, supporting both standard and GPU-accelerated deployments.

The build configurations are primarily used by:

- **Developers** building Docker images for local development and testing
- **DevOps engineers** managing containerized deployments in Kubernetes environments
- **CI/CD systems** that require standardized build parameters for automated image creation
- **AI models** understanding development platform integration and generating build configurations

## Directory Contents

### Files

| File             | Purpose                                                                                                          | Format |
| ---------------- | ---------------------------------------------------------------------------------------------------------------- | ------ |
| client.sh        | Client Docker image build configuration that sets up environment variables for building Zimagi CLI client images | Bash   |
| server.sh        | Server Docker image build configuration that defines build arguments for standard Zimagi server images           | Bash   |
| server.nvidia.sh | NVIDIA-enabled server Docker image build configuration for GPU-accelerated server deployments                    | Bash   |
| shared.sh        | Shared build functions and variables that provide common environment setup for all build configurations          | Bash   |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `reactor` directory which provides Kubernetes development and management platform integration (see reactor/README.md)
- **Docker Integration**: Works with `docker` directory for containerization of CLI tools and applications (see docker/README.md)
- **Environment Configuration**: Uses and extends configurations from `env` directory for build processes (see env/README.md)
- **Reactor CLI Integration**: Connects to the custom `zimagi` executable in the reactor directory for Kubernetes development

The `reactor/build` directory serves as the build configuration foundation that enables consistent Docker image creation for the Reactor platform, connecting to Docker build systems in `docker` and environment configurations in `env`.

## Key Concepts, Conventions, and Patterns

### Build Configuration Architecture

The build configuration files implement a modular approach to Docker image creation:

- **Environment-Based Configuration**: Build arguments are defined through environment variables that control image creation
- **Runtime-Specific Builds**: Different configurations support standard and NVIDIA GPU-accelerated deployments
- **Shared Functionality**: Common build logic is abstracted into shared scripts to reduce duplication
- **Standardized Parameters**: All configurations follow consistent patterns for environment variable definitions

### Naming Conventions

- Bash scripts use descriptive names with clear functional purposes (e.g., `client.sh`, `server.nvidia.sh`)
- Configuration files are named by their target component with optional runtime modifiers
- Shared utility files use `shared` prefix to indicate common functionality
- File extensions follow Unix conventions with no extensions for executable scripts

### File Organization

Files are organized by build target and runtime requirements:

- Client build configuration in `client.sh`
- Standard server build configuration in `server.sh`
- NVIDIA-enabled server build configuration in `server.nvidia.sh`
- Shared build utilities in `shared.sh`

### Domain-Specific Patterns

- Build scripts use standardized environment variable patterns for Docker integration
- Runtime detection is handled through explicit script naming (standard vs nvidia)
- Environment variable inheritance follows consistent patterns through shared.sh
- Build argument arrays are used for consistent Docker command construction

## Developer Notes and Usage Tips

### Integration Requirements

The build configuration files require:

- Docker for containerized execution of build processes
- Proper network connectivity to Docker Hub for base image downloads
- Environment variables for configuration (automatically handled by initialization scripts)
- Access to project directories for volume mounting in Docker containers

### Usage Patterns

- Build configurations are sourced by Docker build processes in the reactor platform
- Environment variables are automatically exported by build scripts
- Shared functions provide common setup for all build configurations
- Runtime-specific scripts set appropriate environment flags for specialized deployments

### Dependencies

- Docker for containerized execution
- Bash shell environment
- Network connectivity to Docker Hub
- Access to project directories for volume mounting

### AI Development Guidance

When generating or modifying build configuration files in this directory:

1. Maintain consistency with existing script architecture patterns
2. Follow Unix conventions for executable script naming and structure
3. Ensure proper integration with Docker containerization and Kubernetes deployment
4. Implement environment variable handling through established patterns
5. Follow the pattern of providing both local development and production execution modes
6. Maintain consistency with error handling and exit code patterns
7. Ensure scripts properly integrate with the zimagi CLI and reactor platform
8. Respect the separation between different build target configurations
9. Follow the client-driven approach where scripts provide interfaces to development platform functionality
10. Use shared functions from shared.sh rather than duplicating functionality
