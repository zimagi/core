=====================================================
README for Directory: .circleci
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the continuous integration and continuous deployment (CI/CD) configurations for the project, specifically utilizing CircleCI. Its primary role is to automate the testing, building, and deployment processes for various components of the Zimagi application, ensuring code quality and efficient delivery.

**Key Functionality**
   * Automated testing of API commands, SDKs (JavaScript and Python), and scheduling functionalities.
   * Building and deploying Docker images for both CLI and server components across different architectures (AMD64, ARM64) and environments (standard, NVIDIA).
   * Publishing SDKs to package managers (NPM, Pip).
   * Deploying documentation and updating Helm charts.

Dependencies
-------------------------

The configurations within this directory rely on the CircleCI platform itself. Specific jobs within `config.yml` utilize Docker images for their execution environments (e.g., `ubuntu-2404:current`, `cimg/node:24.6.0`, `python:3.12`). It also depends on standard shell utilities (`bash`, `git`, `curl`, `docker`, `npm`, `pip`) and project-specific scripts located in `docker/`, `sdk/javascript/`, `sdk/python/`, `docs/`, and `app/`.

File Structure and Descriptions
-------------------------------

**.circleci/config.yml**
     **Role:** This file defines the entire CI/CD pipeline for the Zimagi project on CircleCI.
     **Detailed Description:** It orchestrates a series of jobs, including various types of tests (API commands, SDK tests, schema validation, schedule tests) and deployment steps (Docker image builds and pushes for CLI and server, NPM and Pip package deployments, documentation deployment, and Helm chart updates). The file uses CircleCI's `machine` executor for most jobs, specifying different Ubuntu versions and resource classes (e.g., `arm.medium` for ARM builds). It leverages shared `volumes` and `run` commands for environment setup and cleanup. Workflows are defined to manage the execution order and dependencies of these jobs, with filters for branches and tags to control when specific jobs run.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The `config.yml` file is the central entry point for all CI/CD processes. When code is pushed to the repository or a tag is created, CircleCI triggers the workflows defined in this file. Each workflow consists of multiple jobs that execute sequentially or in parallel based on their `requires` dependencies. For example, test jobs (e.g., `test-api-commands`, `test-python-sdk`) run first to ensure code quality. Upon successful completion of relevant tests, deployment jobs (e.g., `deploy-cli-docker-amd64-latest`, `deploy-npm`) are triggered. Many jobs start by sourcing the project's `start` script to initialize the Zimagi runtime environment, and then execute project-specific test or deployment scripts.

**External Interfaces**
   *   **Docker Hub:** The deployment jobs interact with Docker Hub to push built Docker images (e.g., `zimagi/cli`, `zimagi/server`).
   *   **NPM Registry:** The `deploy-npm` job publishes JavaScript SDK packages to the NPM registry.
   *   **PyPI (Python Package Index):** The `deploy-pip` job publishes Python SDK packages to PyPI.
   *   **GitHub:** The `deploy-docs` and `update-helm-chart` jobs interact with GitHub to push documentation updates and Helm chart version changes to their respective repositories.
   *   **Internal Zimagi Services:** During testing, the `start` script brings up various Zimagi services (command-api, data-api, mcp-api, controller, scheduler, tasks) using Docker Compose, and tests interact with these running services.
   *   **Curl:** Used within health checks for various services to verify their availability.
