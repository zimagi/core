GPU Management
==============

Zimagi provides capabilities for managing and utilizing NVIDIA GPU resources, which is crucial for accelerating AI and machine learning workloads.

Overview
--------
The platform allows for querying GPU device information and configuring services to leverage NVIDIA GPUs in supported environments.

Key GPU Management Features
--------------------------
*   **GPU Information Display**: Query and display detailed information about available NVIDIA GPUs.
*   **NVIDIA Runtime Support**: Configure Docker environments to use NVIDIA Container Toolkit for GPU access.
*   **AI Workload Acceleration**: Leverage GPUs for faster execution of language models, encoders, and other compute-intensive tasks.

GPU Command (`app/commands/gpu.py`)
-----------------------------------
*   **`app/commands/gpu.py`**: Defines the `gpu` command for displaying NVIDIA GPU information.

Utility Functions (`app/utility/nvidia.py`)
-------------------------------------------
*   **`app/utility/nvidia.py`**: Provides an interface for interacting with NVIDIA GPU devices using `pynvml`.

Docker Configuration (`docker/`)
-------------------------------
*   **`docker/Dockerfile.server`**: Dockerfile for building the Zimagi server image, including NVIDIA-specific dependencies.
*   **`docker/deploy_server_image.sh`**: Script to build and push NVIDIA-enabled Docker images.
*   **`docker/deploy_server_manifest.sh`**: Script to create multi-architecture Docker manifests, including NVIDIA-specific runtimes.

Environment Variables (`env/`)
------------------------------
*   **`ZIMAGI_DOCKER_RUNTIME`**: Set to `nvidia` to enable GPU support in Docker Compose.

Using GPU Management
--------------------

1.  **Displaying GPU Information**: Use the `zimagi gpu` command.

    .. code-block:: bash

        zimagi gpu

    This command will output details about your NVIDIA GPUs, such as memory usage, driver version, and device ID.

2.  **Starting Zimagi with NVIDIA Support**: When starting your Zimagi environment, specify the `nvidia` type.

    .. code-block:: bash

        source start nvidia local default

    This ensures that Docker Compose uses the NVIDIA runtime for services that require GPU access.

3.  **Configuring AI Agents for GPU**: AI agents (e.g., `language_model`, `encoder`) can be configured to use specific GPU devices if available. This is typically done through their plugin options or environment variables.

    Example: Configuring an encoder plugin to use a specific device (conceptual, depends on plugin implementation):

    .. code-block:: yaml

        encoder:
            transformer:
                options:
                    device: "cuda:0"

Leveraging GPU resources is essential for optimizing the performance of demanding AI and machine learning tasks within Zimagi.
