Running Tests
=============

The Zimagi platform includes a comprehensive test suite to ensure the reliability, correctness, and integration of its various components.

Overview
--------
Tests cover command-line interfaces, Python SDK interactions, data management, API validation, and more. The testing framework is built on Django's test utilities and interacts with a running Zimagi environment.

Test Directory Structure
------------------------
The `app/tests/` directory is the central hub for all automated tests:

*   **`app/tests/command`**: Base classes and structures for CLI tests.
*   **`app/tests/data`**: YAML-formatted test data files.
*   **`app/tests/sdk_python`**: Python SDK tests.
*   **`app/tests/mixins`**: Reusable assertion methods.
*   **`app/tests/base.py`**: Foundational base test class for all Zimagi tests.

Prerequisites for Running Tests
-------------------------------
1.  **Docker Daemon**: Ensure a Docker daemon is running on your system.
2.  **Zimagi Services**: Zimagi services must be up and running. You can start them using the `start` script:

    .. code-block:: bash

        source start standard local test

    This will start the services in a `test` environment configuration.

Executing Tests
---------------
To run the entire test suite:

.. code-block:: bash

    python manage.py test

This command will:
1.  Discover test classes that inherit from `app/tests/base.py`.
2.  Initialize `command_api` and `data_api` clients for interacting with Zimagi's APIs.
3.  Load test data (often from `app/tests/data`).
4.  Execute individual test methods against the running Zimagi services.
5.  Perform assertions using utilities from `app/tests/mixins/assertions.py`.
6.  Clean up resources after tests.

Specific Test Suites
--------------------

*   **Python SDK Tests**: Located in `app/tests/sdk_python`, these tests validate the Python client's interaction with Zimagi APIs.
*   **CLI Tests**: Located in `app/tests/command`, these tests verify the functionality of Zimagi's command-line interface.

Custom Test Runner
------------------
The `app/tests/sdk_python/runner.py` defines a custom test runner that extends Django's `DiscoverRunner`, allowing for custom setup/teardown logic and time-keeping results.
