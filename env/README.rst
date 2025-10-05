=====================================================
README for Directory: env
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for all environment-specific configuration files and sensitive credentials required by the Zimagi application. It segregates configuration based on deployment profiles (e.g., default, API, encrypted API) and provides templates for secret management, ensuring that the application can adapt to various operational contexts securely and efficiently.

**Key Functionality**
   Manages application-wide environment variables for different deployment scenarios. Stores default and profile-specific public configuration settings. Provides a template for sensitive information and secrets. Facilitates the secure handling of encrypted configuration data.


Dependencies
-------------------------

The files within this `env` directory are primarily consumed by the Docker Compose configurations (e.g., `compose.standard.local.yaml`, `compose.nvidia.local.yaml`) and the main `zimagi` and `start` shell scripts. These scripts and configurations parse and utilize the environment variables defined in these files to set up the application's runtime environment, including database connections, API ports, and various application settings. There are no direct code dependencies within this directory itself, but its contents are critical inputs for the broader system's operation.


File Structure and Descriptions
-------------------------------

**env/public.api.encrypted**
     **Role:** Stores public environment variables specifically for API deployments, with an emphasis on encrypted values.
     **Detailed Description:** This file contains a collection of environment variables that are publicly accessible but may include values that are expected to be encrypted at rest or handled with specific security considerations. It defines common application settings, database connection parameters, and API-specific configurations that are relevant when the application is deployed in an API-centric profile. It is designed to be sourced by deployment scripts that handle encrypted configurations.

**env/README.rst**
     **Role:** This file provides comprehensive documentation for the `env` directory.
     **Detailed Description:** This README file details the purpose, key functionality, dependencies, file structure, and execution flow of the `env` directory. It serves as a guide for developers and AI models to understand how environment variables and secrets are managed and utilized within the Zimagi project.

**env/public.default**
     **Role:** Defines the default public environment variables for the Zimagi application.
     **Detailed Description:** This file holds the standard, non-sensitive environment variables that apply to most general deployments of the Zimagi application. It includes settings for the application name, database user and name, connection limits, parallel processing flags, debug modes, logging levels, and server worker configurations. This file acts as a baseline for other `public` environment files, providing sensible defaults that can be overridden by more specific profiles.

**env/public.api**
     **Role:** Contains public environment variables tailored for API-specific deployments.
     **Detailed Description:** Similar to `public.default`, this file specifies environment variables relevant to API deployments. It includes settings for common application parameters, database configurations, and API-specific flags such as encryption settings for command and data APIs, page caching, and REST page counts. This file is intended for use in environments where the application primarily functions as an API service, providing a clear separation of concerns for API-related configurations.

**env/secret.example**
     **Role:** Provides an example template for sensitive environment variables and secrets.
     **Detailed Description:** This file serves as a template for creating the actual `env/secret` file, which holds sensitive information like API keys, database passwords, and other confidential credentials. It outlines the structure and types of secrets the application expects, such as `ZIMAGI_SECRET_KEY`, email server credentials, GitHub tokens, and various API keys for AI and search services. This example file is crucial for guiding developers on what sensitive information needs to be configured without exposing actual secrets in version control.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1. The `start` script (located in the project root, outside this directory) is the primary entry point for initializing the Zimagi application environment.
   2. During its execution, `start` determines the `COMPOSE_ENVIRONMENT` (e.g., `local`, `test`) and `COMPOSE_PROFILE` (e.g., `default`, `api`, `api.encrypted`).
   3. Based on the `COMPOSE_PROFILE`, the `start` script sources the corresponding `env/public.<profile>` file (e.g., `env/public.default`, `env/public.api`, `env/public.api.encrypted`) to load public environment variables.
   4. It also sources the `env/secret` file (which is typically a copy of `env/secret.example` populated with actual secrets) to load sensitive environment variables.
   5. These loaded environment variables are then used to populate the `.env` file at the project root, which Docker Compose uses for building images and running services.
   6. The `zimagi` script (also in the project root), used for running commands, also sources these environment files to ensure the correct configuration is available for CLI operations.

**External Interfaces**
   The environment variables defined in this directory directly influence how the Zimagi application interacts with various external systems:
   *   **Databases:** `ZIMAGI_POSTGRES_DB`, `ZIMAGI_POSTGRES_USER`, `ZIMAGI_POSTGRES_PASSWORD`, `ZIMAGI_REDIS_PASSWORD`, `ZIMAGI_QDRANT_ACCESS_KEY` configure connections to PostgreSQL, Redis, and Qdrant databases.
   *   **Email Services:** `ZIMAGI_EMAIL_HOST`, `ZIMAGI_EMAIL_HOST_USER`, `ZIMAGI_EMAIL_HOST_PASSWORD` facilitate communication with external SMTP servers for email notifications.
   *   **Version Control/APIs:** `ZIMAGI_GITHUB_USER`, `ZIMAGI_GITHUB_TOKEN` enable interaction with GitHub APIs.
   *   **AI/ML Services:** `ZIMAGI_HUGGINGFACE_TOKEN`, `OPENROUTER_API_KEY`, `DEEPINFRA_API_KEY` are used for integrating with various AI platforms.
   *   **Search Engines:** `ZIMAGI_GOOGLE_SEARCH_ID`, `ZIMAGI_GOOGLE_SEARCH_API_KEY` configure access to Google Search services.
   *   **Cloud Storage:** `ZIMAGI_GOOGLE_DRIVE_EMAIL`, `ZIMAGI_GOOGLE_DRIVE_PROJECT_ID`, etc., are used for Google Drive integration.
   *   **Docker Daemon:** The `start` script and Docker Compose configurations interact with the local Docker daemon to build and manage containers, using variables like `ZIMAGI_USER_UID` and `ZIMAGI_DOCKER_GID` for user and group permissions within containers.
