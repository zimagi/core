=====================================================
README for Directory: app/tests/sdk_python
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the Python SDK tests for the Zimagi platform. Its primary role is to ensure the correct functionality and integration of the Python client with the Zimagi APIs, covering data operations, command execution, and system initialization.

**Key Functionality**
   *  **API Client Testing:** Validates the interactions between the Python SDK and the Zimagi Command and Data APIs.
   *  **Data Model Verification:** Confirms that data creation, retrieval, and manipulation operations work as expected across various Zimagi data types.
   *  **System Initialization Checks:** Ensures that core Zimagi services and schema are correctly initialized and accessible.
   *  **Scheduled Task Validation:** Tests the scheduling and execution of tasks via the Zimagi platform.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed to run within a Python 3.x environment, specifically targeting the Django test framework. It interacts with Docker containers for Zimagi services and relies on the Zimagi platform's API for its operations.

**Local Dependencies**
   *  `django.test`: Provides the testing framework and utilities for running tests.
   *  `zimagi`: The core Python SDK for interacting with the Zimagi platform.
   *  `docker`: Used for managing and interacting with Docker containers that host Zimagi services during testing.
   *  `utility.data`: Provides data manipulation utilities like `normalize_value` and `dump_json`.
   *  `utility.filesystem`: Used for loading test data from YAML files.
   *  `utility.terminal`: Provides terminal output formatting for test messages.
   *  `openapi_spec_validator`: Used for validating OpenAPI schemas.

File Structure and Descriptions
-------------------------------

**app/tests/sdk_python/data**
     **Role:** This subdirectory contains test cases specifically focused on data-related operations through the Zimagi Data API.
     **Detailed Description:** Files within this directory define tests for creating, listing, updating, and deleting various data types managed by Zimagi. They often involve loading predefined test data and asserting the correct state and content after API interactions. For example, `test_group.py` tests group management functionalities.

**app/tests/sdk_python/init**
     **Role:** This subdirectory holds test cases that verify the initial setup, schema integrity, and basic functionality of the Zimagi platform and its APIs.
     **Detailed Description:** Tests here cover critical initialization aspects such as OpenAPI schema validation (`test_schema.py`), basic data creation (`test_create.py`), system status checks (`test_status.py`), and the scheduling mechanisms (`test_schedule.py`). These tests ensure that the fundamental components of Zimagi are correctly configured and operational.

**app/tests/sdk_python/runner.py**
     **Role:** This file defines a custom test runner for the Django test suite, extending the default `DiscoverRunner`.
     **Detailed Description:** The `TestRunner` class in this file customizes how tests are discovered and executed within the Django framework. It overrides the `run_tests` method to potentially add custom setup or teardown logic, or to integrate with specific reporting mechanisms. It ensures that the test environment is properly set up and torn down, and it prints time-keeping results.

**app/tests/sdk_python/base.py**
     **Role:** This file provides a base test class (`BaseTest`) that all other Python SDK test cases inherit from, establishing common setup and teardown procedures and API client initialization.
     **Detailed Description:** The `BaseTest` class sets up the `command_api` and `data_api` clients for interacting with Zimagi's Command and Data APIs, respectively. It handles authentication and configuration for these clients. It also includes methods for loading test data (`_load_data`) and a message callback for API responses (`_message_callback`), ensuring a consistent testing environment and reducing boilerplate in individual test files. It inherits from `django.test.TestCase` and custom mixins for assertions and terminal output.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `TestRunner` in `app/tests/sdk_python/runner.py` is the entry point for executing the test suite.
   2.  `TestRunner` discovers test classes that inherit from `BaseTest` in `app/tests/sdk_python/base.py`.
   3.  For each test class, `BaseTest.setUpClass()` initializes the `command_api` and `data_api` clients, configuring them with necessary credentials and API endpoints.
   4.  Individual test methods within `app/tests/sdk_python/data` and `app/tests/sdk_python/init` then use these initialized API clients to perform operations against the running Zimagi services.
   5.  Assertions are made on the API responses to validate functionality.
   6.  After all tests in a class are run, `BaseTest.tearDownClass()` is called to perform any necessary cleanup.

**External Interfaces**
   *  **Zimagi Command API:** The `command_api` client (initialized in `base.py`) interacts with the Zimagi Command API, typically running on `localhost:5000` (or a configured port), to execute commands and tasks.
   *  **Zimagi Data API:** The `data_api` client (initialized in `base.py`) interacts with the Zimagi Data API, typically on `localhost:5000` (or a configured port), for all data-related operations (create, list, update, delete).
   *  **Docker Daemon:** The tests implicitly rely on a running Docker daemon to manage and interact with the Zimagi service containers (e.g., starting, stopping, inspecting logs).
   *  **PostgreSQL, Redis, Qdrant:** The Zimagi services themselves (which the SDK tests interact with) depend on these database services for their persistence and caching layers.
