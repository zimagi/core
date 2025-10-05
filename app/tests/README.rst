=====================================================
README for Directory: app/tests
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central hub for all automated tests within the Zimagi application. Its primary role is to ensure the correctness, reliability, and integration of various components, including command-line interfaces, Python SDK interactions, and data management.

**Key Functionality**
   *  **Command-line Interface (CLI) Testing:** Validates the functionality and behavior of Zimagi's CLI commands.
   *  **Python SDK Testing:** Ensures the correct operation and integration of the Python Software Development Kit with Zimagi APIs.
   *  **Data Integrity and API Validation:** Verifies data creation, manipulation, and retrieval through the Data API, and validates API schemas.
   *  **Reusable Test Utilities:** Provides common base classes, assertion mixins, and data fixtures to promote consistent and efficient test development.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed to run within a Python 3.x environment, specifically leveraging the Django test framework. Tests often interact with Docker containers that host Zimagi services, making a Docker daemon a crucial part of the testing environment.

**Local Dependencies**
   *  `django.test`: The primary framework for running tests.
   *  `zimagi`: The core Python SDK for interacting with the Zimagi platform.
   *  `docker`: Used for managing and interacting with Docker containers during testing.
   *  `utility.data`: Provides data manipulation utilities like `normalize_value` and `dump_json`.
   *  `utility.filesystem`: Used for loading test data from YAML files.
   *  `utility.terminal`: Provides terminal output formatting for test messages.
   *  `openapi_spec_validator`: Used for validating OpenAPI schemas.


File Structure and Descriptions
-------------------------------

**app/tests/command**
     **Role:** This subdirectory houses the base classes and foundational structures for implementing command-line interface (CLI) tests.
     **Detailed Description:** It provides a standardized way to define and execute tests for various Zimagi commands, ensuring consistency and reusability across the testing suite. It includes `base.py` which is an abstract base class for all command-line interface tests, providing core methods for executing tests, managing module profiles (running and destroying them), and retrieving an ordered list of modules relevant to the tests.

**app/tests/data**
     **Role:** This subdirectory serves as a dedicated repository for various YAML-formatted test data files.
     **Detailed Description:** It provides structured configurations, host details, and group definitions that are essential for validating different aspects of the system's functionality, ensuring consistent and reproducible test environments. Files like `group.yml`, `config.yml`, and `host.yml` define mock data for testing.

**app/tests/sdk_python**
     **Role:** This subdirectory houses the Python SDK tests for the Zimagi platform.
     **Detailed Description:** Its primary role is to ensure the correct functionality and integration of the Python client with the Zimagi APIs, covering data operations, command execution, and system initialization. It contains subdirectories for data-related tests (`data`), initialization tests (`init`), and core SDK test utilities (`base.py`, `runner.py`).

**app/tests/mixins**
     **Role:** This directory contains mixin classes designed to provide reusable assertion methods for unit and integration tests.
     **Detailed Description:** These mixins enhance the testing framework by offering specialized assertion utilities beyond the standard Python `unittest` module, such as `TestAssertions` in `assertions.py` for comparing complex data structures and checking key existence.

**app/tests/command_local.py**
     **Role:** This file defines a specific local command test.
     **Detailed Description:** It inherits from `BaseCommandTest` and serves as an entry point for running command-line interface tests in a local context. It demonstrates how to extend the base command testing functionality for specific test scenarios.

**app/tests/base.py**
     **Role:** This file provides a foundational base test class for all Zimagi tests.
     **Detailed Description:** The `BaseTest` class establishes common setup and teardown procedures, and provides core utilities for all tests within the `app/tests` directory. It integrates `TerminalMixin` for output and `TestAssertions` for advanced assertions, ensuring a consistent testing environment.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The overall test execution typically begins with a test runner (e.g., `app/tests/sdk_python/runner.py` for SDK tests or `app/tests/command_local.py` for command tests). These runners discover test classes that inherit from `app/tests/base.py` (or its specialized subclasses like `app/tests/sdk_python/base.py` or `app/tests/command/base.py`). During setup, API clients are initialized, and test data (often loaded from `app/tests/data`) is prepared. Individual test methods then use these clients and data to perform operations and assert expected outcomes, leveraging assertion utilities from `app/tests/mixins/assertions.py`. Cleanup procedures are executed during teardown.

**External Interfaces**
   The tests in this directory primarily interact with the Zimagi Command API and Data API, which are typically exposed via HTTP endpoints (e.g., `localhost:5000`). They also implicitly rely on a running Docker daemon to manage Zimagi service containers (PostgreSQL, Redis, Qdrant) that provide the backend for the APIs. Test data is loaded from YAML files within the `app/tests/data` directory.
