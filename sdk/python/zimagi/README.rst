=====================================================
README for Directory: sdk/python/zimagi
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the foundational Python SDK for interacting with the Zimagi platform. It provides core client functionalities, communication protocols, data handling, and utility functions necessary for building applications and command-line tools that integrate with Zimagi services. It abstracts away the complexities of API communication, encryption, and data parsing, offering a streamlined interface for developers.

**Key Functionality**
   *   Provides base classes for API clients, handling common concerns like authentication, encryption, and request/response processing.
   *   Manages secure communication with Zimagi services through encryption and custom transport layers.
   *   Offers robust data serialization and deserialization mechanisms for various media types, including JSON and OpenAPI specifications.
   *   Includes utility functions for data manipulation, error handling, and parallel processing.
   *   Defines core exceptions and configuration settings for the Zimagi Python SDK.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for Python 3.x environments, typically running on Linux-based systems, and interacts with Docker containers for Zimagi services.

**Local Dependencies**
   *   ``requests``: Used for making HTTP requests to Zimagi APIs.
   *   ``pycryptodome``: Provides cryptographic primitives for encryption and decryption.
   *   ``terminaltables``: Used for formatting tabular data in terminal output.
   *   ``validators``: Used for URL validation.
   *   ``pandas``: Utilized in the data codecs for handling tabular data (e.g., CSV).
   *   ``oyaml``: Used for YAML serialization/deserialization.
   *   ``magic``: Used for determining file mimetypes.
   *   ``urllib3``: Used for managing HTTP connection pools and disabling warnings.

File Structure and Descriptions
-------------------------------

**sdk/python/zimagi/command**
     **Role:** Contains the client-side implementation for interacting with the Zimagi Command API.
     **Detailed Description:** This subdirectory provides the Python client for executing commands on the Zimagi platform. It includes modules for defining command schemas, encoding/decoding command-specific messages, handling command responses, and managing the HTTP transport layer for command execution. It allows programmatic interaction with Zimagi's command-line interface functionalities.

**sdk/python/zimagi/data**
     **Role:** Contains the client-side implementation for interacting with the Zimagi Data API.
     **Detailed Description:** This subdirectory provides the Python client for interacting with the Zimagi Data API. It includes modules for defining data-specific codecs (like OpenAPI JSON and CSV), managing the HTTP transport for data operations, and providing a high-level client interface for CRUD operations and data queries.

**sdk/python/zimagi/codecs.py**
     **Role:** Defines generic data encoding and decoding strategies for common media types.
     **Detailed Description:** This file contains the `JSONCodec` class, which is responsible for converting raw byte strings into Python data structures and vice-versa for standard JSON payloads. It is a shared codec used by both the command and data API clients to ensure consistent JSON handling.

**sdk/python/zimagi/utility.py**
     **Role:** Provides a collection of general-purpose utility functions.
     **Detailed Description:** This file offers various helper functions for tasks such as URL formatting, API call wrapping, value normalization (e.g., converting strings to booleans or numbers), JSON serialization/deserialization, error formatting, and data caching. These utilities are widely used across the Zimagi SDK to maintain consistency and reduce code duplication.

**sdk/python/zimagi/collection.py**
     **Role:** Implements flexible data structures for attribute access.
     **Detailed Description:** This file defines the `Collection` and `RecursiveCollection` classes, which provide dictionary-like objects that allow attribute-style access (e.g., `obj.key` instead of `obj['key']`). `RecursiveCollection` extends this to nested dictionaries, converting them into `Collection` instances for easier access. These are used to represent API responses and configuration data.

**sdk/python/zimagi/README.rst**
     **Role:** This file is the README document for the `sdk/python/zimagi` directory.
     **Detailed Description:** This document provides an overview of the `sdk/python/zimagi` directory, detailing its purpose, key functionalities, platform dependencies, file structure with descriptions of individual files and subdirectories, and an explanation of the execution flow and external interfaces.

**sdk/python/zimagi/datetime.py**
     **Role:** Provides utilities for handling date and time operations with timezone support.
     **Detailed Description:** This file contains the `Time` class, which offers methods for managing timezones, converting between string and datetime objects, shifting dates, calculating time distances, and generating sequences of dates. It ensures consistent and reliable date/time handling across the SDK.

**sdk/python/zimagi/settings.py**
     **Role:** Defines global configuration settings for the Zimagi Python SDK.
     **Detailed Description:** This file stores default values and configurable parameters for the SDK, such as cache directories, connection retry logic, default host/port information, user credentials, and logging levels. These settings can be overridden to customize the SDK's behavior.

**sdk/python/zimagi/exceptions.py**
     **Role:** Defines custom exception types for Zimagi-specific errors.
     **Detailed Description:** This file centralizes custom exception classes like `ClientError`, `ConnectionError`, `ParseError`, and `ResponseError`. These exceptions provide more specific error handling and context for issues encountered during API communication, data parsing, or client operations within the Zimagi SDK.

