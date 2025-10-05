=====================================================
README for Directory: sdk/python/zimagi/data
=====================================================

Directory Overview
------------------

**Purpose**
   This directory provides the Python client-side implementation for interacting with the Zimagi Data API. It encapsulates the logic for encoding and decoding various data formats, handling network communication, and providing a structured interface for data operations. Its primary role is to enable other Python components within the Zimagi ecosystem, or external Python applications, to seamlessly access and manipulate data managed by the Zimagi platform.

**Key Functionality**
   *   Serialization and deserialization of data to and from various formats (e.g., OpenAPI JSON, CSV, standard JSON).
   *   Management of HTTP communication with the Zimagi Data API, including request handling, error processing, and encryption.
   *   Provision of a high-level client interface for common data operations such as creating, reading, updating, deleting, listing, and querying data.
   *   Retrieval and caching of API schema information to facilitate dynamic interaction with data types.

Dependencies
-------------------------

This directory relies on several external and internal Python libraries:
*   ``pandas``: Used for efficient handling and manipulation of tabular data, particularly for CSV decoding.
*   ``requests``: (Implicitly used by underlying transport mechanisms) For making HTTP requests to the Zimagi Data API.
*   ``zimagi.client``: Provides the base API client functionality, including common request handling and decoder management.
*   ``zimagi.codecs``: Offers shared codec implementations, specifically for JSON.
*   ``zimagi.exceptions``: Defines custom exception types for API-related errors.
*   ``zimagi.parallel``: Utilized for parallel execution of tasks, such as fetching multiple schema paths.
*   ``zimagi.settings``: Provides default configuration values for client initialization.
*   ``zimagi.utility``: Offers general utility functions for data manipulation, JSON handling, and API call wrapping.

File Structure and Descriptions
-------------------------------

**sdk/python/zimagi/data/codecs.py**
     **Role:** Defines data encoding and decoding strategies for various media types.
     **Detailed Description:** This file contains classes responsible for converting raw byte strings into Python data structures and vice-versa, specifically for data received from or sent to the Zimagi Data API. It includes `OpenAPIJSONCodec` for handling OpenAPI specification JSON and `CSVCodec` for processing CSV formatted data. These codecs ensure that the client can correctly interpret different data representations provided by the API.

**sdk/python/zimagi/data/transports.py**
     **Role:** Manages the HTTP communication layer for the Zimagi Data API.
     **Detailed Description:** This file implements the `DataHTTPTransport` class, which extends a base transport class to handle the specifics of communicating with the Zimagi Data API. It defines how HTTP requests are constructed, sent, and how responses are processed, including error handling and decryption if applicable. It differentiates between various API endpoints (e.g., status, schema, data operations) to apply appropriate request parameters and encryption settings.

**sdk/python/zimagi/data/__init__.py**
     **Role:** Serves as the package initializer, exposing key components.
     **Detailed Description:** This file is the entry point for the `zimagi.data` Python package. Its primary function is to make the `Client` class directly importable from the `zimagi.data` package, simplifying access for developers who wish to use the Zimagi Data API client.

**sdk/python/zimagi/data/client.py**
     **Role:** Provides the main client interface for interacting with the Zimagi Data API.
     **Detailed Description:** This file defines the `Client` class, which is the central component for programmatic access to the Zimagi Data API. It initializes the API client with appropriate decoders and a data-specific transport layer. The `Client` class offers methods for retrieving API schema, performing CRUD (Create, Read, Update, Delete) operations on data types, listing data, and executing specialized data queries like `json`, `csv`, `values`, and `count`. It also manages data type metadata such as ID, key, system, unique, dynamic, atomic, scope, relation, and reverse fields.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A Python application instantiates `Client` from `sdk/python/zimagi/data/client.py`.
   2.  During initialization, the `Client` sets up `DataHTTPTransport` (from `sdk/python/zimagi/data/transports.py`) and registers various codecs (from `sdk/python/zimagi/data/codecs.py` and shared codecs).
   3.  The `Client` immediately fetches the API schema using its `_request` method, which delegates to the `DataHTTPTransport` to perform the actual HTTP call.
   4.  When a data operation method (e.g., `create`, `get`, `list`) is called on the `Client` instance, it constructs the appropriate URL and parameters.
   5.  The `Client` then calls its internal `_request` method, which in turn uses the `DataHTTPTransport` to send the request to the Zimagi Data API.
   6.  The `DataHTTPTransport` handles the low-level HTTP communication, including encryption/decryption, and receives the raw response.
   7.  The `DataHTTPTransport` then uses the registered codecs (e.g., `OpenAPIJSONCodec`, `CSVCodec`) to decode the raw response into a usable Python data structure.
   8.  Finally, the decoded data is returned to the calling method in the `Client`, which then returns it to the application.

**External Interfaces**
   The code in this directory primarily interacts with the **Zimagi Data API** over HTTP. This API is an external service that manages and exposes data. The client communicates with this API to perform all data-related operations. It also implicitly relies on the underlying network infrastructure to establish connections and transmit data.
