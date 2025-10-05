=====================================================
README for Directory: app/systems/kubernetes
=====================================================

Directory Overview
------------------

**Purpose**
   This directory encapsulates the core logic for interacting with a Kubernetes cluster, enabling the deployment, management, and scaling of Zimagi services and workers within a Kubernetes environment. It abstracts the complexities of the Kubernetes API, providing a simplified interface for the Zimagi application.

**Key Functionality**
   *   Kubernetes cluster connection and API interaction.
   *   Deployment and scaling of Zimagi agents.
   *   Creation and management of Zimagi worker jobs.
   *   Configuration management within Kubernetes (ConfigMaps and Secrets).
   *   Base functionalities for Kubernetes resource specification generation.


Dependencies
-------------------------

This directory heavily relies on the `kubernetes` Python client library for interacting with the Kubernetes API. It also depends on Django settings for configuration values such as namespace, pod names, and image pull secrets. Internal dependencies include `utility.data` for data manipulation and `settings.config` for application-wide configuration.


File Structure and Descriptions
-------------------------------

**app/systems/kubernetes/agent.py**
     **Role:** Manages the deployment and scaling of Zimagi agents as Kubernetes Deployments.
     **Detailed Description:** This file defines the `KubeAgent` class, which is responsible for generating Kubernetes Deployment specifications for Zimagi agents. It handles the creation, checking, retrieval, and scaling of these deployments within the Kubernetes cluster. It leverages the `KubeBase` class for common Kubernetes object generation and interacts with the `cluster.py` for API execution.

**app/systems/kubernetes/base.py**
     **Role:** Provides foundational utilities and base classes for generating Kubernetes resource specifications.
     **Detailed Description:** The `KubeBase` class in this file serves as a parent class for other Kubernetes-related modules. It contains common methods for generating labels, selectors, image pull secrets, image pull policies, node selectors, environment variables, volume mounts, metadata, container specifications, and pod specifications. This centralizes common logic and ensures consistency across different Kubernetes resource types.

**app/systems/kubernetes/cluster.py**
     **Role:** Establishes and manages the connection to the Kubernetes cluster and orchestrates operations.
     **Detailed Description:** This file defines the `KubeCluster` class, which is the primary entry point for all Kubernetes interactions. It handles connecting to the Kubernetes API (both in-cluster and via kubeconfig), provides access to various Kubernetes API clients (CoreV1Api, AppsV1Api, BatchV1Api), and includes methods for executing Kubernetes operations with error handling. It also acts as a facade for `KubeAgent`, `KubeWorker`, and `KubeConfig` operations.

**app/systems/kubernetes/config.py**
     **Role:** Manages Kubernetes ConfigMaps for application configuration.
     **Detailed Description:** The `KubeConfig` class in this file provides methods for retrieving and updating Kubernetes ConfigMaps. It allows the application to store and retrieve configuration data dynamically from the Kubernetes cluster, ensuring that services can access shared settings. It interacts with the `KubeCluster` for API calls and uses `utility.data` for value normalization.

**app/systems/kubernetes/worker.py**
     **Role:** Manages the creation and lifecycle of Zimagi worker jobs as Kubernetes Jobs.
     **Detailed Description:** This file defines the `KubeWorker` class, which is responsible for generating Kubernetes Job specifications for Zimagi workers. It handles the creation of these jobs and provides functionality to retrieve active worker jobs within the Kubernetes cluster. It utilizes the `KubeBase` class for common Kubernetes object generation and interacts with the `KubeCluster` for API execution.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The primary entry point for Kubernetes interactions is the `KubeCluster` class in `app/systems/kubernetes/cluster.py`. When a Zimagi service or worker needs to be managed in Kubernetes, the `Manager` (from `app/systems/manager.py`) will instantiate `KubeCluster`. `KubeCluster` then uses its `exec` method to perform operations, delegating to specialized classes like `KubeAgent` (for agent deployments), `KubeWorker` (for worker jobs), and `KubeConfig` (for configuration management). These specialized classes, in turn, leverage the `KubeBase` class for generating the common parts of Kubernetes resource specifications.

**External Interfaces**
   This directory primarily interfaces with the Kubernetes API server. It reads and writes Kubernetes resources such as Deployments, Jobs, Pods, ConfigMaps, and Secrets. It relies on Django's `settings` for various configuration parameters, including the Kubernetes namespace, pod name, and image pull secrets. It also interacts with the Docker daemon (implicitly, through Kubernetes' container runtime) for image management and container execution.
