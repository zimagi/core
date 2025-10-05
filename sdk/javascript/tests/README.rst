=====================================================
README for Directory: sdk/javascript/tests
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the comprehensive testing suite for the JavaScript SDK, ensuring the reliability, correctness, and integration of its various components. It validates the functionality of client interactions, message handling, schema parsing, transport layers, and overall system integration.

**Key Functionality**
   *   Validation of command response parsing and message handling.
   *   Verification of client-side API interactions for both command and data services.
   *   Testing of different transport mechanisms (e.g., HTTP) for communication.
   *   Confirmation of correct schema object and array parsing and representation.
   *   End-to-end integration tests with a running Zimagi environment.

Dependencies
-------------------------

The tests in this directory primarily rely on the `jest` testing framework for execution and assertion. They also depend on the core modules of the JavaScript SDK itself, which are located in `sdk/javascript/src`. For integration tests, a running Zimagi environment with specific environment variables configured is required to connect to the command and data APIs.

File Structure and Descriptions
-------------------------------

**sdk/javascript/tests/schema.test.ts**
     **Role:** This file contains unit tests for the schema-related classes within the JavaScript SDK.
     **Detailed Description:** It verifies the correct initialization and behavior of `Root`, `Router`, `Action`, `Field`, `Error`, `SchemaObject`, and `SchemaArray` classes. These tests ensure that schema definitions are correctly parsed and accessible, which is crucial for the SDK's ability to understand and interact with the Zimagi API's structure.

**sdk/javascript/tests/client.test.ts**
     **Role:** This file provides unit tests for the base and specific client implementations in the JavaScript SDK.
     **Detailed Description:** It tests the `BaseAPIClient`, `CommandClient`, and `DataClient` classes, ensuring their proper initialization, default option handling, URL formatting, and error conditions (e.g., when a transport is not defined). It validates the client's ability to construct requests and handle basic configurations.

**sdk/javascript/tests/transports.test.ts**
     **Role:** This file contains unit tests for the transport layer implementations used by the JavaScript SDK.
     **Detailed Description:** It focuses on the `BaseTransport`, `CommandHTTPTransport`, and `DataHTTPTransport` classes. These tests verify the initialization of transports, error handling for unimplemented methods, decoder selection, and basic utility functions like `_sleep`. It ensures that the SDK can correctly send and receive data over various protocols.

**sdk/javascript/tests/integration.test.ts**
     **Role:** This file performs integration tests for the command and data client functionality against a live Zimagi environment.
     **Detailed Description:** These tests are designed to run against a deployed Zimagi instance, validating end-to-end communication. They check the ability to retrieve status, schema, and list users, ensuring that the SDK can successfully interact with the Zimagi command and data APIs when properly configured with environment variables. These tests are skipped if the necessary environment variables are not set.

**sdk/javascript/tests/README.rst**
     **Role:** This file provides documentation and an overview of the `sdk/javascript/tests` directory.
     **Detailed Description:** This README explains the purpose, functionality, dependencies, file structure, and execution flow of the test suite for the JavaScript SDK, serving as a guide for developers and other AI models.

**sdk/javascript/tests/messages.test.ts**
     **Role:** This file contains unit tests for the various message implementations within the JavaScript SDK.
     **Detailed Description:** It validates the `Message`, `StatusMessage`, `DataMessage`, `WarningMessage`, and `ErrorMessage` classes. Tests cover initialization with options, error identification, data handling, message rendering, formatting, and display behavior (e.g., logging to console). This ensures consistent and correct message processing throughout the SDK.

**sdk/javascript/tests/command.test.ts**
     **Role:** This file provides unit tests for the `CommandResponse` class, which handles responses from the Zimagi command API.
     **Detailed Description:** It verifies the initialization of `CommandResponse` with default values, the addition of different message types (status, data, error), and the extraction of specific data like named data, active user, and log key. It also tests error message generation and the iterability of the response object, ensuring robust handling of command execution results.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow within this directory is primarily driven by the `jest` testing framework.
   1.  When `jest` is run, it discovers test files (e.g., `*.test.ts`).
   2.  Each test file (e.g., `schema.test.ts`, `client.test.ts`, `messages.test.ts`, `command.test.ts`, `transports.test.ts`) is executed independently.
   3.  Within each test file, individual `describe` blocks group related tests, and `test` blocks define specific assertions.
   4.  The `integration.test.ts` file has a conditional execution flow; it checks for the presence of specific environment variables (`ZIMAGI_COMMAND_HOST`, `ZIMAGI_COMMAND_PORT`, etc.) before running its tests. If these variables are not set, the integration tests are skipped.
   5.  `beforeAll` hooks in `integration.test.ts` initialize `CommandClient` and `DataClient` instances, which then make actual network requests.

**External Interfaces**
   *   **Zimagi Command API:** The `integration.test.ts` file directly interacts with the Zimagi Command API (via `CommandClient`) to retrieve status and schema information.
   *   **Zimagi Data API:** The `integration.test.ts` file also interacts with the Zimagi Data API (via `DataClient`) to retrieve status, schema, and list users.
   *   **Environment Variables:** The `integration.test.ts` file relies on environment variables (e.g., `ZIMAGI_COMMAND_HOST`, `ZIMAGI_COMMAND_PORT`, `ZIMAGI_DEFAULT_ADMIN_TOKEN`, `ZIMAGI_ADMIN_API_KEY`) to configure connections to the Zimagi services.
   *   **Console Output:** `messages.test.ts` specifically tests interactions with `console.warn` and `console.log` to ensure messages are displayed correctly.