**sdk/python/zimagi/auth.py**
     **Role:** Implements authentication mechanisms for API requests.
     **Detailed Description:** This file contains the `ClientTokenAuthentication` class, which is a custom authentication handler for the `requests` library. It manages the inclusion of user and token information in the Authorization header of HTTP requests, optionally encrypting the token before transmission.

**sdk/python/zimagi/transports.py**
     **Role:** Provides base classes for HTTP communication with Zimagi APIs.
     **Detailed Description:** This file defines the `BaseTransport` class, which encapsulates the common logic for making HTTP requests, handling retries, processing responses, and integrating with decoders and encryption. It serves as a foundation for more specialized transport layers in the command and data API clients.

**sdk/python/zimagi/__init__.py**
     **Role:** Initializes the `zimagi` Python package, exposing key components.
     **Detailed Description:** This file serves as the entry point for the `zimagi` package. It imports and makes accessible core client classes (like `CommandClient` and `DataClient`), message types, response objects, and exception classes directly under the `zimagi` namespace, simplifying imports for consumers of the SDK.

**sdk/python/zimagi/client.py**
     **Role:** Provides the abstract base class for all Zimagi API clients.
     **Detailed Description:** This file defines `BaseAPIClient`, which establishes the common structure and functionalities for interacting with Zimagi APIs. It handles client initialization, base URL construction, encryption setup, authentication, and provides a generic request method (`_request`) that delegates to a transport layer. It also includes methods for retrieving API status and schema.

**sdk/python/zimagi/encryption.py**
     **Role:** Implements cryptographic utilities for secure communication.
     **Detailed Description:** This file contains `Cipher`, `NullCipher`, and `AESCipher` classes. `Cipher` acts as a factory for creating either a `NullCipher` (for unencrypted communication) or an `AESCipher` (for AES-256 encryption). `AESCipher` handles the encryption and decryption of messages using AES in CTR mode, ensuring data confidentiality during transmission.

**sdk/python/zimagi/parallel.py**
     **Role:** Provides utilities for executing tasks in parallel using threads.
     **Detailed Description:** This file implements a `ThreadPool` and associated `WorkerThread` classes for managing concurrent execution of tasks. It includes `ThreadResults` to aggregate outcomes, including errors, from parallel operations. The `Parallel` class offers a convenient interface for executing a callback function across a list of items concurrently, improving performance for CPU-bound tasks.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A developer initializes a specific Zimagi client (e.g., `zimagi.CommandClient` or `zimagi.DataClient`) from `sdk/python/zimagi/__init__.py`.
   2.  During client initialization, `sdk/python/zimagi/client.py` sets up the base URL, authentication (`sdk/python/zimagi/auth.py`), and potentially an encryption cipher (`sdk/python/zimagi/encryption.py`).
   3.  The client then retrieves the API status and schema by making requests through its specialized transport (e.g., `sdk/python/zimagi/command/transports.py` or `sdk/python/zimagi/data/transports.py`), which inherits from `sdk/python/zimagi/transports.py`.
   4.  When an API call is made (e.g., `client.execute()` for command or `client.get()` for data), the request is formatted, potentially encrypted, and sent via the transport layer.
   5.  The transport layer handles the HTTP communication, retries, and receives the raw response.
   6.  The raw response is then decrypted (if applicable) and decoded by an appropriate codec (e.g., `sdk/python/zimagi/codecs.py` or specialized codecs in `sdk/python/zimagi/command/codecs.py` or `sdk/python/zimagi/data/codecs.py`) into Python objects, often `Collection` instances from `sdk/python/zimagi/collection.py`.
   7.  Utility functions from `sdk/python/zimagi/utility.py` are frequently used throughout this process for tasks like value normalization and error formatting.
   8.  Errors encountered during this flow are raised as custom exceptions defined in `sdk/python/zimagi/exceptions.py`.
   9.  For operations requiring concurrency, `sdk/python/zimagi/parallel.py` can be utilized to execute tasks across multiple threads.

**External Interfaces**
   *   **Zimagi Command API:** The `sdk/python/zimagi/command` subdirectory directly communicates with the Zimagi Command API over HTTP/HTTPS to execute commands and receive streamed responses.
   *   **Zimagi Data API:** The `sdk/python/zimagi/data` subdirectory directly communicates with the Zimagi Data API over HTTP/HTTPS to perform data operations.
   *   **Operating System:** Interacts with the operating system for file system operations (e.g., caching in `sdk/python/zimagi/utility.py`) and environment variables.
   *   **Network Infrastructure:** Relies on underlying network infrastructure to establish connections and transmit data to Zimagi services.
