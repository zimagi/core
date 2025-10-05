JavaScript SDK
==============

The Zimagi JavaScript SDK provides a comprehensive set of functionalities for interacting with Zimagi backend services from client-side JavaScript applications.

Overview
--------
This SDK is designed for JavaScript environments (Node.js or modern web browsers) and offers tools for command execution, data management, authentication, encryption, caching, and performance monitoring.

Key Functionality
-----------------
*   **API Client Base Classes**: Provides base classes and specific client implementations for Command and Data API interactions.
*   **Secure Communication**: Manages authentication and encryption for secure communication.
*   **Message System**: Robust system for handling various response types (status, data, info, error).
*   **Codec System**: Flexible encoding/decoding for different data formats (JSON, CSV, OpenAPI JSON, Zimagi JSON).
*   **Caching & Performance**: Implements caching and performance monitoring for optimized client operations.

Directory Structure (`sdk/javascript`)
--------------------------------------
*   **`sdk/javascript/src`**: Main entry point and core implementation.
    *   **`sdk/javascript/src/command`**: Handles command responses.
    *   **`sdk/javascript/src/messages`**: Defines the message system.
    *   **`sdk/javascript/src/codecs`**: Codec implementations for various data formats.
    *   **`sdk/javascript/src/client`**: Core client-side implementations (`BaseAPIClient`, `CommandClient`, `DataClient`).
    *   **`sdk/javascript/src/transports`**: HTTP transport implementations.
    *   **`sdk/javascript/src/schema`**: Defines data structures and schema classes.
    *   **`sdk/javascript/src/exceptions.ts`**: Custom exception classes.
    *   **`sdk/javascript/src/performance.ts`**: Performance monitoring utilities.
    *   **`sdk/javascript/src/encryption.ts`**: Encryption and decryption utilities.
    *   **`sdk/javascript/src/auth.ts`**: Authentication system.
    *   **`sdk/javascript/src/cache.ts`**: In-memory caching system.
    *   **`sdk/javascript/src/utility.ts`**: General-purpose utility functions.
*   **`sdk/javascript/tests`**: Comprehensive testing suite.
*   **`sdk/javascript/package.json`**: Project metadata and dependencies.
*   **`sdk/javascript/deploy.sh`**: Script for deploying to npm registry.

Using the JavaScript SDK
------------------------

1.  **Installation**: Install the SDK via npm:

    .. code-block:: bash

        npm install zimagi

2.  **Command Client**: Interact with the Zimagi Command API.

    .. code-block:: javascript

        import { CommandClient } from 'zimagi';

        const client = new CommandClient({
            host: 'localhost',
            port: 5123,
            user: 'admin',
            token: 'your_admin_token',
        });
        await client.initialize();
        const response = await client.execute('platform info');
        console.log(response.messages);

3.  **Data Client**: Interact with the Zimagi Data API.

    .. code-block:: javascript

        import { DataClient } from 'zimagi';

        const client = new DataClient({
            host: 'localhost',
            port: 5323,
            user: 'admin',
            token: 'your_admin_token',
        });
        await client.initialize();
        const users = await client.list('user');
        users.forEach(user => console.log(user.name));

For more detailed examples and API reference, refer to the specific SDK documentation within the `sdk/javascript/src` directory.
