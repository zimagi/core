Data Management
===============

Zimagi provides comprehensive data management capabilities, including defining data models, handling migrations, advanced querying, and supporting various data formats.

Overview
--------
Data models are the foundation of Zimagi, defining the structure, behavior, and relationships of all data entities. The platform uses Django's ORM and dynamic schema generation.

Key Data Management Features
----------------------------
*   **Data Model Definition**: Define schemas for various data entities (users, configurations, logs, schedules, etc.).
*   **Database Migrations**: Manage schema evolution over time, ensuring compatibility.
*   **Advanced Querying**: Filter, order, and paginate data with powerful query capabilities.
*   **Data Formats**: Support for JSON, YAML, and CSV for serialization/deserialization.
*   **Caching**: Optimize performance by storing and retrieving frequently accessed data.
*   **Data Integrity**: Enforce data integrity and business rules through validation.

Data Model Directory Structure (`app/data`)
-------------------------------------------
*   **`app/data/base`**: Foundational base classes for data models.
*   **`app/data/cache`**: Data models for caching mechanisms.
*   **`app/data/notification`**: Data models for the notification system.
*   **`app/data/memory`**: Data models for conversational memory.
*   **`app/data/group`**: Data models for user groups.
*   **`app/data/config`**: Data models for configuration settings.
*   **`app/data/host`**: Data models for host-related information.
*   **`app/data/schedule`**: Data models for scheduled tasks.
*   **`app/data/log`**: Data models for log data.
*   **`app/data/module`**: Data models for application modules.
*   **`app/data/state`**: Data models for application state.
*   **`app/data/user`**: Data models for user management.
*   **`app/data/mixins`**: Reusable mixin classes for Django models.
*   **`app/data/dataset`**: Data models for datasets.
*   **`app/data/scaling_event`**: Data models for scaling events.

Core Modeling System (`app/systems/models`)
-------------------------------------------
*   **`app/systems/models/index.py`**: Manages dynamic generation, registration, and retrieval of models and facades.
*   **`app/systems/models/facade.py`**: Implements the core `ModelFacade` class for interacting with models.
*   **`app/systems/models/dataset.py`**: Tools for constructing and manipulating complex datasets.
*   **`app/systems/models/parsers`**: Defines parsing functionalities for filter expressions, field assignments, etc.

Using Data Management Features
------------------------------

1.  **Defining Data Models**: Data models are defined declaratively using YAML files in `app/spec/data/`.

    .. code-block:: yaml

        my_custom_data:
            name: my_custom_data
            fields:
                name:
                    type: @django.CharField
                    max_length: 100
                value:
                    type: @zimagi.DataField

2.  **Interacting via CLI**: Use `zimagi data` commands or resource-specific commands.

    .. code-block:: bash

        zimagi config save my_app_setting --value "production" --type string
        zimagi user list

3.  **Interacting via Data API**: Programmatically manage data using the Data API. Refer to :doc:`api_data`.

4.  **Database Snapshots**: Backup and restore your database.

    .. code-block:: bash

        zimagi db backup my-backup-name
        zimagi db restore my-backup-name

5.  **Caching**: Clear application caches.

    .. code-block:: bash

        zimagi cache clear

For detailed information on specific data models, refer to their respective `README.rst` files within `app/data/`.
