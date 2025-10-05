Module Management
=================

Zimagi's modular architecture allows for dynamic loading and management of various components. This section details how to manage modules within the platform.

Overview
--------
Modules are fundamental building blocks that encapsulate functionalities, configurations, and data models. They can be sourced from Git repositories, GitHub, or local file systems.

Key Module Management Features
------------------------------
*   **Module Definition**: Define module metadata, dependencies, and configurations.
*   **Version Control Integration**: Manage modules from Git and GitHub repositories.
*   **Local Module Support**: Use and manage modules directly from the local filesystem.
*   **Lifecycle Management**: Install, add, initialize, and create modules.
*   **Profile Execution**: Run and destroy module-specific profiles and tasks.

Module Directory Structure (`app/data/module`)
----------------------------------------------
*   **`app/data/module/models.py`**: Defines the `Module` Django model and its facade.
*   **`app/data/module/migrations`**: Database migration files for the `Module` model.

Module Command Implementations (`app/commands/module`)
------------------------------------------------------
*   **`app/commands/module/install.py`**: Installs module-specific requirements and scripts.
*   **`app/commands/module/add.py`**: Adds a new module to the Zimagi platform.
*   **`app/commands/module/init.py`**: Initializes a module's resources and data.
*   **`app/commands/module/create.py`**: Creates a new module based on a template.

Module Provider Plugins (`app/plugins/module`)
----------------------------------------------
*   **`app/plugins/module/github.py`**: Module provider for GitHub repositories.
*   **`app/plugins/module/local.py`**: Module provider for local file system modules.
*   **`app/plugins/module/core.py`**: Module provider for the core Zimagi module.
*   **`app/plugins/module/git.py`**: Generic Git module provider.
*   **`app/plugins/module/base.py`**: Abstract base class for all module providers.

Using Module Management
-----------------------

1.  **Creating a New Module**: Use the `zimagi module create` command.

    .. code-block:: bash

        zimagi module create my-new-feature --template standard

    This command uses templates from `app/templates/module/standard` to scaffold your new module.

2.  **Adding an Existing Module (e.g., from Git/GitHub)**:

    .. code-block:: bash

        zimagi module add my-remote-module --provider git --remote "git@github.com:user/repo.git" --reference main

3.  **Installing Module Requirements**:

    .. code-block:: bash

        zimagi module install my-new-feature

4.  **Running Module Profiles**: Execute predefined workflows or configurations within a module.

    .. code-block:: bash

        zimagi run my-new-feature my-profile

5.  **Destroying Module Profiles**: Clean up resources associated with a module profile.

    .. code-block:: bash

        zimagi destroy my-new-feature my-profile

Module management is crucial for extending Zimagi's capabilities and integrating custom functionalities.
