=====================================================
README for Directory: app/spec/base
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for base specifications (specs) that define the fundamental structure and behavior of various core components within the Zimagi application. These specifications are written in YAML and are crucial for configuring how commands, data resources, and other system elements are processed and managed.

**Key Functionality**
   Defines the foundational command structures and their associated permissions. Establishes the base definitions for data resources, including their fields, types, and metadata. Provides a standardized and extensible framework for system configuration.

Platform and Dependencies
-------------------------

The files in this directory are YAML configuration files, which are platform-agnostic in their definition. They are primarily consumed and interpreted by the Zimagi Python backend, which runs on a Linux-based Docker environment. The parsing and application of these specifications rely on Python's YAML parsing libraries and the internal Zimagi framework for dynamic configuration.

File Structure and Descriptions
-------------------------------

**app/spec/base/command.yml**
     **Role:** Defines the base command specifications and their associated properties within the Zimagi system.
     **Detailed Description:** This YAML file outlines the fundamental commands available in Zimagi, including their mixins, allowed user groups, background execution status, and parsing rules. It acts as a blueprint for how various system operations are structured and authorized. For instance, it defines base commands like `platform`, `host`, `user`, `group`, `config`, `module`, `schedule`, `notification`, `service`, `db`, `webhook`, `qdrant_admin`, `cache`, `log`, `scaling_event`, `import`, `calculate`, `dataset`, `gpu`, `ai`, `chat`, `mcp`, `agent`, `cell`, `library`, and `browser`, specifying their default behaviors and permissions. It is a critical component for understanding the command-line interface and internal command processing logic.

**app/spec/base/data.yml**
     **Role:** Specifies the base data resource definitions used throughout the Zimagi application.
     **Detailed Description:** This YAML file contains the core definitions for data resources, such as `name_resource` and `id_resource`. It details the class, mixins, unique identifiers (`id`, `key`), and fields for each resource. For each field, it specifies the data type (e.g., `@django.CharField`), color for display purposes, and options like `primary_key`, `max_length`, and `editable`. The `meta` section defines ordering for these resources. This file is essential for understanding the data models and how data is structured and managed within Zimagi.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The YAML files in `app/spec/base` are loaded and parsed by the Zimagi backend during application startup or configuration refresh. The `command.yml` file is used to dynamically register and configure available commands, their permissions, and execution characteristics. The `data.yml` file is used to define and register data models, influencing how data is stored, retrieved, and validated within the system. These specifications are then referenced by various Zimagi services, such as the command API, data API, and controller, to enforce rules and structure operations.

**External Interfaces**
   The specifications defined in this directory primarily interface with the internal Zimagi application services. They dictate the behavior of the command-line interface (CLI) and the data management layer. While these YAML files themselves do not directly interact with external databases or APIs, the services that consume these specifications will interact with a PostgreSQL database (for data persistence), Redis (for caching and messaging), and Qdrant (for vector search), as configured by other parts of the Zimagi system.
