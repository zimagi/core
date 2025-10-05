Scaling Services
================

Zimagi is designed for scalability, allowing you to dynamically adjust the number of running instances for various services and agents to meet demand.

Overview
--------
The platform supports dynamic scaling of worker processes and agents, both in Docker Compose and Kubernetes environments, ensuring efficient resource utilization.

Key Scaling Features
--------------------
*   **Dynamic Worker Scaling**: Adjust the number of Celery workers based on task queue demand.
*   **Agent Scaling**: Scale specific AI agents (e.g., `language_model`, `encoder`, `browser`) independently.
*   **Container Orchestration Integration**: Seamlessly integrates with Docker Compose and Kubernetes for scaling.
*   **Scaling Event Archival**: Track and archive scaling activities for historical analysis.

Scaling Commands (`app/commands/service`, `app/commands/scale.py`)
------------------------------------------------------------------
*   **`app/commands/service/lock`**: Manages distributed service locks (relevant for coordinated scaling).
*   **`app/commands/scale.py`**: Defines the `scale` command for adjusting agent instance counts.

Worker Plugins (`app/plugins/worker`)
-------------------------------------
*   **`app/plugins/worker/base.py`**: Abstract base class for all worker providers.
*   **`app/plugins/worker/docker.py`**: Implements worker management using Docker containers.
*   **`app/plugins/worker/kubernetes.py`**: Implements worker management within a Kubernetes cluster.

Scaling Event Data Model (`app/data/scaling_event`)
---------------------------------------------------
*   **`app/data/scaling_event/models.py`**: Defines the `ScalingEvent` data model.
*   **`app/data/scaling_event/migrations`**: Database migration files for scaling events.

Agent Archiving (`app/commands/agent/archiver.py`)
--------------------------------------------------
*   **`app/commands/agent/archiver.py`**: Agent responsible for archiving scaling events.

Using Scaling Services
----------------------

1.  **Scaling an Agent**: Use the `zimagi service scale` command.

    .. code-block:: bash

        zimagi service scale language_model --count 2

    This command will adjust the number of `language_model` agent instances to 2.

2.  **Stopping All Services**: The `stop` profile can be used to scale all services down to zero.

    .. code-block:: bash

        zimagi run stop

3.  **Monitoring Scaling Events**: Scaling activities are archived by the `archiver` agent and can be viewed through logs or data queries.

    .. code-block:: bash

        zimagi log list --command "agent archiver"

4.  **Distributed Locking**: When implementing custom scaling logic or critical operations, use distributed locks to prevent race conditions.

    .. code-block:: bash

        zimagi service lock set my-critical-lock --expire 60

Dynamic scaling is a core capability of Zimagi, enabling you to build resilient and performant AI-driven applications.
