=====================================================
README for Directory: sdk/javascript/src/transports
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains the core transport implementations for the Zimagi JavaScript SDK, responsible for handling communication with the Zimagi backend services over HTTP. It abstracts the underlying network requests, message encoding/decoding, and error handling, providing a consistent interface for the SDK's client-side operations.

**Key Functionality**
   *   **Base Transport Logic:** Provides foundational methods for making HTTP requests, handling retries, and managing common request/response processing.
   *   **Data API Communication:** Specifically manages interactions with the Zimagi Data API for CRUD operations and schema requests.
   *   **Command API Streaming:** Handles real-time, streaming communication with the Zimagi Command API, processing individual messages as they arrive.

Dependencies
-------------------------

The code in this directory relies on standard JavaScript/TypeScript features and the `fetch` API for making HTTP requests. It also depends on internal SDK components such as `../exceptions` for error handling, `../command/response` for command-specific responses, and `../messages` for message parsing.

File Structure and Descriptions
-------------------------------

**sdk/javascript/src/transports/base.ts**
     **Role:** Defines the foundational `BaseTransport` class, which all other transport implementations extend.
     **Detailed Description:** This file establishes the common functionalities required for any HTTP transport within the Zimagi JavaScript SDK. It includes methods for debugging, making generic HTTP requests (`request`), handling request retries, and managing the overall request lifecycle. It also provides mechanisms for encrypting request parameters and decrypting response messages using a client-provided cipher, as well as decoding messages based on content type. The `handleRequest` method is an abstract method that must be implemented by concrete transport classes.

**sdk/javascript/src/transports/data.ts**
     **Role:** Implements the `DataHTTPTransport` for interacting with the Zimagi Data API.
     **Detailed Description:** This file extends `BaseTransport` to provide specific logic for communicating with the Zimagi Data API. It overrides the `handleRequest` method to differentiate between status requests, schema/root requests, and general data requests (GET, POST, PUT, DELETE). It includes an `updateData` method for handling data modification requests, ensuring proper content-type headers and error handling specific to data operations. This transport is responsible for managing encrypted communication for data-related endpoints.

**sdk/javascript/src/transports/command.ts**
     **Role:** Implements the `CommandHTTPTransport` for streaming communication with the Zimagi Command API.
     **Detailed Description:** This file extends `BaseTransport` to manage interactions with the Zimagi Command API, which primarily involves streaming responses. Its `handleRequest` method is tailored to process status and root requests, but its main function is `requestCommand`, which handles POST requests to the command API. This method is designed to read and process a continuous stream of messages from the server, parsing each line as a JSON message and optionally invoking a `messageCallback` for real-time processing. It also constructs a `CommandResponse` object to aggregate all messages received during the stream.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A client application initiates a request through the Zimagi JavaScript SDK.
   2.  The SDK determines the appropriate transport (e.g., `DataHTTPTransport` for data operations, `CommandHTTPTransport` for command execution).
   3.  The chosen transport's `request` method (inherited from `BaseTransport`) is called, which sets up common headers and parameters.
   4.  The `request` method then delegates to the transport-specific `handleRequest` method.
   5.  `handleRequest` in `DataHTTPTransport` directs the request to `requestPage` for GET operations or `updateData` for modifications.
   6.  `handleRequest` in `CommandHTTPTransport` directs the request to `requestPage` for status/root or `requestCommand` for streaming command execution.
   7.  The `_request` method (in `BaseTransport`) performs the actual `fetch` call, handling encryption/decryption and authentication.
   8.  For `DataHTTPTransport`, `decodeMessage` processes the final response.
   9.  For `CommandHTTPTransport`, `requestCommand` continuously reads and processes streaming chunks, decoding each message individually.

**External Interfaces**
   *   **Zimagi Backend APIs:** All transports communicate directly with the Zimagi Command API and Data API endpoints over HTTP.
   *   **Client Cipher:** The `BaseTransport` and its subclasses interact with a client-provided cipher (if available) for encrypting request parameters and decrypting response bodies, ensuring secure communication.
   *   **Client Authentication:** The `BaseTransport` integrates with the client's authentication mechanism to apply necessary authentication headers to outgoing requests.
   *   **`fetch` API:** The underlying network communication is handled by the standard JavaScript `fetch` API.
