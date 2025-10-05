=====================================================
README for Directory: sdk/javascript/src/client
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains the core client-side implementations for interacting with the Zimagi API. It provides the foundational classes and specific client implementations for Command and Data API interactions, enabling JavaScript applications to communicate with the Zimagi backend services.

**Key Functionality**
   *  **Base API Client:** Provides common functionalities for all Zimagi API clients, including request handling, authentication, encryption, caching, and performance monitoring.
   *  **Command API Client:** Facilitates the execution of commands, module extensions, task running, and profile management within the Zimagi system.
   *  **Data API Client:** Enables CRUD operations, data retrieval in various formats (JSON, CSV), and schema introspection for Zimagi data models.


Dependencies
-------------------------

*   **Node.js:** The JavaScript runtime environment for executing the SDK.
*   **TypeScript:** The language used for developing the SDK, providing type safety and improved maintainability.
*   **`../transports/command` and `../transports/data`:** These internal modules provide the HTTP transport layer for Command and Data API clients, respectively.
*   **`../codecs/index`:** Provides various codecs (e.g., `ZimagiJSONCodec`, `JSONCodec`, `OpenAPIJSONCodec`, `CSVCodec`) for encoding and decoding API responses.
*   **`../exceptions`:** Defines custom exception classes for handling API-related errors.
*   **`../schema/index`:** Contains schema definitions, including `Root` and `Action`, used for understanding API structure and validating commands.
*   **`../command/response`:** Defines the structure for command responses.
*   **`../utility`:** Provides utility functions like `getServiceURL`.
*   **`../auth`:** Contains authentication mechanisms, specifically `ClientTokenAuthentication`.
*   **`../encryption`:** Provides encryption utilities, including `Cipher`.
*   **`../cache`:** Offers caching mechanisms for API responses.
*   **`../performance`:** Includes performance monitoring utilities.


File Structure and Descriptions
-------------------------------

**sdk/javascript/src/client/base.ts**
     **Role:** Defines the foundational `BaseAPIClient` class, which encapsulates common functionalities required by all Zimagi API clients.
     **Detailed Description:** This file establishes the core structure for interacting with any Zimagi API. It manages host, port, user, token, encryption, and protocol settings. It includes methods for making HTTP requests (`_request`), handling authentication (`ClientTokenAuthentication`), encryption (`Cipher`), caching (`cache`), and performance monitoring (`performanceMonitor`). It also provides mechanisms for retrieving the service status (`getStatus`) and the API schema (`getSchema`), and includes error formatting and caching utilities. All other specific API clients (like `CommandClient` and `DataClient`) extend this base class to inherit these fundamental capabilities.

**sdk/javascript/src/client/data.ts**
     **Role:** Implements the `DataClient` class, providing methods for interacting with the Zimagi Data API to perform CRUD operations and retrieve data.
     **Detailed Description:** This file focuses on data management within the Zimagi ecosystem. The `DataClient` extends `BaseAPIClient` and utilizes `DataHTTPTransport` for its communication. It offers methods for creating (`create`), updating (`update`), deleting (`delete`), and retrieving (`get`, `getByKey`, `list`) data records. It also supports retrieving data in specific formats like JSON (`json`) and CSV (`csv`), and provides utilities for fetching field values (`values`), record counts (`count`), and downloading datasets (`download`). The client can introspect the data schema to understand data types, ID fields, key fields, and various other field properties (system, unique, dynamic, atomic, scope, relation, reverse).

**sdk/javascript/src/client/command.ts**
     **Role:** Implements the `CommandClient` class, which enables interaction with the Zimagi Command API for executing commands and managing modules, tasks, and profiles.
     **Detailed Description:** This file defines the `CommandClient` responsible for sending commands to the Zimagi backend. It extends `BaseAPIClient` and uses `CommandHTTPTransport`. Key functionalities include initializing and managing available commands based on the API schema (`_initCommands`), executing arbitrary commands (`execute`), extending the system with remote modules (`extend`), running specific tasks (`runTask`), managing profiles (running `runProfile` and destroying `destroyProfile`), and initiating imports (`runImports`) and calculations (`runCalculations`). It also includes internal methods for normalizing command paths (`_normalizePath`), looking up commands in the schema (`_lookup`), and validating command options (`_validate`).


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A JavaScript application instantiates either a `CommandClient` or `DataClient` from this directory, providing configuration options.
   2.  Upon initialization (e.g., `client.initialize()`), the client fetches the API schema by making a `GET` request to the base URL via its `BaseAPIClient` parent. This schema is then cached.
   3.  For `CommandClient`, the schema is used to dynamically populate available commands and actions.
   4.  When a method like `client.execute('some/command', options)` (for `CommandClient`) or `client.create('dataType', fields)` (for `DataClient`) is called, the request is prepared.
   5.  The request is then passed to the `_request` method of `BaseAPIClient`, which utilizes the configured `transport` (either `CommandHTTPTransport` or `DataHTTPTransport`) to send the HTTP request to the Zimagi API.
   6.  The transport layer handles the actual network communication, including authentication and encryption if configured.
   7.  Upon receiving a response, the `decoders` (e.g., `ZimagiJSONCodec`, `JSONCodec`) process the raw data into a usable format.
   8.  The `_request` method then returns the processed data, or throws a `ClientError` or `ResponseError` if an issue occurred.

**External Interfaces**
   *   **Zimagi Command API:** The `CommandClient` communicates directly with the Zimagi Command API endpoint (typically on port 5123) to execute system commands, manage modules, and orchestrate tasks and profiles.
   *   **Zimagi Data API:** The `DataClient` interacts with the Zimagi Data API endpoint (typically on port 5323) to perform all data-related operations, including CRUD, querying, and schema introspection.
   *   **Operating System/Network:** Both clients rely on the underlying Node.js environment and network stack to establish HTTP/HTTPS connections to the Zimagi backend services.
   *   **Caching Mechanism:** The `BaseAPIClient` utilizes an internal caching mechanism (defaulting to `defaultCache`) to store API schema and other frequently accessed data, reducing redundant API calls.
   *   **Performance Monitoring:** The `BaseAPIClient` integrates with a performance monitoring system (defaulting to `defaultMonitor`) to track the timing of API requests.
