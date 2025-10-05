Environment Variables
=====================

Environment variables are crucial for configuring the Zimagi platform across different deployment environments. They allow for dynamic adjustments without modifying the codebase.

Overview
--------
Zimagi uses environment variables to control various aspects of its behavior, including database connections, API endpoints, security settings, and operational parameters. These variables are typically loaded from files in the `env/` directory.

Loading Environment Variables
-----------------------------
The `start` script (located in the project root) is the primary mechanism for loading environment variables. It sources files from the `env/` directory based on the chosen deployment profile.

Example: Loading `public.default` and `secret`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When you run `source start standard local default`, the script will:
1.  Source `env/public.default` to load general public settings.
2.  Source `env/secret` (if it exists) to load sensitive credentials.
3.  These variables are then made available to Docker Compose and Zimagi services.

Key Environment Variable Categories
-----------------------------------

1.  **General Application Settings**
    *   `ZIMAGI_APP_NAME`: Name of the application.
    *   `ZIMAGI_DEBUG`: Enable/disable debug mode.
    *   `ZIMAGI_LOG_LEVEL`: Logging verbosity.
    *   `ZIMAGI_PARALLEL_ENABLED`: Enable/disable parallel processing.

2.  **Database Configuration**
    *   `ZIMAGI_POSTGRES_DB`: PostgreSQL database name.
    *   `ZIMAGI_POSTGRES_USER`: PostgreSQL username.
    *   `ZIMAGI_POSTGRES_PASSWORD`: PostgreSQL password.
    *   `ZIMAGI_REDIS_PASSWORD`: Redis password.
    *   `ZIMAGI_QDRANT_ACCESS_KEY`: Qdrant access key.

3.  **API Endpoints & Communication**
    *   `ZIMAGI_COMMAND_HOST`, `ZIMAGI_COMMAND_PORT`: Command API host and port.
    *   `ZIMAGI_DATA_HOST`, `ZIMAGI_DATA_PORT`: Data API host and port.
    *   `ZIMAGI_API_ENCRYPT_COMMAND`, `ZIMAGI_API_ENCRYPT_DATA`: Enable/disable encryption for APIs.

4.  **Security & Authentication**
    *   `ZIMAGI_SECRET_KEY`: Django secret key.
    *   `ZIMAGI_ADMIN_API_KEY`, `ZIMAGI_ADMIN_API_TOKEN`: Admin API credentials.
    *   `ZIMAGI_DEFAULT_ADMIN_USER`, `ZIMAGI_DEFAULT_ADMIN_TOKEN`: Default admin user credentials.
    *   `ZIMAGI_ENCRYPTION_KEY`: General encryption key.

5.  **AI & External Service Integration**
    *   `ZIMAGI_HUGGINGFACE_TOKEN`: Hugging Face API token.
    *   `OPENROUTER_API_KEY`, `DEEPINFRA_API_KEY`: API keys for various AI platforms.
    *   `ZIMAGI_GOOGLE_SEARCH_ID`, `ZIMAGI_GOOGLE_SEARCH_API_KEY`: Google Search API credentials.
    *   `ZIMAGI_GOOGLE_DRIVE_EMAIL`, `ZIMAGI_GOOGLE_DRIVE_PROJECT_ID`: Google Drive integration.

6.  **Docker & Kubernetes Specifics**
    *   `ZIMAGI_DOCKER_RUNTIME`: `standard` or `nvidia`.
    *   `ZIMAGI_USER_UID`, `ZIMAGI_DOCKER_GID`: User and group IDs for container permissions.
    *   `ZIMAGI_KUBERNETES_NAMESPACE`: Kubernetes namespace.

For a complete list and detailed descriptions, refer to the `env/` directory and the `app/settings/core.py` file.
