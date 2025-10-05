=====================================================
README for Directory: sdk/javascript/src
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the main entry point and core implementation for the Zimagi JavaScript SDK. It provides a comprehensive set of functionalities for interacting with Zimagi backend services, including command execution, data management, authentication, encryption, caching, and performance monitoring, all designed to be consumed by client-side JavaScript applications.

**Key Functionality**
   *   Provides base classes and specific client implementations for Command and Data API interactions.
   *   Manages authentication and encryption for secure communication with Zimagi services.
   *   Offers a robust message system for handling various types of responses (status, data, info, error).
   *   Includes a flexible codec system for encoding and decoding different data formats (JSON, CSV, OpenAPI JSON, Zimagi JSON).
   *   Implements a caching mechanism and performance monitoring for optimized client operations.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for JavaScript environments, primarily targeting execution within Node.js or modern web browsers as an integral part of the Zimagi JavaScript SDK. It is built to be compatible with standard JavaScript runtimes.

**Local Dependencies**
   This directory relies on standard JavaScript features and the `fetch` API for making HTTP requests. It also depends on internal SDK components for error handling, command-specific responses, message parsing, and utility functions.


File Structure and Descriptions
-------------------------------

**sdk/javascript/src/command**
     **Role:** This directory is a core component of the Zimagi JavaScript SDK, specifically designed to handle the processing and management of command responses received from the Zimagi backend.
     **Detailed Description:** It provides a structured way to parse, store, and access various types of messages and data returned by Zimagi commands, ensuring a consistent and manageable interface for command execution results. It includes the `CommandResponse` class, which encapsulates all information returned by a Zimagi command, categorizing messages, handling errors, and providing access to named data payloads.

**sdk/javascript/src/messages**
     **Role:** This directory is dedicated to defining and managing the message system for the Zimagi JavaScript SDK.
     **Detailed Description:** It provides a structured way to handle various types of messages, including status updates, data payloads, informational messages, warnings, and errors, ensuring consistent communication within the SDK and with external systems. It contains the base `Message` class and specialized message classes like `StatusMessage`, `DataMessage`, `ErrorMessage`, etc., each with specific behaviors for rendering, formatting, and display.

**sdk/javascript/src/codecs**
     **Role:** This directory contains various codec implementations for encoding and decoding data in different formats within the Zimagi JavaScript SDK.
     **Detailed Description:** It provides classes for handling `JSON`, `CSV`, `OpenAPI JSON`, and `Zimagi JSON` data formats. These codecs are crucial for serializing outgoing request data and deserializing incoming API responses, ensuring that the SDK can communicate effectively with diverse Zimagi backend endpoints. Each codec extends a `BaseCodec` and defines its supported media types and `encode`/`decode` methods.

**sdk/javascript/src/client**
     **Role:** This directory contains the core client-side implementations for interacting with the Zimagi API.
     **Detailed Description:** It provides the foundational `BaseAPIClient` class, which encapsulates common functionalities like request handling, authentication, encryption, caching, and performance monitoring. It also includes specific client implementations: `CommandClient` for executing commands, managing modules, tasks, and profiles, and `DataClient` for CRUD operations, data retrieval, and schema introspection for Zimagi data models.

**sdk/javascript/src/transports**
     **Role:** This directory contains the core transport implementations for the Zimagi JavaScript SDK, responsible for handling communication with the Zimagi backend services over HTTP.
     **Detailed Description:** It abstracts the underlying network requests, message encoding/decoding, and error handling, providing a consistent interface for the SDK's client-side operations. It includes `BaseTransport` for common HTTP request logic, `DataHTTPTransport` for interacting with the Zimagi Data API, and `CommandHTTPTransport` for streaming communication with the Zimagi Command API.

**sdk/javascript/src/schema**
     **Role:** This directory defines the data structures and schema classes used throughout the Zimagi JavaScript SDK.
     **Detailed Description:** It provides a structured way to represent API responses, commands, actions, and other data entities, ensuring consistency and type safety across the client-side application. It exports classes such as `Root`, `Router`, `Action`, `Field`, `Error`, `SchemaObject`, and `SchemaArray`, which are used to parse and interpret API metadata into structured JavaScript objects.

**sdk/javascript/src/exceptions.ts**
     **Role:** This file defines custom exception classes for handling various error conditions within the Zimagi JavaScript SDK.
     **Detailed Description:** It provides a hierarchy of error classes, including `ClientError` (base class for all client-side errors), `ConnectionError` (for network connectivity issues), `ParseError` (for data parsing failures), `ResponseError` (for HTTP response errors), and `CommandParseError` (for specific command parsing issues). These classes allow for more granular error handling and clearer debugging.

