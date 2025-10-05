=====================================================
README for Directory: app/help
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for all help documentation within the application. It organizes help content by language and command, providing descriptive overviews and detailed explanations for various functionalities. This structure ensures that both human users and AI models can easily access and understand the purpose and usage of different application commands and features.

**Key Functionality**
   *   Centralized storage and organization of application help documentation.
   *   Categorization of help content by language (e.g., English).
   *   Detailed descriptions for application commands, including overviews and usage instructions.
   *   Facilitates consistent and accessible documentation for all application features.


Dependencies
-------------------------

This directory primarily contains static content files (YAML). It does not have direct runtime code dependencies on external libraries or services. Its content is consumed by other parts of the application (e.g., CLI, UI) that are responsible for parsing and displaying the help information.


File Structure and Descriptions
-------------------------------

**app/help/en**
     **Role:** This subdirectory contains all the English language help documentation for the application's commands and features.
     **Detailed Description:** Within this directory, each YAML file corresponds to a major command or a logical grouping of commands (e.g., `dataset.yml`, `schedule.yml`). These YAML files are structured to provide an `overview` (a brief summary) and a `description` (a more detailed explanation) for each command and its subcommands. This hierarchical organization allows for comprehensive and easily navigable help content, ensuring that users can quickly find information relevant to their needs.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The files within `app/help/en` are static data files and do not have an active execution flow in themselves. Instead, they are loaded and parsed by other components of the application. Typically, when a user requests help for a command (e.g., `zimagi --help` or `zimagi dataset --help`), the application's command-line interface (CLI) or a documentation generation tool will read the relevant YAML file from `app/help/en`, parse its content, and then display the `overview` and `description` fields to the user.

**External Interfaces**
   The help files in this directory primarily interface with the application's internal components that are responsible for displaying help information. This includes:
   *   **Command-Line Interface (CLI):** The CLI reads these YAML files to provide on-demand help for various commands.
   *   **Documentation Generators:** Tools that build official documentation (e.g., a website) would parse these files to create comprehensive user guides.
   *   **AI Models/Agents:** Other AI components within the system might access these files to understand command capabilities and generate more informed responses or actions.
