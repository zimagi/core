Configuration Management
========================

Zimagi provides robust mechanisms for managing application-wide settings and configurations, ensuring consistent behavior across different services and deployment environments.

Overview
--------
Configuration settings can be dynamic, environment-specific, and managed through data models and environment variables.

Key Configuration Management Features
-------------------------------------
*   **Centralized Settings**: Manage core application parameters, directories, and naming conventions.
*   **Database-backed Configuration**: Store configuration values persistently in the database.
*   **Environment Variable Integration**: Override settings using environment variables.
*   **Dynamic Loading**: Configurations are dynamically loaded and applied.
*   **Type Enforcement**: Ensure configuration values conform to expected data types.

Configuration Data Model (`app/data/config`)
--------------------------------------------
*   **`app/data/config/models.py`**: Defines the `Config` Django model and its associated facade.
*   **`app/data/config/migrations`**: Database migration scripts for the `Config` model.

Configuration Commands (`app/commands/config`)
----------------------------------------------
*   **`app/commands/config.yml` (spec)**: Defines commands for managing configuration settings.

Configuration Mixins (`app/commands/mixins/config.py`)
------------------------------------------------------
*   **`app/commands/mixins/config.py`**: Provides a simple method for retrieving configuration values.

Core Settings (`app/settings`)
------------------------------
*   **`app/settings/core.py`**: Establishes fundamental and universal settings.
*   **`app/settings/full.py`**: Defines comprehensive settings for a full Zimagi service instance.
*   **`app/settings/install.py`**: Settings related to installation and initial setup.
*   **`app/settings/client.py`**: Settings tailored for client-side operations.
*   **`app/settings/config.py`**: Utility class for robust retrieval of configuration values.

Using Configuration Management
------------------------------

1.  **Saving a Configuration Setting**: Use the `zimagi config save` command.

    .. code-block:: bash

        zimagi config save my_feature_flag --value "true" --type boolean --group my-team

    This saves a boolean configuration named `my_feature_flag` associated with `my-team` group.

2.  **Retrieving a Configuration Setting**:

    .. code-block:: bash

        zimagi config get my_feature_flag

3.  **Listing All Configurations**:

    .. code-block:: bash

        zimagi config list

4.  **Overriding with Environment Variables**: You can override any setting by defining an environment variable with the `ZIMAGI_` prefix.

    .. code-block:: bash

        export ZIMAGI_DEBUG=true
        zimagi platform info # Debug mode will be active

5.  **Dynamic Value Parsing**: Configuration values can include dynamic expressions that are parsed at runtime. Refer to :doc:`development/plugins` for details on the `parser` plugin.

Effective configuration management is vital for adapting Zimagi to various operational environments and requirements.