**sdk/javascript/src/performance.ts**
     **Role:** This file provides utilities for performance monitoring within the Zimagi JavaScript SDK.
     **Detailed Description:** It defines the `PerformanceMonitor` class, which allows for tracking the duration of various operations. It includes methods to start and end timing, retrieve metrics for specific operations, calculate average durations, and get comprehensive statistics. A default `PerformanceMonitor` instance is also exported for convenience.

**sdk/javascript/src/encryption.ts**
     **Role:** This file provides encryption and decryption utilities for secure communication within the Zimagi JavaScript SDK.
     **Detailed Description:** It defines a `Cipher` factory class that returns either a `NullCipher` (for no encryption) or an `AESCipher` (for AES-256-CTR encryption) based on the provided key. The `AESCipher` handles the generation of initialization vectors (IVs) and the encryption/decryption of messages, including support for binary data.

**sdk/javascript/src/auth.ts**
     **Role:** This file implements the authentication system for the Zimagi JavaScript SDK.
     **Detailed Description:** It contains the `ClientTokenAuthentication` class, which manages user credentials (username and token) and applies them to outgoing request headers. It also integrates with the client's encryption mechanism to encrypt the authentication token if a cipher is available, ensuring secure transmission of credentials.

**sdk/javascript/src/cache.ts**
     **Role:** This file provides a simple in-memory caching system for the Zimagi JavaScript SDK.
     **Detailed Description:** It defines the `Cache` class, which allows for storing and retrieving key-value pairs with an optional time-to-live (TTL). It includes methods for setting, getting, checking existence, deleting, and clearing cache entries, as well as managing expired items. A default `Cache` instance is provided for general use.

**sdk/javascript/src/README.rst**
     **Role:** This file serves as the documentation for the `sdk/javascript/src` directory.
     **Detailed Description:** It provides an overview of the directory's purpose, key functionalities, dependencies, and detailed descriptions of the files contained within it. This README is crucial for understanding the architecture and usage of the Zimagi JavaScript SDK.

**sdk/javascript/src/index.ts**
     **Role:** This file serves as the main entry point and public API for the entire Zimagi JavaScript SDK.
     **Detailed Description:** It re-exports all essential classes, functions, and interfaces from the various sub-directories, making them easily accessible to consumers of the SDK. This includes utilities, exceptions, authentication, encryption, codecs, transports, API clients, schema definitions, messages, and command response handling.

**sdk/javascript/src/utility.ts**
     **Role:** This file provides a collection of general-purpose utility functions for the Zimagi JavaScript SDK.
     **Detailed Description:** It includes functions such as `getServiceURL` for constructing API endpoint URLs, `normalizeValue` for converting string representations to appropriate JavaScript types (e.g., boolean, number, JSON), `formatOptions` for preparing HTTP request parameters, and `formatError` for consistent error message formatting.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The typical execution flow begins when a JavaScript application imports and instantiates either a `CommandClient` or `DataClient` from the `sdk/javascript/src/client` directory. Upon instantiation, the client's `initialize()` method is often called, which in turn uses `BaseAPIClient` (from `sdk/javascript/src/client` directory) to fetch the API schema via a `GET` request. This request is handled by the appropriate transport (from `sdk/javascript/src/transports` directory), which uses the `fetch` API and applies authentication (from `sdk/javascript/src/auth.ts`) and encryption (from `sdk/javascript/src/encryption.ts`) if configured. The response is then decoded by one of the codecs (from `sdk/javascript/src/codecs` directory) and structured according to the schema definitions (from `sdk/javascript/src/schema` directory). Subsequent API calls made through the client (e.g., `execute` for commands, `create` for data) follow a similar path, leveraging the transport, authentication, encryption, and codec layers. Performance metrics are collected throughout this process by `PerformanceMonitor` (from `sdk/javascript/src/performance.ts`), and frequently accessed data may be cached by `Cache` (from `sdk/javascript/src/cache.ts`). Errors encountered at any stage are handled by the exception classes defined in `sdk/javascript/src/exceptions.ts`. The `sdk/javascript/src/index.ts` file serves as the primary entry point for consuming all these functionalities.

**External Interfaces**
   The code in `sdk/javascript/src` primarily interacts with the Zimagi Command API and Data API endpoints over HTTP/HTTPS. It relies on the underlying JavaScript runtime's `fetch` API for network communication. Authentication is handled via tokens, potentially encrypted. Data is exchanged in various formats (JSON, CSV) as defined by the codecs. It also interacts with the browser's `console` for debugging and logging purposes.
