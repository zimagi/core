=====================================================
README for Directory: sdk/python/zimagi/command
=====================================================

Directory Overview
------------------

**Purpose**
   This directory provides the core client-side command-line interface (CLI) and API interaction logic for the Zimagi platform. It defines the structure for commands, messages, and responses, and handles the communication with the Zimagi server.

**Key Functionality**
   *   Defines the schema for Zimagi commands and responses.
   *   Encodes and decodes messages for communication with the Zimagi server.
   *   Manages the client-side execution of Zimagi commands.
   *   Handles the transport layer for sending requests and receiving responses from the Zimagi API.

Dependencies
-------------------------

This directory primarily relies on standard Python libraries and internal Zimagi utility modules.
*   `urllib`: Used for URL parsing and opening URLs in `codecs.py` and `messages.py`.
*   `logging`: Standard Python logging library used across various modules for debugging and information.
*   `re`: Regular expression module used for path normalization in `client.py`.
*   `copy`: Used for deep copying client instances in `client.py`.
*   `collections.OrderedDict`: Used in `schema.py` to maintain order of command definitions.
*   `oyaml`: A YAML library used in `messages.py` for dumping data.
*   `magic`: Used in `messages.py` for determining file mimetypes.
*   `base64`: Used in `messages.py` for encoding/decoding image data.
*   `zimagi.utility`: Provides general utility functions like JSON handling, value normalization, and data formatting.
*   `zimagi.exceptions`: Defines custom exception types for Zimagi.
*   `zimagi.settings`: Provides global configuration settings for the Zimagi client.
*   `zimagi.client`: The base API client class that `client.py` extends.
*   `zimagi.transports`: Provides base transport classes for HTTP communication.

File Structure and Descriptions
-------------------------------

**sdk/python/zimagi/command/schema.py**
     **Role:** Defines the data structures and schema for Zimagi commands, routers, actions, fields, and responses.
     **Detailed Description:** This file contains classes like `Root`, `Router`, `Action`, `Field`, `Error`, `Object`, and `Array`, which represent the hierarchical structure of Zimagi's command-line interface and API. These classes are used to parse and represent the server's command definitions, allowing the client to understand available commands, their arguments, and expected responses. It includes mixins for sorting and indexing commands.

**sdk/python/zimagi/command/codecs.py**
     **Role:** Handles the encoding and decoding of Zimagi-specific JSON data.
     **Detailed Description:** This file provides the `ZimagiJSONCodec` class, which is responsible for converting raw byte strings received from the server into structured Python objects based on the schema defined in `schema.py`. It also includes helper functions for safely extracting different data types (boolean, string, number, list, dict) from parsed JSON. This codec ensures that the client can correctly interpret the server's responses.

**sdk/python/zimagi/command/messages.py**
     **Role:** Defines various message types used for communication between the Zimagi client and server.
     **Detailed Description:** This file contains base `Message` class and its subclasses such as `StatusMessage`, `DataMessage`, `InfoMessage`, `NoticeMessage`, `SuccessMessage`, `WarningMessage`, `ErrorMessage`, `TableMessage`, and `ImageMessage`. These classes encapsulate different types of information or events that can be sent from the server to the client, including command output, errors, and status updates. Each message type has methods for rendering, formatting, and displaying its content.

**sdk/python/zimagi/command/response.py**
     **Role:** Manages and aggregates messages received from the Zimagi server during command execution.
     **Detailed Description:** The `CommandResponse` class in this file acts as a container for all messages (including status, data, and errors) returned by a Zimagi command execution. It provides methods to add messages, check for errors, retrieve specific named data, and format error messages for display. This class centralizes the handling of server responses, making it easier to process and react to command outcomes.

**sdk/python/zimagi/command/transports.py**
     **Role:** Implements the HTTP transport layer for Zimagi command communication.
     **Detailed Description:** This file contains the `CommandHTTPTransport` class, which extends a base transport class to handle HTTP requests and responses specifically for Zimagi commands. It manages the streaming of responses from the server, decrypts messages if encryption is enabled, and passes them to a message callback for processing. It also handles error responses from the server, raising appropriate exceptions.

**sdk/python/zimagi/command/__init__.py**
     **Role:** Initializes the `command` package, making its core components accessible.
     **Detailed Description:** This file serves as the package initializer. It imports key classes and functions from `client.py`, `messages.py`, and `response.py` into the `zimagi.command` namespace. This allows other modules to easily access these components using a simplified import statement, contributing to a cleaner and more organized codebase.

**sdk/python/zimagi/command/client.py**
     **Role:** Provides the main client interface for interacting with the Zimagi command API.
     **Detailed Description:** The `Client` class in this file is the primary entry point for developers to programmatically interact with the Zimagi server. It manages the connection, handles command execution, validates command options against the server's schema, and processes responses. It also includes methods for common operations like extending modules, running tasks, and managing profiles. This client abstracts away the underlying HTTP communication and message handling, offering a high-level API.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A developer initializes the `Client` from `sdk/python/zimagi/command/client.py`, optionally providing a message callback.
   2.  During initialization, the `Client` fetches the command `schema` from the Zimagi server and populates its internal command and action registries.
   3.  When `client.execute()` is called with a command name and options, the `Client` first normalizes the command name and looks up the corresponding `Action` in its schema.
   4.  The `Client` then validates the provided options against the `Field` definitions of the `Action`.
   5.  The `Client` constructs an HTTP request and delegates its execution to the `CommandHTTPTransport` in `sdk/python/zimagi/command/transports.py`.
   6.  The `CommandHTTPTransport` sends the request to the Zimagi server and streams the response.
   7.  Each line of the streamed response is decoded by `ZimagiJSONCodec` from `sdk/python/zimagi/command/codecs.py` into a `Message` object (e.g., `DataMessage`, `ErrorMessage`) from `sdk/python/zimagi/command/messages.py`.
   8.  These `Message` objects are then added to a `CommandResponse` object from `sdk/python/zimagi/command/response.py`.
   9.  If a message callback was provided to the `Client`, each `Message` is passed to this callback for real-time processing.
   10. Finally, the `CommandResponse` object, containing all aggregated messages and status, is returned to the caller of `client.execute()`.

**External Interfaces**
   *   **Zimagi Server API:** The code in this directory, particularly `transports.py` and `client.py`, communicates directly with the Zimagi server's command API over HTTP/HTTPS. This involves sending command execution requests and receiving streamed responses.
   *   **Encryption Module:** The `client.py` and `transports.py` modules interact with the `zimagi.encryption` module (not in this directory) for encrypting outgoing requests and decrypting incoming responses, ensuring secure communication.
   *   **Utility Module:** Various functions from `zimagi.utility` (outside this directory) are used for tasks such as JSON serialization/deserialization, value normalization, and data formatting.
   *   **Exceptions Module:** Custom exceptions defined in `zimagi.exceptions` are raised by `client.py` and `transports.py` to signal specific error conditions during API interaction.
