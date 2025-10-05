=====================================================
README for Directory: app/systems/commands/mixins
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains a collection of reusable mixin classes designed to extend the functionality of command-line interface (CLI) commands within the Zimagi platform. These mixins encapsulate common patterns for argument parsing, data querying, service interaction, and output rendering, promoting code reuse and consistency across various Zimagi commands.

**Key Functionality**
   -   Automated argument parsing for flags, variables, and fields.
   -   Standardized interaction with Zimagi's data facades for querying and manipulating instances.
   -   Management of service lifecycles and execution of shell commands.
   -   Dynamic generation of command schema based on model definitions.
   -   Formatted rendering of data for CLI output.

Dependencies
-------------------------

The mixins in this directory primarily rely on internal Zimagi components and standard Python libraries.
-   `django.conf.settings`: For accessing global Django settings, such as `DB_LOCK` and `DOCKER_USER_UID`.
-   `utility.data`: Provides utilities for data manipulation, such as `ensure_list`, `normalize_value`, and `Collection`.
-   `utility.shell`: Used for executing shell commands and capturing output.
-   `utility.ssh`: Provides SSH client functionality for remote execution.
-   `utility.text`: Offers text formatting and interpolation capabilities.
-   `systems.commands.args`: Handles the underlying argument parsing logic for CLI commands.
-   `systems.commands.index.CommandMixin`: The base class that these mixins extend, providing core command functionality.
-   `systems.models.base.BaseModel`: Used for type hinting and interacting with Zimagi's ORM.
-   `inflect`: A library for pluralizing words, used in `meta.py` for generating plural names.
-   `yaml`: For dumping YAML formatted data in `renderer.py`.
-   `docker`: The Docker SDK for Python, used in `app/systems/manage/service.py` for Docker container management.

File Structure and Descriptions
-------------------------------

**app/systems/commands/mixins/meta.py**
     **Role:** Dynamically generates command-line argument parsing methods and properties based on predefined schemas.
     **Detailed Description:** This file defines `MetaBaseMixin`, a metaclass that programmatically adds methods to command classes. It inspects a `schema` attribute on the command class to create methods for parsing instance IDs, keys, fields, and search parameters, as well as methods for interacting with providers and relations. This significantly reduces boilerplate code for command argument definition and ensures consistency. It relies on `inflect` for pluralization and `django.conf.settings` to check for database lock status.

**app/systems/commands/mixins/exec.py**
     **Role:** Provides methods for executing shell commands and establishing SSH connections.
     **Detailed Description:** The `ExecMixin` class offers `sh` for local shell command execution with real-time output streaming and `ssh` for establishing secure shell connections to remote hosts. It includes callback mechanisms for handling stdout and stderr, and wraps SSH operations with error handling. This mixin is crucial for commands that need to interact with the underlying operating system or remote servers.

**app/systems/commands/mixins/query.py**
     **Role:** Encapsulates common patterns for querying and manipulating data instances through Zimagi's facade system.
     **Detailed Description:** `QueryMixin` provides methods like `get_instance`, `get_instances`, `search_instances`, `save_instance`, and `remove_instance`. These methods abstract away the complexities of interacting with Zimagi's data layer, including caching, filtering, and error handling. It allows commands to easily retrieve, create, update, and delete model instances, supporting both single and multiple instance operations. It uses regular expressions for parsing search queries and `utility.data` for value normalization.

**app/systems/commands/mixins/relations.py**
     **Role:** Manages the parsing and resolution of command-line arguments related to model relationships and scope.
     **Detailed Description:** The `RelationMixin` class provides methods to parse and set the scope for facade operations, ensuring that commands operate within the correct hierarchical context (e.g., a user within a specific group). It also handles the parsing of related instance keys, allowing commands to link instances across different models. This mixin is essential for commands that deal with complex data structures and inter-model dependencies.

**app/systems/commands/mixins/renderer.py**
     **Role:** Provides utilities for formatting and rendering data for display in the command-line interface.
     **Detailed Description:** `RendererMixin` offers methods to render lists of instances and detailed instance displays. It dynamically determines which fields to display based on command configurations and model facades, handles datetime formatting, and can render related instances in a structured way. It uses `utility.data` and `utility.display` (implicitly) for formatting and `yaml` for dumping complex data types.

**app/systems/commands/mixins/base.py**
     **Role:** Serves as the foundational mixin for all command-line interface commands, providing core argument parsing and common utility methods.
     **Detailed Description:** `BaseMixin` is the entry point for most command mixins, inheriting from `MetaBaseMixin` to enable dynamic argument generation. It provides fundamental methods for parsing flags, single variables, and multiple variables, including handling defaults, help text, and tags. It also includes common command options like `test`, `force`, `count`, `clear`, and `search`, making them readily available to any command that inherits from it. It extensively uses `systems.commands.args` for argument parsing and `utility.text` for help text formatting.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A Zimagi CLI command is invoked, which is an instance of a class inheriting from `CommandMixin` and potentially several mixins from this directory.
   2.  During command initialization, `app/systems/commands/mixins/base.py` (via `MetaBaseMixin`) dynamically adds argument parsing methods based on the command's schema.
   3.  When the command's `parse_args` method is called, methods from `base.py`, `meta.py`, `relations.py`, and `query.py` are used to process command-line arguments, flags, and options, populating the command's `options` attribute.
   4.  During command execution, methods from `query.py` are used to interact with Zimagi's data facades to retrieve, create, update, or delete model instances.
   5.  If the command needs to execute external processes or connect to remote systems, methods from `exec.py` are utilized.
   6.  Finally, if the command needs to display structured output, methods from `renderer.py` are employed to format the data for the console.

**External Interfaces**
   -   **Zimagi Data Facades:** The `query.py` and `relations.py` mixins interact heavily with Zimagi's internal data facades (defined elsewhere in the `systems.models` and `systems.facades` directories) to perform ORM operations on the underlying database (PostgreSQL, Redis, Qdrant).
   -   **Operating System Shell:** The `exec.py` mixin directly interacts with the local operating system's shell for executing commands and with remote systems via SSH.
   -   **Docker Daemon:** The `app/systems/manage/service.py` (which is used by some commands) interacts with the Docker daemon via the Docker SDK for Python to manage containers, images, and networks.
   -   **External APIs/Services:** While not directly implemented in these mixins, the `exec.py` mixin provides the capability for commands to interact with external APIs or services by executing `curl` or other HTTP client commands.
