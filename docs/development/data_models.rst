Developing Data Models
======================

Data models are the foundation of Zimagi, defining the structure, behavior, and relationships of all data entities within the platform. This section guides you through developing new data models.

Overview
--------
Zimagi uses Django's ORM for data persistence, with dynamic model generation based on YAML specifications. This allows for flexible and evolving data schemas.

Data Model Directory Structure (`app/data`)
-------------------------------------------
The `app/data/` directory is the central repository for all application data models:

*   **`app/data/base`**: Foundational base classes for data models (e.g., `id_resource`, `name_resource`).
*   **`app/data/cache`**: Data models and migrations for caching mechanisms.
*   **`app/data/notification`**: Data models and migrations for the notification system.
*   **`app/data/memory`**: Data models and migrations for conversational memory.
*   **`app/data/group`**: Data models, caching, and migrations for user groups.
*   **`app/data/config`**: Data models and migrations for configuration settings.
*   **`app/data/host`**: Data models and migrations for host-related information.
*   **`app/data/schedule`**: Data models and migrations for scheduled tasks.
*   **`app/data/log`**: Data models and migrations for log data.
*   **`app/data/module`**: Data models and migrations for application modules.
*   **`app/data/state`**: Data models and migrations for application state.
*   **`app/data/user`**: Data models and migrations for user management.
*   **`app/data/mixins`**: Reusable mixin classes for Django models (provider integration, group access, resource timestamps).
*   **`app/data/dataset`**: Data models and migrations for datasets.
*   **`app/data/scaling_event`**: Data models and migrations for scaling events.

Core Modeling System (`app/systems/models`)
-------------------------------------------
The `app/systems/models/` directory provides the robust and extensible framework for model management:

*   **`app/systems/models/parsers`**: Defines parsing functionalities for filter expressions, field assignments, etc.
*   **`app/systems/models/mixins`**: Mixin classes to extend model facade functionality (fields, relations, query, update).
*   **`app/systems/models/fields.py`**: Custom Django model fields (e.g., `DataField`, `ListField`, `DictionaryField`).
*   **`app/systems/models/errors.py`**: Custom exception classes for model-related errors.
*   **`app/systems/models/aggregates.py`**: Custom Django ORM aggregate functions.
*   **`app/systems/models/template.py.tpl`**: Jinja2 template for generating dynamic model files.
*   **`app/systems/models/index.py`**: Manages dynamic generation, registration, and retrieval of models and facades.
*   **`app/systems/models/facade.py`**: Implements the core `ModelFacade` class.
*   **`app/systems/models/dataset.py`**: Tools for constructing and manipulating complex datasets.
*   **`app/systems/models/base.py`**: Foundational abstract base classes for all Django models.
*   **`app/systems/models/overrides.py`**: Overrides for Django's default model behaviors.

Creating a New Data Model
-------------------------
1.  **Choose a Category**: Decide which existing data category your new model belongs to, or create a new subdirectory in `app/data/`.
2.  **Define Specification**: Create a YAML file in `app/spec/data/` (e.g., `app/spec/data/my_model.yml`) to define your model's schema. This is the primary way to create new models.

    .. code-block:: yaml

        my_model:
            name: my_model
            plural: my_models
            base: name_resource # or id_resource
            mixins:
                - provider
                - group
            fields:
                my_string_field:
                    type: @django.CharField
                    max_length: 255
                    help: A sample string field.
                my_integer_field:
                    type: @django.IntegerField
                    default: 0
                    help: A sample integer field.
            roles:
                view:
                    - admin
                edit:
                    - admin

3.  **Generate Model Files**: The Zimagi framework will dynamically generate the Python model files and database migrations based on this specification. You might need to run a command to trigger this generation and apply migrations:

    .. code-block:: bash

        zimagi build

4.  **Interact with the Model**: Once generated and migrated, you can interact with your new model via the Zimagi Data API or through commands.

    .. code-block:: bash

        zimagi data save my_model my-instance --my-string-field "Hello" --my-integer-field 123

This declarative approach simplifies data model development and ensures consistency across the platform.
