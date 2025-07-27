# Docker Directory

## Overview

The `docker` directory contains all Docker-related configuration files, build scripts, and deployment utilities for the Zimagi platform. This directory is responsible for defining how the Zimagi server and client applications are containerized, built, and deployed across different environments.

This directory serves both human developers and automated systems (CI/CD pipelines, deployment tools) by providing the necessary components to create consistent, reproducible Docker images for the Zimagi platform services.

## Directory Contents

### Files

| File                      | Purpose                                                                             | Format      |
| ------------------------- | ----------------------------------------------------------------------------------- | ----------- |
| Dockerfile.server         | Defines the Docker image configuration for the Zimagi server application            | Dockerfile  |
| Dockerfile.cli            | Defines the Docker image configuration for the Zimagi command-line interface client | Dockerfile  |
| packages.core.txt         | Lists core system packages required for both server and client images               | Text        |
| packages.server.txt       | Lists additional packages required specifically for the server image                | Text        |
| build_client_image.sh     | Script to build the Zimagi CLI Docker image locally                                 | Bash script |
| deploy_cli_image.sh       | Script to build and deploy the CLI image to a container registry                    | Bash script |
| deploy_cli_manifest.sh    | Script to create and push a multi-architecture manifest for the CLI image           | Bash script |
| deploy_server_image.sh    | Script to build and deploy the server image to a container registry                 | Bash script |
| deploy_server_manifest.sh | Script to create and push a multi-architecture manifest for the server image        | Bash script |
| cli_entrypoint.sh         | Entrypoint script for the CLI Docker container                                      | Bash script |

### Subdirectories

There are no subdirectories in the docker directory.

## Cross-Referencing

The docker directory integrates with several other parts of the Zimagi project:

- **app directory**: Contains the application source code that gets packaged into Docker images
- **package directory**: Contains the Python client library that is included in both server and client images
- **env directory**: Provides environment variable configurations that are used during container runtime
- **reactor directory**: Contains integration tools that work with the Docker build process

## Key Concepts and Conventions

### Image Architecture

Zimagi provides two distinct Docker images:

1. **Server Image** (`zimagi/server`): A complete Zimagi server environment with all services
2. **CLI Image** (`zimagi/cli`): A lightweight client for interacting with Zimagi servers

### Multi-Architecture Support

The deployment scripts support building images for multiple CPU architectures (amd64, arm64) and creating manifest files that allow Docker to automatically select the appropriate image for the target platform.

### Build Process

- Images are built from Ubuntu 24.04 base images
- System dependencies are installed via apt-get using package list files
- Python virtual environments are created for application dependencies
- The Zimagi application is installed as a Python package within containers

### Naming Conventions

- Deployment scripts follow the pattern `deploy_{service}_{type}.sh`
- Package lists are named `packages.{context}.txt`
- Dockerfiles are named `Dockerfile.{context}`

## Developer Notes and Usage Tips

### Building Images

To build images locally:

- Use `build_client_image.sh` for local CLI image development
- Server images require the full build pipeline in deployment scripts

### Environment Variables

Several environment variables affect the build process:

- `ZIMAGI_ENVIRONMENT`: Controls which requirements file is used (prod, dev, etc.)
- `ZIMAGI_USER_UID`: Sets the UID for the zimagi user in containers
- `ZIMAGI_PARENT_IMAGE`: Allows overriding the base image

### Deployment Requirements

Deployment scripts require:

- Docker Hub credentials in `PKG_DOCKER_USER` and `PKG_DOCKER_PASSWORD`
- Proper Docker registry permissions
- The Reactor Kubernetes development platform (automatically cloned if not present)

### AI-Specific Guidance

When generating or modifying Docker-related content:

- Maintain consistency with existing package list formatting (comments with #)
- Follow the established pattern for multi-architecture deployments
- Ensure environment variable handling matches existing implementations
- Preserve the separation between core, client, and server package requirements
