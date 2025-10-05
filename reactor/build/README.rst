=====================================================
README for Directory: reactor/build
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains shell scripts responsible for configuring and initiating the Docker build process for various Zimagi application components, specifically focusing on client and server images for different runtime environments. It centralizes the logic for setting up build arguments and environment variables required by Docker.

**Key Functionality**
   Manages the Docker build arguments for client and server images. Sets environment variables crucial for the Docker build process. Differentiates build configurations for standard and NVIDIA-accelerated server environments. Provides a shared utility script for common build functions.

Dependencies
-------------------------

The scripts in this directory primarily rely on standard Unix-like shell environments (Bash) and the Docker command-line interface. They interact with the `id` command for user ID retrieval and `cat` for file content.

File Structure and Descriptions
-------------------------------

**reactor/build/server.sh**
     **Role:** This script is responsible for setting up the Docker build arguments for the standard Zimagi server image.
     **Detailed Description:** It sources the `shared.sh` script to access common functions and then explicitly sets `ZIMAGI_DOCKER_RUNTIME` to "standard". Finally, it calls the `server_build_args` function, which populates the `DOCKER_BUILD_VARS` array with environment-specific and user-specific build arguments for the server. This script is the entry point for building the standard server image.

**reactor/build/shared.sh**
     **Role:** This script contains common shell functions and variables shared across other build scripts in the `reactor/build` directory.
     **Detailed Description:** It defines functions like `server_build_args` and `client_build_args` which are used to prepare the `DOCKER_BUILD_VARS` array with necessary build arguments such as `ZIMAGI_PARENT_IMAGE`, `ZIMAGI_ENVIRONMENT`, and `ZIMAGI_USER_UID`. This script ensures consistency and reusability of build logic across different component builds.

**reactor/build/README.rst**
     **Role:** This file provides documentation for the `reactor/build` directory, explaining its purpose, contents, and execution flow.
     **Detailed Description:** As a reStructuredText file, it serves as a comprehensive guide for developers and AI models to understand the build process and the roles of individual scripts within this directory. It outlines the directory's overview, dependencies, file structure, and execution flow.

**reactor/build/client.sh**
     **Role:** This script is dedicated to configuring the Docker build arguments for the Zimagi client image.
     **Detailed Description:** Similar to `server.sh`, it sources `shared.sh` and sets `ZIMAGI_DOCKER_RUNTIME` to "standard". It then invokes the `client_build_args` function from `shared.sh` to prepare the `DOCKER_BUILD_VARS` array with the appropriate arguments for building the client-side Docker image.

**reactor/build/server.nvidia.sh**
     **Role:** This script sets up the Docker build arguments specifically for the NVIDIA-accelerated Zimagi server image.
     **Detailed Description:** This script is a specialized version of `server.sh`. It also sources `shared.sh` but sets `ZIMAGI_DOCKER_RUNTIME` to "nvidia". It then calls `server_build_args` to configure the build variables, ensuring that the resulting server image is optimized for NVIDIA GPU environments.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The typical execution flow begins with either `client.sh`, `server.sh`, or `server.nvidia.sh`. These scripts first establish the current script's directory and then source `shared.sh` to gain access to common build functions. Depending on the specific script, `ZIMAGI_DOCKER_RUNTIME` is set to either "standard" or "nvidia". Finally, either `client_build_args` or `server_build_args` (both defined in `shared.sh`) is called to populate the `DOCKER_BUILD_VARS` array, which is then used by the Docker build command (not explicitly shown in these scripts but implied by their purpose) to construct the respective Docker images.

**External Interfaces**
   The scripts in this directory primarily interface with the Docker daemon and the underlying operating system's shell environment. They prepare environment variables and build arguments that are consumed by Docker commands (e.g., `docker build`) to create container images. They also interact with system commands like `id` to retrieve user information for setting appropriate permissions within the Docker containers.
