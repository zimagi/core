Python SDK
==========

The Zimagi Python SDK provides a foundational library for interacting with the Zimagi platform from Python applications and scripts.

Overview
--------
The SDK abstracts away the complexities of API communication, encryption, and data parsing, offering a streamlined interface for developers. It includes core client functionalities, communication protocols, and utility functions.

Key Functionality
-----------------
*   **API Client Base Classes**: Handles authentication, encryption, and request/response processing.
*   **Secure Communication**: Manages secure communication with Zimagi services.
*   **Data Serialization/Deserialization**: Robust mechanisms for various media types (JSON, OpenAPI, CSV).
*   **Utility Functions**: Data manipulation, error handling, and parallel processing.
*   **Core Exceptions**: Defines Zimagi-specific error types.
*   **Configuration Settings**: Global configuration for the Python SDK.

Directory Structure (`sdk/python`)
----------------------------------
*   **`sdk/python/bin`**: Contains executable scripts, primarily the `zimagi` CLI.
*   **`sdk/python/zimagi`**: Core Zimagi Python SDK modules.
    *   **`sdk/python/zimagi/command`**: Client-side implementation for the Command API.
    *   **`sdk/python/zimagi/data`**: Client-side implementation for the Data API.
    *   **`sdk/python/zimagi/codecs.py`**: Generic data encoding/decoding.
    *   **`sdk/python/zimagi/utility.py`**: General-purpose utility functions.
    *   **`sdk/python/zimagi/collection.py`**: Flexible data structures for attribute access.
    *   **`sdk/python/zimagi/datetime.py`**: Date and time utilities.
    *   **`sdk/python/zimagi/settings.py`**: Global configuration settings.
    *   **`sdk/python/zimagi/exceptions.py`**: Custom exception types.
    *   **`sdk/python/zimagi/auth.py`**: Authentication mechanisms.
    *   **`sdk/python/zimagi/transports.py`**: Base classes for HTTP communication.
    *   **`sdk/python/zimagi/client.py`**: Abstract base class for all Zimagi API clients.
    *   **`sdk/python/zimagi/encryption.py`**: Cryptographic utilities.
    *   **`sdk/python/zimagi/parallel.py`**: Utilities for parallel task execution.
*   **`sdk/python/setup.py`**: Package metadata and build instructions.
*   **`sdk/python/requirements.txt`**: Python package dependencies.
*   **`sdk/python/deploy.sh`**: Script for deploying to PyPI.

Using the Python SDK
--------------------

1.  **Installation**: The SDK is installed as part of the main Zimagi setup. You can also install it via pip:

    .. code-block:: bash

        pip install zimagi

2.  **Command Client**: Interact with the Zimagi Command API.

    .. code-block:: python

        from zimagi import CommandClient

        client = CommandClient(
            host="localhost",
            port=5123,
            user="admin",
            token="your_admin_token",
            # ... other options
        )
        client.initialize()
        response = client.execute("platform info")
        print(response.messages)

3.  **Data Client**: Interact with the Zimagi Data API.

    .. code-block:: python

        from zimagi import DataClient

        client = DataClient(
            host="localhost",
            port=5323,
            user="admin",
            token="your_admin_token",
            # ... other options
        )
        client.initialize()
        users = client.list("user")
        for user in users:
            print(user.name)

For more detailed examples and API reference, refer to the specific SDK documentation within the `sdk/python/zimagi` directory.
