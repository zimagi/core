=====================================================
README for Directory: app/templates
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for all Jinja2 template files used throughout the Zimagi application. These templates are crucial for defining the structure, content, and behavior of various application components, including data models, command definitions, plugin configurations, user roles, and AI cell prompts. It ensures consistency and accelerates development by providing standardized, reusable blueprints for generating dynamic content and configurations.

**Key Functionality**
   *   **Dynamic Configuration Generation:** Provides templates for generating YAML configuration files for data models, commands, and plugins.
   *   **User Management Definitions:** Contains templates for defining user roles and their associated properties.
   *   **AI Prompt Engineering:** Houses templates for structuring system prompts, chat interactions, and tool definitions for AI models.
   *   **Field Type Standardization:** Offers templates for standardizing the creation and configuration of various data field types.
   *   **Module Scaffolding:** Includes templates for generating new Zimagi modules with predefined structures and boilerplate code.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   The templates themselves are platform-agnostic, as they are processed by a templating engine. However, the generated output (YAML files, Python code, shell scripts) is intended for consumption by the Zimagi framework, which operates within a Dockerized environment, typically on Linux-based systems. The framework leverages Python 3.x for its backend services. The templating engine implicitly relies on Python's standard library.

**Local Dependencies**
   The templates within this directory primarily rely on the **Jinja2 templating engine** for rendering. They also implicitly depend on the Zimagi framework's internal mechanisms for interpreting and utilizing the generated configuration files. Specifically, modules like `app/systems/manage/service.py` are responsible for orchestrating the rendering process. Additionally, some templates utilize utility functions from `app/templates/functions` (e.g., `utility.data` for data manipulation and `utility.text` for interpolation).

File Structure and Descriptions
-------------------------------

**app/templates/cell**
     **Role:** This directory serves as a central repository for template files specifically designed for "cell" components within the Zimagi application.
     **Detailed Description:** These templates are crucial for defining the structure and content of various prompts and configurations used by the system, particularly in AI-driven interactions and dynamic content generation. It enables the dynamic generation of context-rich messages for AI models and facilitates the configuration of how these models interact with available tools and users.

**app/templates/field**
     **Role:** This directory serves as a central repository for defining various data field templates used throughout the Zimagi application.
     **Detailed Description:** These templates standardize the creation and configuration of different field types for data models, ensuring consistency and reusability across the system. They configure field properties such as nullability, default values, and editability, facilitating the automated generation of data model specifications and ensuring consistent data handling and validation.

**app/templates/data**
     **Role:** This directory serves as a central repository for Jinja2 templates used to generate various configuration files and code artifacts within the Zimagi project.
     **Detailed Description:** Specifically, it focuses on defining the structure and behavior of data models, commands, and plugins. It provides templates for defining the structure, fields, relationships, and API behavior of data models, offers templates for generating command mixins and base commands, and contains templates for creating plugin configurations that integrate with data models.

**app/templates/functions**
     **Role:** This directory serves as a centralized repository for reusable utility functions that can be incorporated into various templates throughout the Zimagi application.
     **Detailed Description:** These functions are designed to perform common data manipulations, text processing, and object transformations, ensuring consistency and reducing code duplication across the templating system. Key functionalities include standardized class name generation, robust list manipulation, and flexible text processing and rendering.

**app/templates/module**
     **Role:** This directory serves as a collection of templates for generating new modules within the Zimagi application framework.
     **Detailed Description:** It provides predefined structures and boilerplate code to ensure consistency and accelerate module development. It defines the basic file structure and configuration for modules, and includes optional components like license files, installation scripts, and Python requirements.

**app/templates/user**
     **Role:** This directory serves as a collection point for user-related templates within the Zimagi application.
     **Detailed Description:** It is designed to house definitions and configurations that pertain to user management, roles, and permissions, facilitating the dynamic generation of application components based on these templates. It provides a structured way to manage user-specific configurations and supports the generation of application components related to user access and permissions.

**app/templates/README.rst**
     **Role:** This file provides comprehensive documentation for the `app/templates` directory.
     **Detailed Description:** This README explains the purpose, key functionalities, dependencies, and file structure of the `app/templates` directory. It serves as a guide for developers and AI models to understand how the templates within this directory contribute to the overall Zimagi project architecture and how they are used to generate various configuration artifacts.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The templates within `app/templates` are not directly executable files. Instead, they are static resources consumed by the Zimagi application's templating engine (likely Jinja2). When a new component (e.g., a data model, a user role, an AI prompt, or a new module) needs to be generated or configured, a Zimagi management command or an internal process (such as those in `app/systems/manage/service.py`) will:
   1.  Identify the appropriate template file within `app/templates` (e.g., `app/templates/data/model/data.yml` for a data model).
   2.  Provide a context of variables (e.g., `name`, `plural_suffix`, `mixins`) to the templating engine.
   3.  The templating engine renders the template, substituting variables and applying conditional logic defined within the template.
   4.  The output is typically a YAML configuration file, a Python file, or a shell script, which is then consumed by other parts of the Zimagi system to define or configure the respective component.

**External Interfaces**
   The generated files from these templates serve as internal interfaces for other Zimagi components. For example:
   *   **Zimagi Data API:** Data model definitions generated from `app/templates/data/model` are used by the Zimagi Data API to create database tables, define ORM models, and expose RESTful endpoints.
   *   **Zimagi Command API:** Command structures defined in `app/templates/data/model` are used by the Zimagi Command API to register and execute commands.
   *   **Zimagi Plugin System:** Plugin configurations from `app/templates/data/model` integrate with the Zimagi plugin management system.
   *   **AI Models:** Prompt templates from `app/templates/cell/prompt` are fed as input to AI models (which might be external services like OpenAI or internal AI components) to guide their behavior and interactions.
   *   **Database:** Ultimately, data model definitions influence the schema and interactions with the underlying PostgreSQL database (as configured in `compose.db.yaml`).
   *   **Operating System/Shell:** Generated `install.sh` scripts from `app/templates/module/standard` interact with the operating system's package managers (e.g., `pip`) and shell environment.
