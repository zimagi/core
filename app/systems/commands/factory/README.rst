=====================================================
README for Directory: app/systems/commands/factory
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is responsible for dynamically generating command classes for various resource operations within the Zimagi system. It acts as a factory for creating standardized command structures, ensuring consistency and reducing boilerplate code for common actions like listing, getting, saving, removing, and clearing resources.

**Key Functionality**
   *   Dynamic command class generation for CRUD-like operations.
   *   Standardization of command parsing, execution, and permission handling.
   *   Facilitation of resource management through a consistent command-line interface.


Dependencies
-------------------------

This directory primarily relies on internal Zimagi utilities and Django settings.
*   `utility.data`: Provides data manipulation utilities like `ensure_list` for handling iterable data.
*   `utility.python`: Offers utilities like `create_class` for dynamic class creation.
*   `settings.roles`: Used for defining and checking user roles and permissions for command access.


File Structure and Descriptions
-------------------------------

**app/systems/commands/factory/operations**
     **Role:** This subdirectory contains individual modules, each defining a specific resource operation (e.g., `clear.py`, `get.py`, `list.py`, `remove.py`, `save.py`).
     **Detailed Description:** Each file within this directory exports a function (e.g., `ClearCommand`, `GetCommand`) that acts as a factory for creating a command class tailored to its respective operation. These functions take parameters like parent classes, base names, facade names, and role-based permissions to construct a command with predefined `parse`, `exec`, `get_priority`, and `groups_allowed` methods. They encapsulate the logic for how each operation interacts with the underlying resource facade.

**app/systems/commands/factory/resource.py**
     **Role:** This file provides a high-level factory function for generating a complete set of resource-related commands.
     **Detailed Description:** The `ResourceCommandSet` function in this file orchestrates the creation of multiple command classes (list, get, save, remove, clear) for a given resource. It takes a command dictionary, parent classes, resource names, and various configuration options (like `save_fields`, `edit_roles`, `view_roles`) to build a comprehensive set of commands. It leverages the individual operation factories from the `operations` subdirectory to construct these commands, ensuring that all standard resource actions are available and properly configured.

**app/systems/commands/factory/helpers.py**
     **Role:** This file contains utility functions that assist in the dynamic generation and configuration of command classes.
     **Detailed Description:** `helpers.py` provides several helper functions used across the command factory. Functions like `get_value`, `get_facade`, and `get_joined_value` assist in constructing names and retrieving configuration values. `parse_field_names` and `get_field_names` are used for handling field selection in list and get commands, while `parse_fields` and `get_fields` facilitate the parsing and retrieval of data fields for save operations. These helpers centralize common logic, making the command generation process more modular and maintainable.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `ResourceCommandSet` function in `resource.py` is typically called to initiate the creation of a set of commands for a specific resource.
   2.  `ResourceCommandSet` then calls individual command factory functions (e.g., `ListCommand`, `GetCommand`, `SaveCommand`) located in the `operations` subdirectory.
   3.  These operation-specific factory functions utilize utilities from `helpers.py` to construct command class attributes, such as parsing arguments, defining execution logic, and setting permissions.
   4.  The `create_class` function from `utility.python` is used by these factories to dynamically generate the final command classes, which are then added to a command dictionary.
   5.  When a generated command is executed, its `parse` method (defined during creation) processes command-line arguments, and its `exec` method interacts with the appropriate resource facade to perform the desired operation.

**External Interfaces**
   *   **Resource Facades:** The generated commands interact heavily with resource facades (e.g., `_facade_name` in `operations/*.py`), which are responsible for abstracting the underlying data models and business logic. These facades are typically defined elsewhere in the `app/systems` or `app/data` directories.
   *   **Settings and Roles:** Command permissions are determined by `settings.roles.Roles`, which are external to this directory but crucial for access control.
   *   **Command-Line Interface (CLI):** The generated command classes are designed to be integrated into a CLI framework, where they receive arguments and produce output.
