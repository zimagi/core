=====================================================
README for Directory: app/templates/module
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as a collection of templates for generating new modules within the Zimagi application framework. It provides predefined structures and boilerplate code to ensure consistency and accelerate module development.

**Key Functionality**
   *   Provides a standard template for new Zimagi modules.
   *   Defines the basic file structure and configuration for modules.
   *   Includes optional components like license files, installation scripts, and Python requirements.

Dependencies
-------------------------

The templates themselves do not have direct runtime dependencies in the traditional sense, as they are source files used for generation. However, the generated modules and the templating system rely on:

*   **Zimagi Core:** The overall Zimagi application framework, which processes these templates and integrates the generated modules.
*   **Jinja2 (or similar templating engine):** Implied by the use of `{{ }}` and `{% %}` syntax in some template files, indicating a templating engine is used to render these files into actual module code.

File Structure and Descriptions
-------------------------------

**app/templates/module/standard**
     **Role:** This subdirectory contains the default and most commonly used template for generating a standard Zimagi module.
     **Detailed Description:** It provides a complete boilerplate for a new module, including its basic configuration (`zimagi.yml`), Python-related files (`django.py`, `requirements.txt`), a `.gitignore` for common exclusions, and an optional installation script (`install.sh`) and license file (`LICENSE`). This template is designed to be a starting point for most new module creations, offering a consistent and functional base structure.

**app/templates/module/standard/.gitignore**
     **Role:** This file specifies intentionally untracked files that Git should ignore when generating a module from the standard template.
     **Detailed Description:** It lists patterns for files and directories that should not be committed to version control within a generated module. This typically includes Python cache files (`__pycache__`), system-generated files (`.zimagi*`), and other temporary or build-related artifacts, ensuring a clean and relevant repository for the module's source code.

**app/templates/module/standard/install.sh**
     **Role:** This is a shell script template designed to install module-related dependencies.
     **Detailed Description:** When a module is generated with the `include_install_script` option, this script is included. It's intended to be executed to set up any necessary external dependencies or configurations for the module, ensuring that the module can run correctly in its environment. The `set -e` command ensures that the script exits immediately if any command fails.

**app/templates/module/standard/requirements.txt**
     **Role:** This file is a template for a Python requirements file, listing the Python packages that a generated module depends on.
     **Detailed Description:** If the `inlude_requirements` option is enabled during module generation, this file is created. Developers would then populate this file with the specific Python libraries and their versions required for their module, which can be installed using `pip`.

**app/templates/module/standard/django.py**
     **Role:** This file is a template for Django-specific environment configurations within a generated module.
     **Detailed Description:** It's intended to hold settings and configurations relevant to a Django application, allowing modules to integrate seamlessly with the Django framework used by Zimagi. It imports `Config` from `settings.config`, suggesting it's part of a larger configuration management system.

**app/templates/module/standard/index.yml**
     **Role:** This is a configuration file that defines the variables and mapping rules for generating a new module from the "standard" template.
     **Detailed Description:** It specifies the input variables required from the user (e.g., `module_name`, `modules`), their help text, and default values. Crucially, it also contains a `map` section that dictates which template files are copied to which target filenames, and under what conditions (`when` clauses based on input variables like `include_license` or `inlude_requirements`). It also defines a list of `directories` to be created by default within the new module.

**app/templates/module/standard/zimagi.yml**
     **Role:** This file is the core configuration file template for a Zimagi module.
     **Detailed Description:** It defines essential metadata for the module, such as its `name`, `version`, and `compatibility` with the Zimagi framework. It also conditionally includes references to the `scripts` (install.sh) and `requirements` (requirements.txt) files based on the generation options. Furthermore, it can list `modules` that this module depends on, specifying their `remote` source and `reference` version.

**app/templates/module/standard/LICENSE**
     **Role:** This file is a template for the Apache License, Version 2.0, to be included in a generated module.
     **Detailed Description:** If the `include_license` option is set during module generation, this file is copied into the new module. It provides the legal terms under which the module's code is distributed, ensuring compliance with open-source licensing standards.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The files within `app/templates/module` are not executed directly as part of the application's runtime. Instead, they are consumed by a module generation or scaffolding tool (likely part of the Zimagi core framework).

   1.  A user or an automated process initiates the creation of a new Zimagi module, specifying the "standard" template.
   2.  The Zimagi framework's templating engine reads the `index.yml` file within `app/templates/module/standard` to understand the template's structure, variables, and mapping rules.
   3.  Variables (e.g., `module_name`, `modules`, `include_license`) are passed to the templating engine, which then renders the template files (like `zimagi.yml`, `django.py`, `requirements.txt`, `install.sh`, `LICENSE`, and `.gitignore`) based on the `map` and `when` conditions defined in `index.yml`.
   4.  The rendered files are saved to the target directory, forming the new module's codebase, and the specified `directories` are created.
   5.  Optional scripts like `install.sh` (if included) might be executed as part of the module's setup process after generation.

**External Interfaces**
   The primary external interface for these templates is the **Zimagi module generation system**. This system reads the template files and uses them to create new modules. Once a module is generated from these templates, it will then interact with other Zimagi core components, databases (PostgreSQL, Redis, Qdrant), and potentially external APIs, depending on the module's specific functionality. The `requirements.txt` and `install.sh` files define dependencies and installation steps that interact with the operating system's package managers (e.g., `pip`) and shell environment.
