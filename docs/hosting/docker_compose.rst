Docker Compose Deployment
=========================

Zimagi leverages Docker Compose for orchestrating its services in development and local environments.

Overview
--------
Docker Compose allows you to define and run multi-container Docker applications. With Zimagi, it's used to manage the database, message queue, vector database, and various Zimagi microservices.

Configuration Files
-------------------
The `env/` directory contains environment-specific configuration files that are crucial for Docker Compose:

*   **`env/public.default`**: Default public environment variables.
*   **`env/public.api`**: Public environment variables for API-specific deployments.
*   **`env/public.api.encrypted`**: Public environment variables for encrypted API deployments.
*   **`env/secret.example`**: Template for sensitive information and secrets.

These files are sourced by the `start` script to populate the `.env` file used by Docker Compose.

Starting Services
-----------------
To start Zimagi services using Docker Compose, you typically use the `start` script from the project root:

.. code-block:: bash

    source start [type: standard | nvidia] [environment: local | test] [configuration: default | api | api.encrypted]

This command will:
1.  Load the appropriate environment variables from the `env/` directory.
2.  Build Docker images based on `docker/Dockerfile.cli` and `docker/Dockerfile.server`.
3.  Launch services defined in the `compose.*.yaml` files (e.g., `compose.standard.local.yaml`).

Key Services Managed by Docker Compose
--------------------------------------
*   **PostgreSQL**: The primary relational database.
*   **Redis**: Used for caching, message brokering (Celery), and inter-service communication.
*   **Qdrant**: The vector database for AI features.
*   **Command API**: Handles command execution requests.
*   **Data API**: Manages data model interactions.
*   **MCP API**: Management Control Plane API for external systems and AI agents.
*   **Controller**: Orchestrates other Zimagi components.
*   **Scheduler**: Manages scheduled tasks.
*   **Workers**: Process asynchronous tasks.

Stopping Services
-----------------
To stop all running Zimagi services:

.. code-block:: bash

    zimagi run stop

This command uses the `app/profiles/stop.yml` profile to scale down all services to zero.

Troubleshooting
---------------
*   **Service Health Checks**: Docker Compose configurations often include health checks using `curl` to ensure services are ready.
*   **Logs**: Check Docker container logs for errors: `docker-compose logs [service_name]`.
