=====================================================
README for Directory: docker
=====================================================

Directory Overview
------------------

**Purpose**
   This `docker` directory is central to the project's containerization strategy, providing all necessary Dockerfiles, build scripts, and deployment manifests to create and manage Docker images for both the client-side CLI and the server-side application components. It encapsulates the environment setup and packaging logic for consistent deployment across various environments.

**Key Functionality**
   *   Defines Docker images for the client-side CLI and the server application.
   *   Manages the installation of core and server-specific system packages within Docker images.
   *   Provides scripts for building, deploying, and creating multi-architecture manifests for Docker images.
   *   Configures the entry points and user environments for Docker containers.

Dependencies
-------------------------

The files in this directory heavily rely on Docker and Docker Compose for image building, container orchestration, and deployment. Shell scripting (Bash) is used for automating build and deployment processes. Specific system packages and Python libraries are managed via `apt-get` and `pip3` within the Dockerfiles.

File Structure and Descriptions
-------------------------------

**docker/packages.server.txt**
     **Role:** Lists core system packages required for the server Docker image.
     **Detailed Description:** This file contains a newline-separated list of `apt-get` packages that are installed during the Docker image build process for the server. These packages include utilities like `git`, `openssh-client`, database support libraries (`libpq-dev`), and various multimedia and image processing dependencies (`ffmpeg`, `libsm6`). It ensures that the server environment has all necessary external tools and libraries.

**docker/build_client_image.sh**
     **Role:** Script to build the Zimagi client Docker image.
     **Detailed Description:** This Bash script automates the Docker image build process for the Zimagi client. It reads the application version, constructs the image tag, and executes the `docker build` command using `Dockerfile.cli`. This script is typically invoked during local development or CI/CD pipelines to create a runnable client container.

**docker/deploy_cli_manifest.sh**
     **Role:** Script to create and push a multi-architecture Docker manifest for the CLI image.
     **Detailed Description:** This script is responsible for creating a Docker manifest list for the `zimagi/cli` image, combining architecture-specific images (amd64 and arm64) into a single tag. It requires Docker Hub credentials and ensures that the CLI image is discoverable and usable across different CPU architectures.

**docker/cli_entrypoint.sh**
     **Role:** Entrypoint script for the Zimagi client Docker container.
     **Detailed Description:** This simple Bash script sets up the terminal color environment and then executes the `zimagi-cli` command with any provided arguments. It serves as the initial command run when a `zimagi/cli` container starts, ensuring the CLI application is properly invoked.

**docker/deploy_server_image.sh**
     **Role:** Script to build and push a specific architecture Docker image for the server.
     **Detailed Description:** This Bash script handles the building and pushing of a Docker image for the Zimagi server, tailored for a specific architecture (e.g., `amd64` or `arm64`). It logs into Docker Hub, builds the image using `Dockerfile.server` with appropriate platform arguments, and then pushes the resulting image to the registry.

**docker/Dockerfile.cli**
     **Role:** Dockerfile for building the Zimagi client image.
     **Detailed Description:** This Dockerfile defines the steps to create the `zimagi/cli` Docker image. It starts from a base Ubuntu image, installs core system packages (from `packages.core.txt`), Node.js, and Python dependencies. It sets up the virtual environment, copies the Python SDK and application code, and defines the entrypoint for the client application.

**docker/Dockerfile.server**
     **Role:** Dockerfile for building the Zimagi server image.
     **Detailed Description:** This Dockerfile outlines the construction of the `zimagi/server` Docker image. It builds upon a base Ubuntu image, installs core system packages (from `packages.core.txt`) and server-specific packages (from `packages.server.txt`), including `libgit2` and `geckodriver`. It configures the Python environment, copies the application and SDK, and sets up various directories and entrypoints for the server components.

**docker/deploy_server_manifest.sh**
     **Role:** Script to create and push a multi-architecture Docker manifest for the server image.
     **Detailed Description:** Similar to `deploy_cli_manifest.sh`, this script creates and pushes a Docker manifest list for the `zimagi/server` image. It supports both standard (amd64 and arm64) and NVIDIA-specific (amd64 only) server runtimes, ensuring the correct architecture images are grouped under a single tag for deployment.

**docker/deploy_cli_image.sh**
     **Role:** Script to build and push a specific architecture Docker image for the CLI.
     **Detailed Description:** This script is responsible for building and pushing a Docker image for the Zimagi CLI for a particular architecture. It logs into Docker Hub, builds the image using `Dockerfile.cli` with platform-specific arguments, and then pushes the image to the Docker registry.

**docker/packages.core.txt**
     **Role:** Lists fundamental system packages required for both client and server Docker images.
     **Detailed Description:** This file specifies a common set of `apt-get` packages that are installed in both `Dockerfile.cli` and `Dockerfile.server`. These include essential utilities like `curl`, `wget`, `build-essential` for compilation, `python3-venv`, and `cargo` for Rust-based dependencies, forming the foundational environment for both client and server containers.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The typical execution flow for building and deploying images starts with the `build_client_image.sh` or `deploy_server_image.sh` scripts. These scripts invoke `docker build`, which in turn uses `Dockerfile.cli` or `Dockerfile.server` to construct the images based on the package lists (`packages.core.txt`, `packages.server.txt`). Once architecture-specific images are built and pushed (via `deploy_cli_image.sh` or `deploy_server_image.sh`), `deploy_cli_manifest.sh` or `deploy_server_manifest.sh` are used to create multi-architecture manifests, making the images accessible under a single tag. The `cli_entrypoint.sh` script defines how the client container starts and executes the Zimagi CLI.

**External Interfaces**
   This `docker` directory primarily interfaces with the Docker daemon for building and managing images and containers. It also interacts with Docker Hub (or any configured Docker registry) for pushing and pulling images and manifests. The build processes fetch packages from Ubuntu's `apt` repositories and other external sources like GitHub (for `libgit2` and `geckodriver`). The resulting Docker images are then consumed by Docker Compose files (located outside this directory, e.g., `compose.standard.local.yaml`) to orchestrate the application's services.
