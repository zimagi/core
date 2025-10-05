=====================================================
README for Directory: reactor/utilities
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains essential shell scripts that manage and configure the environment for Zimagi Docker containers, ensuring proper setup for various runtime environments and security settings. It centralizes environment variable generation and Docker-related configurations.

**Key Functionality**
   1.  Manages Docker runtime environment variables, including image names and parent images.
   2.  Configures security-related environment variables like API keys and tokens.
   3.  Provides functions for debugging environment variable settings.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for Unix-like operating systems (Linux, macOS) that support Bash shell scripting. It specifically targets environments where Docker and Docker Compose are installed and actively used for container orchestration.

**Local Dependencies**
   This directory primarily relies on standard Unix shell utilities (e.g., `cat`, `grep`, `env`, `cut`, `awk`, `hexdump`, `id`, `getent`, `read`, `source`, `export`, `unset`, `rm`, `cp`, `test`, `dirname`, `pwd`, `re.search`, `subprocess.call`) and the `docker` command-line interface for interacting with Docker. It also depends on environment variables set by the broader Zimagi project, such as `DEFAULT_ZIMAGI_BASE_IMAGE`, `DEFAULT_ZIMAGI_DOCKER_RUNTIME`, `DEFAULT_ZIMAGI_DOCKER_TAG`, `DEFAULT_ZIMAGI_SECRET_KEY`, `DEFAULT_ZIMAGI_ADMIN_API_KEY`, and `DEFAULT_ZIMAGI_ADMIN_API_TOKEN`.


File Structure and Descriptions
-------------------------------

**reactor/utilities/README.rst**
     **Role:** This file provides comprehensive documentation for the `reactor/utilities` directory.
     **Detailed Description:** This README file serves as a guide for human developers and AI models, explaining the purpose, key functionalities, dependencies, file structure, and execution flow of the scripts within the `reactor/utilities` directory. It details the role of `env.sh` and its functions in setting up the Docker and security environments for Zimagi applications.

**reactor/utilities/env.sh**
     **Role:** This script defines and exports critical environment variables related to Docker configuration and security for the Zimagi application.
     **Detailed Description:** It contains shell functions `zimagi_docker_environment`, `zimagi_security_environment`, and `zimagi_environment`. The `zimagi_docker_environment` function determines the appropriate Docker base image and tag based on the specified runtime (standard or NVIDIA) and sets related environment variables like `ZIMAGI_DOCKER_GROUP`, `ZIMAGI_DOCKER_RUNTIME`, `ZIMAGI_DOCKER_TAG`, `ZIMAGI_PARENT_IMAGE`, `ZIMAGI_BASE_IMAGE`, and `ZIMAGI_DEFAULT_RUNTIME_IMAGE`. The `zimagi_security_environment` function sets up API keys and tokens by exporting `ZIMAGI_SECRET_KEY`, `ZIMAGI_ADMIN_API_KEY`, and `ZIMAGI_ADMIN_API_TOKEN`. The `zimagi_environment` function acts as an orchestrator, calling the Docker and security environment setup functions. It includes debugging output for transparency using the `debug` function.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The `env.sh` script is typically sourced by other shell scripts within the Zimagi project, such as `start` or `zimagi`, to establish the necessary environment variables before executing Docker commands or other application logic. The `zimagi_environment` function serves as the primary entry point within this script, which then sequentially calls `zimagi_docker_environment` and `zimagi_security_environment`. These functions set various `ZIMAGI_` prefixed environment variables that are crucial for the application's operation.

**External Interfaces**
   This script interacts with the Docker daemon indirectly by setting environment variables that influence how Docker images are built and containers are run. It also relies on system utilities like `env` for debugging output. The environment variables it sets are consumed by Docker Compose files (e.g., `compose.standard.local.yaml`, `compose.nvidia.local.yaml`) and other Zimagi application components to configure their runtime behavior and security. Specifically, variables like `ZIMAGI_DOCKER_RUNTIME`, `ZIMAGI_DOCKER_TAG`, `ZIMAGI_PARENT_IMAGE`, `ZIMAGI_BASE_IMAGE`, `ZIMAGI_DEFAULT_RUNTIME_IMAGE`, `ZIMAGI_SECRET_KEY`, `ZIMAGI_ADMIN_API_KEY`, and `ZIMAGI_ADMIN_API_TOKEN` are made available globally for other scripts and Docker configurations to utilize.
