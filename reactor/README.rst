=====================================================
README for Directory: reactor
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the core operational hub for the Zimagi application's reactor environment. It centralizes scripts and configurations essential for building, initializing, managing, and executing various components of the Zimagi system, including Docker images, services, and command-line operations.

**Key Functionality**
   1.  **Environment Management:** Initializes and configures the Zimagi runtime environment, including Docker-related settings and security variables.
   2.  **Docker Image Building:** Provides scripts for building client and server Docker images for different runtime environments (standard, NVIDIA).
   3.  **Service Orchestration:** Manages the lifecycle of Zimagi services within Docker containers, including starting, stopping, and logging.
   4.  **Command Execution:** Acts as the entry point for executing Zimagi commands within a Dockerized context.
   5.  **Dependency Management:** Specifies Python development dependencies for the project.
   6.  **Lifecycle Hooks:** Defines custom actions to be executed at various points in the application's lifecycle.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for Unix-like operating systems (Linux, macOS) that support Bash shell scripting. It specifically targets environments where Docker and Docker Compose are installed and actively used for container orchestration. The Python dependencies are managed via `pip`.

**Local Dependencies**
   This directory heavily relies on standard Unix shell utilities (e.g., `cat`, `grep`, `env`, `cut`, `awk`, `hexdump`, `id`, `getent`, `read`, `source`, `export`, `unset`, `rm`, `cp`, `test`, `dirname`, `pwd`, `re.search`, `subprocess.call`) and the `docker` command-line interface for interacting with Docker. It also depends on environment variables set by the broader Zimagi project, such as `DEFAULT_ZIMAGI_BASE_IMAGE`, `DEFAULT_ZIMAGI_DOCKER_RUNTIME`, `DEFAULT_ZIMAGI_DOCKER_TAG`, `DEFAULT_ZIMAGI_SECRET_KEY`, `DEFAULT_ZIMAGI_ADMIN_API_KEY`, and `DEFAULT_ZIMAGI_ADMIN_API_TOKEN`. Python dependencies are listed in `requirements.txt`.


File Structure and Descriptions
-------------------------------

**reactor/build**
     **Role:** This subdirectory contains shell scripts responsible for configuring and initiating the Docker build process for various Zimagi application components.
     **Detailed Description:** It centralizes the logic for setting up build arguments and environment variables required by Docker. It manages the Docker build arguments for client and server images, and differentiates build configurations for standard and NVIDIA-accelerated server environments. It also provides a shared utility script for common build functions.

**reactor/utilities**
     **Role:** This subdirectory contains essential shell scripts that manage and configure the environment for Zimagi Docker containers.
     **Detailed Description:** It ensures proper setup for various runtime environments and security settings. It centralizes environment variable generation and Docker-related configurations, managing Docker runtime environment variables (image names, parent images) and configuring security-related environment variables (API keys, tokens).

**reactor/commands**
     **Role:** This subdirectory contains shell scripts that define and execute Zimagi operations within a reactor environment context.
     **Detailed Description:** These scripts serve as entry points for various Zimagi commands, facilitating interaction with the Zimagi application and its underlying Docker infrastructure. They are responsible for executing Zimagi commands within a Docker container and setting up the necessary environment variables and Docker arguments for command execution.

**reactor/requirements.txt**
     **Role:** This file lists the Python development dependencies required for the Zimagi project.
     **Detailed Description:** It specifies the exact versions of libraries and packages necessary for code quality tools and other development-related utilities. This ensures a consistent development environment across different setups.

**reactor/hooks.sh**
     **Role:** This script defines custom shell functions that act as lifecycle hooks for the Zimagi project.
     **Detailed Description:** These functions are designed to be executed at specific points in the application's lifecycle, such as when modifications are detected or during updates. They provide a mechanism to extend or customize the behavior of the Zimagi system without altering core scripts.

**reactor/initialize.sh**
     **Role:** This script initializes critical project variables and sets up the foundational environment for the Zimagi application.
     **Detailed Description:** It defines magic variables for key directories within the project, sets default environment configurations, and establishes base image information for Docker builds. It also ensures the creation of necessary data and library directories, providing a consistent starting point for all Zimagi operations.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The typical execution flow often begins with `initialize.sh`, which sets up the foundational environment variables and directory structures. Subsequently, scripts within `reactor/utilities` (specifically `env.sh`) are sourced to establish Docker and security-related environment variables. When building Docker images, scripts in `reactor/build` are invoked, which in turn rely on the environment variables set by `utilities/env.sh`. For executing Zimagi commands, `reactor/commands/zimagi.sh` acts as the primary entry point, leveraging the configured environment and Docker to run operations. `reactor/hooks.sh` functions are called at specific points by other scripts to perform custom actions.

**External Interfaces**
   The scripts in this directory primarily interface with the Docker daemon for container management, image building, and service orchestration. They also interact with the host system's environment variables and file system. The environment variables set by these scripts are consumed by Docker Compose files (e.g., `compose.standard.local.yaml`, `compose.nvidia.local.yaml`) and other Zimagi application components to configure their runtime behavior and security. Python dependencies are managed externally via `pip` based on `requirements.txt`.
