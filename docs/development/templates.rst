Using Templates
===============

Zimagi extensively uses Jinja2 templates for dynamic content generation and configuration. This section explains how templates are structured and used within the platform.

Overview
--------
Templates are crucial for defining the structure, content, and behavior of various application components, including data models, command definitions, plugin configurations, user roles, and AI cell prompts. They provide standardized, reusable blueprints.

Template Directory Structure (`app/templates`)
----------------------------------------------
The `app/templates/` directory serves as the central repository for all Jinja2 template files:

*   **`app/templates/cell`**: Templates for "cell" components, particularly AI prompts and configurations.
*   **`app/templates/field`**: Templates for defining various data field types.
*   **`app/templates/data`**: Templates for generating data models, commands, and plugin configurations.
*   **`app/templates/functions`**: Reusable utility functions that can be incorporated into templates.
*   **`app/templates/module`**: Templates for generating new modules.
*   **`app/templates/user`**: User-related templates for roles and permissions.

Template Functions (`app/templates/functions`)
----------------------------------------------
The `app/templates/functions/` directory contains reusable utility functions that can be called within Jinja2 templates:

*   **`app/templates/functions/core_class.py`**: Utilities for manipulating and generating class-related names (e.g., `class_name`).
*   **`app/templates/functions/core_list.py`**: Functions for processing and formatting list data (e.g., `ensure_list`, `comma_separated_value`).
*   **`app/templates/functions/core_text.py`**: Functions for text processing, splitting, and data serialization (e.g., `split_text`, `json`, `yaml`).

How Templates are Used
----------------------
Templates are not directly executed but are processed by Zimagi's templating engine (Jinja2). This typically happens when:

*   **Generating New Modules**: When you create a new module (e.g., `zimagi module create`), templates from `app/templates/module/standard` are used to scaffold the new module's files.
*   **Dynamic Model Generation**: Data model specifications (YAML files in `app/spec/data`) are often generated from templates in `app/templates/data/model`.
*   **AI Prompt Engineering**: AI agents load and render prompt templates from `app/templates/cell/prompt` to guide their behavior and interactions.
*   **Configuration Generation**: Various system configurations can be dynamically generated from templates.

Example: Module Template (`app/templates/module/standard/zimagi.yml`)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This template defines the core configuration for a new module:

.. code-block:: yaml

    name: {{ module_name }}
    version: 1.0.0
    compatibility:
        zimagi: ">=1.0.0"
    {% if include_install_script %}
    scripts:
        install: install.sh
    {% endif %}
    {% if include_requirements %}
    requirements: requirements.txt
    {% endif %}

When rendered, variables like `module_name`, `include_install_script`, and `include_requirements` are replaced with actual values, and conditional blocks are included or excluded.
