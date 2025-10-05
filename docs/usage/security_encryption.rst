Security & Encryption
=====================

Zimagi prioritizes security through robust authentication, authorization, and encryption mechanisms, ensuring the confidentiality and integrity of sensitive data and communications.

Overview
--------
The platform provides end-to-end encryption for API communication, user-specific key management, and role-based access control.

Key Security Features
---------------------
*   **API Token Authentication**: Secure access to Command and Data APIs using tokens.
*   **Role-Based Access Control (RBAC)**: Granular control over user permissions for commands and data models.
*   **End-to-End Encryption**: Encrypts API requests and responses, especially for sensitive data.
*   **User-Specific Encryption Keys**: Data can be encrypted with keys unique to individual users.
*   **Secret Management**: Template for managing sensitive environment variables and secrets.
*   **Distributed Locking**: Prevents race conditions and ensures data integrity in a distributed environment.

Encryption System (`app/systems/encryption`)
--------------------------------------------
*   **`app/systems/encryption/cipher.py`**: Defines the core `Cipher` class for managing encryption functionality.

Encryption Plugins (`app/plugins/encryption`)
---------------------------------------------
*   **`app/plugins/encryption/aes256.py`**: Implements AES256 symmetric encryption/decryption.
*   **`app/plugins/encryption/aes256_user.py`**: Extends AES256 for user-specific encryption keys.
*   **`app/plugins/encryption/base.py`**: Abstract base class for all encryption plugins.

User Management (`app/data/user`)
----------------------------------
*   **`app/data/user/models.py`**: Defines the `User` model, handling authentication and token generation.
*   **`app/commands/user/rotate.py`**: CLI command for rotating a user's authentication token.

Environment Variables (`env/`)
------------------------------
*   **`env/secret.example`**: Template for storing sensitive information like `ZIMAGI_SECRET_KEY`, API keys, and database passwords.

Using Security & Encryption Features
------------------------------------

1.  **API Authentication**: When initializing SDK clients, provide your user credentials.

    *   Python: `CommandClient(user="admin", token="your_admin_token")`
    *   JavaScript: `new CommandClient({ user: 'admin', token: 'your_admin_token' })`

2.  **Enabling API Encryption**: Configure API encryption via environment variables.

    .. code-block:: bash

        export ZIMAGI_API_ENCRYPT_COMMAND=true
        export ZIMAGI_API_ENCRYPT_DATA=true

    Or use the `api.encrypted` configuration profile when starting Zimagi:

    .. code-block:: bash

        source start standard local api.encrypted

3.  **Rotating User Tokens**: For enhanced security, regularly rotate user tokens.

    .. code-block:: bash

        zimagi user rotate admin

4.  **Role-Based Access Control**: Define roles and assign them to users/groups in `app/spec/roles.yml` and `app/spec/data/[model].yml`.

    Example from `app/spec/data/config.yml`:

    .. code-block:: yaml

        roles:
            view:
                - admin
            edit:
                - admin

5.  **Distributed Locking**: The `app/utility/mutex.py` module provides Redis-backed distributed locks to ensure exclusive execution of critical sections, preventing data corruption in concurrent operations.

By leveraging these features, Zimagi helps you build secure and compliant AI-driven applications.
