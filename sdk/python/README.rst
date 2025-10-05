=====================================================
README for Directory: sdk/python
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the foundational Python SDK for interacting with the Zimagi platform. It provides core client functionalities, communication protocols, data handling, and utility functions necessary for building applications and command-line tools that integrate with Zimagi services. It abstracts away the complexities of API communication, encryption, and data parsing, offering a streamlined interface for developers.

**Key Functionality**
   *   Provides base classes for API clients, handling common concerns like authentication, encryption, and request/response processing.
   *   Manages secure communication with Zimagi services through encryption and custom transport layers.
   *   Offers robust data serialization and deserialization mechanisms for various media types, including JSON and OpenAPI specifications.
   *   Includes utility functions for data manipulation, error handling, and parallel processing.
   *   Defines core exceptions and configuration settings for the Zimagi Python SDK.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for Python 3.x environments, typically running on Linux-based systems, and interacts with Docker containers for Zimagi services.

**Local Dependencies**
   *   ``requests``: Used for making HTTP requests to Zimagi APIs.
   *   ``pycryptodome``: Provides cryptographic primitives for encryption and decryption.
   *   ``terminaltables``: Used for formatting tabular data in terminal output.
   *   ``validators``: Used for URL validation.
   *   ``pandas``: Utilized in the data codecs for handling tabular data (e.g., CSV).
   *   ``oyaml``: Used for YAML serialization/deserialization.
   *   ``magic``: Used for determining file mimetypes.
   *   ``urllib3``: Used for managing HTTP connection pools and disabling warnings.

File Structure and Descriptions
-------------------------------

**sdk/python/bin**
     **Role:** Contains executable scripts for the Zimagi Python client.
     **Detailed Description:** This subdirectory holds the primary executable script, `zimagi`, which acts as the command-line interface for the Zimagi Python client. It handles environment setup, configuration loading, and the execution of Zimagi commands within Docker containers, abstracting away the containerization details from the end-user.

**sdk/python/zimagi**
     **Role:** Contains the core Zimagi Python SDK modules.
     **Detailed Description:** This subdirectory is the heart of the Zimagi Python SDK, encompassing various modules for client interaction, data handling, command processing, authentication, encryption, and utility functions. It provides the programmatic interface for developers to integrate with Zimagi services.

**sdk/python/setup.py**
     **Role:** Defines the package metadata and build instructions for the Zimagi Python SDK.
     **Detailed Description:** This file is the standard Python `setuptools` configuration file. It specifies the package name, version, author, description, license, and dependencies (from `requirements.txt`). It also defines how the package should be built and where its scripts (like the `zimagi` CLI) are located, enabling proper installation and distribution of the SDK.

**sdk/python/requirements.txt**
     **Role:** Lists the external Python package dependencies for the Zimagi Python SDK.
     **Detailed Description:** This file explicitly enumerates all third-party Python libraries and their version constraints that are required for the Zimagi Python SDK to function correctly. It is used by package managers like `pip` to install the necessary dependencies during setup.

**sdk/python/README.rst**
     **Role:** This file is the README document for the `sdk/python` directory.
     **Detailed Description:** This document provides an overview of the `sdk/python` directory, detailing its purpose, key functionalities, platform dependencies, file structure with descriptions of individual files and subdirectories, and an explanation of the execution flow and external interfaces.

**sdk/python/README.md**
     **Role:** A placeholder or alternative README file for the `sdk/python` directory.
     **Detailed Description:** This file is currently empty and serves as a placeholder. It could potentially be used for a Markdown-formatted README in the future, offering an alternative to the reStructuredText version for platforms that prefer Markdown rendering.

**sdk/python/deploy.sh**
     **Role:** Provides a shell script for deploying the Zimagi Python SDK to PyPI.
     **Detailed Description:** This shell script automates the process of building and uploading the Zimagi Python SDK package to the Python Package Index (PyPI). It handles setting up PyPI credentials, installing build tools, creating source and wheel distributions, and finally uploading them using `twine`.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `deploy.sh` script is executed to build and publish the SDK.
   2.  During deployment, `setup.py` is used to define the package structure and dependencies listed in `requirements.txt`.
   3.  Once installed, the `zimagi` executable script (located in `sdk/python/bin`) serves as the primary entry point for command-line interactions.
   4.  The `zimagi` script configures the client environment and then invokes the core Python SDK modules within `sdk/python/zimagi` to execute commands.
   5.  Within `sdk/python/zimagi`, various client classes (e.g., `CommandClient`, `DataClient`) handle API communication, authentication, encryption, and data processing.

**External Interfaces**
   *   **PyPI (Python Package Index):** The `deploy.sh` script interacts with PyPI to publish the SDK.
   *   **Docker Daemon:** The `zimagi` CLI script (in `sdk/python/bin`) heavily relies on the local Docker daemon to build and run the Zimagi client Docker image and execute commands within containers.
   *   **Zimagi Command API:** The `sdk/python/zimagi` modules, particularly the `CommandClient`, communicate with the Zimagi Command API over HTTP/HTTPS to execute commands and receive streamed responses.
   *   **Zimagi Data API:** The `sdk/python/zimagi` modules, particularly the `DataClient`, communicate with the Zimagi Data API over HTTP/HTTPS to perform data operations.
   *   **Operating System:** Interacts with the operating system for file system operations (e.g., caching, configuration files) and environment variables.
   *   **Network Infrastructure:** Relies on underlying network infrastructure to establish connections and transmit data to Zimagi services.
