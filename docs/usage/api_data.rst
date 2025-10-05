Data API
========

The Zimagi Data API provides a robust and extensible interface for interacting with the platform's data models, enabling CRUD operations, advanced querying, and data retrieval in various formats.

Overview
--------
The Data API allows external systems and client applications to programmatically manage data stored within Zimagi. It supports secure access, filtering, ordering, and pagination.

API Endpoint
------------
The Data API typically runs on `localhost:5323` by default, but this can be configured via environment variables (`ZIMAGI_DATA_HOST`, `ZIMAGI_DATA_PORT`).

Authentication
--------------
Requests to the Data API require token-based authentication, similar to the Command API.

*   **Python SDK**:
    .. code-block:: python

        from zimagi import DataClient
        client = DataClient(user="admin", token="your_admin_token")
        client.initialize()

*   **JavaScript SDK**:
    .. code-block:: javascript

        import { DataClient } from 'zimagi';
        const client = new DataClient({ user: 'admin', token: 'your_admin_token' });
        await client.initialize();

CRUD Operations
---------------
The Data API supports standard Create, Retrieve, Update, and Delete (CRUD) operations for all defined data models.

*   **Create**:
    *   Python: `client.create("user", {"name": "new_user", "email": "new@example.com"})`
    *   JavaScript: `await client.create('user', { name: 'new_user', email: 'new@example.com' });`

*   **Retrieve (Get by Key)**:
    *   Python: `user = client.get("user", "new_user")`
    *   JavaScript: `const user = await client.get('user', 'new_user');`

*   **List (Query)**:
    *   Python: `users = client.list("user", {"email__icontains": "example.com"})`
    *   JavaScript: `const users = await client.list('user', { 'email__icontains': 'example.com' });`

*   **Update**:
    *   Python: `client.update("user", "new_user", {"first_name": "New"})`
    *   JavaScript: `await client.update('user', 'new_user', { first_name: 'New' });`

*   **Delete**:
    *   Python: `client.delete("user", "new_user")`
    *   JavaScript: `await client.delete('user', 'new_user');`

Advanced Querying
-----------------
The Data API supports advanced filtering, ordering, and pagination.

*   **Filtering**: Use Django-style query lookups (e.g., `field__lookup=value`).
*   **Ordering**: Specify fields for sorting (e.g., `order=["-created"]`).
*   **Pagination**: Control result set size and navigation.

Data Formats
------------
Data can be retrieved in various formats, including JSON and CSV.

*   **JSON**: `client.json("user")`
*   **CSV**: `client.csv("user")`

API Schema
----------
The Data API provides an OpenAPI-compatible schema that describes all available data models, their fields, and relationships.

*   **Python SDK**: `client.get_schema()`
*   **JavaScript SDK**: `client.getSchema()`

Core API Components (`app/systems/api/data`)
--------------------------------------------
*   **`app/systems/api/data/filter`**: Logic for advanced filtering.
*   **`app/systems/api/data/fields.py`**: Custom serializer fields.
*   **`app/systems/api/data/schema.py`**: OpenAPI schema generation.
*   **`app/systems/api/data/pagination.py`**: Custom pagination classes.
*   **`app/systems/api/data/response.py`**: Encrypted response class.
*   **`app/systems/api/data/auth.py`**: Authentication and authorization.
*   **`app/systems/api/data/routers.py`**: Manages API routing.
*   **`app/systems/api/data/filters.py`**: Comprehensive filter classes.
*   **`app/systems/api/data/serializers.py`**: Serializers for data conversion.
*   **`app/systems/api/data/views.py`**: Core logic for handling API requests.
*   **`app/systems/api/data/parsers.py`**: Custom parsers for encrypted JSON.
*   **`app/systems/api/data/renderers.py`**: Custom renderers for OpenAPI schema.
