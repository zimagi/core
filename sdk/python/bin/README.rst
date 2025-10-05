=====================================================
README for Directory: sdk/python/bin
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the entry point for the Zimagi Python client, providing a command-line interface (CLI) for interacting with Zimagi services. It encapsulates the logic for setting up the client environment, handling configuration, and executing commands within a Docker container.

**Key Functionality**
   *   Initializes the Zimagi client environment and configuration.
   *   Provides a command-line interface for various Zimagi operations.
   *   Manages Docker container execution for client commands.
   *   Handles user authentication and API token management.

Dependencies
-------------------------

*   **docker**: The `docker` command-line tool and Docker daemon are essential for running Zimagi client commands within containers.
*   **bash**: The `zimagi` script is a bash script, relying on standard bash functionalities.

File Structure and Descriptions
-------------------------------

**sdk/python/bin/README.rst**
     **Role:** This file provides comprehensive documentation for the `sdk/python/bin` directory, detailing its purpose, contents, dependencies, and operational flow.
     **Detailed Description:** This README is crucial for both human developers and AI models to understand the architecture and functionality of the Zimagi Python client's entry point. It outlines the high-level overview, platform requirements, detailed descriptions of each file, and the execution flow, ensuring clarity and ease of maintenance.

**sdk/python/bin/zimagi**
     **Role:** This is the primary executable script for the Zimagi Python client, acting as the command-line interface.
     **Detailed Description:** The `zimagi` script is responsible for configuring the client environment, including API host, port, user credentials, and API tokens. It dynamically generates a client configuration file if one doesn't exist, prompting the user for necessary information. It then constructs and executes a `docker run` command to launch the Zimagi CLI within a Docker container, passing all relevant environment variables and command-line arguments. This script ensures that all Zimagi client interactions are containerized and consistent. It relies on environment variables for configuration and interacts with the Docker daemon to manage container lifecycles.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `zimagi` script is executed from the command line with specific arguments.
   2.  It first checks for the existence of a client configuration file (`client.<profile>.sh`) in the user's Zimagi client home directory.
   3.  If the configuration file is not found, the script interactively prompts the user for necessary API connection details (host, port, user, token, key) and generates the configuration file.
   4.  The script then sources the configuration file to load environment variables.
   5.  It constructs a `docker run` command, including volumes for client home and other necessary directories, network settings, user/group IDs, and all relevant `ZIMAGI_` prefixed environment variables.
   6.  Finally, it executes the `docker run` command, launching the Zimagi CLI within a Docker container to process the user's command.

**External Interfaces**
   *   **Docker Daemon:** The `zimagi` script heavily relies on the local Docker daemon to build and run the Zimagi client Docker image and execute commands within containers.
   *   **Zimagi Command API:** The client, once running in its Docker container, communicates with the Zimagi Command API (specified by `ZIMAGI_COMMAND_HOST` and `ZIMAGI_COMMAND_PORT`) to perform operations.
   *   **Filesystem:** The script interacts with the local filesystem to store and retrieve client configuration files in `ZIMAGI_CLIENT_HOME`.
