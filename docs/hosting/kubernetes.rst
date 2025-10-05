Kubernetes Deployment
=====================

Zimagi supports deployment within a Kubernetes cluster for production-grade scalability and orchestration.

Overview
--------
Kubernetes is an open-source system for automating deployment, scaling, and management of containerized applications. Zimagi's Kubernetes integration allows for robust management of its microservices.

Key Components in Kubernetes
----------------------------
*   **Deployments**: Used for managing Zimagi agents, ensuring a desired number of replicas are running.
*   **Jobs**: Used for running Zimagi worker tasks, which are typically short-lived or batch processes.
*   **ConfigMaps and Secrets**: Used for managing application configurations and sensitive credentials within the cluster.

Kubernetes Integration Logic
----------------------------
The `app/systems/kubernetes` directory contains the core logic for interacting with a Kubernetes cluster:

*   **`app/systems/kubernetes/cluster.py`**: Manages the connection to the Kubernetes API and orchestrates operations.
*   **`app/systems/kubernetes/agent.py`**: Manages the deployment and scaling of Zimagi agents as Kubernetes Deployments.
*   **`app/systems/kubernetes/worker.py`**: Manages the creation and lifecycle of Zimagi worker jobs as Kubernetes Jobs.
*   **`app/systems/kubernetes/config.py`**: Manages Kubernetes ConfigMaps for application configuration.

Scaling Services in Kubernetes
------------------------------
The `app/profiles/start.yml` and `app/profiles/stop.yml` profiles can be used to define the desired scale for various Zimagi services, which can then be translated into Kubernetes deployments.

Example: Scaling an agent
~~~~~~~~~~~~~~~~~~~~~~~~~
You can scale Zimagi agents using the CLI, which interacts with the Kubernetes integration:

.. code-block:: bash

    zimagi service scale my-agent --count 3

This command would instruct the Kubernetes integration to adjust the replica count for `my-agent` to 3.

Configuration Management
------------------------
Kubernetes ConfigMaps are used to store non-sensitive configuration data, while Kubernetes Secrets are used for sensitive information. The `app/systems/kubernetes/config.py` module provides methods for retrieving and updating these.

Troubleshooting
---------------
*   **Pod Logs**: Check logs for individual pods: `kubectl logs [pod_name]`.
*   **Deployment Status**: Monitor the status of deployments: `kubectl get deployments`.
*   **Job Status**: Monitor the status of jobs: `kubectl get jobs`.
