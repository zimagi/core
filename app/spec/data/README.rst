=====================================================
README for Directory: app/spec/data
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as the central repository for defining the data models and their associated metadata within the application's specification layer. These YAML files describe the structure, relationships, roles, and behaviors of various data entities, forming the blueprint for how data is managed and interacted with throughout the system.

**Key Functionality**
   *  **Data Model Definition:** Specifies the fields, types, and options for various data entities.
   *  **Role-Based Access Control (RBAC):** Defines edit and view permissions for data models based on user roles.
   *  **Inter-Model Relationships:** Establishes foreign key and many-to-many relationships between different data entities.
   *  **Dynamic Field Configuration:** Allows for the definition of fields whose values are computed or derived at runtime.
   *  **Provider and Group Mixins:** Integrates common functionalities like provider-based data handling and group associations into data models.

Dependencies
-------------------------

The data definitions in this directory are primarily consumed by the application's core framework to dynamically generate database schemas, API endpoints, and administrative interfaces. They rely on internal application components for interpreting the YAML structure and translating it into executable code and database migrations. Specific dependencies include:

*   **Django ORM:** The ``@django.`` prefixes indicate reliance on Django's Object-Relational Mapper for defining field types and relationships.
*   **Zimagi DataField and DictionaryField:** The ``@zimagi.`` prefixes refer to custom field types provided by the Zimagi framework for handling generic data and dictionary structures.

File Structure and Descriptions
-------------------------------

**app/spec/data/memory.yml**
     **Role:** Defines the data models for managing conversational memory and dialogs within the application.
     **Detailed Description:** This file specifies the `Memory`, `MemoryDialog`, and `MemoryMessage` data models. `Memory` stores general conversational context for a user, including a label. `MemoryDialog` represents a specific conversation instance associated with a memory, and `MemoryMessage` stores individual messages within a dialog, including sender, role, and content. These models are crucial for AI-driven conversational interfaces, allowing the system to maintain context and history for user interactions.

**app/spec/data/group.yml**
     **Role:** Defines the data model for user groups and a mixin for associating other data models with groups.
     **Detailed Description:** This file defines the `Group` data model, which represents hierarchical user groups within the system, allowing for nested group structures via a `parent` foreign key. It also includes the `GroupMixin`, a reusable component that enables other data models to have many-to-many relationships with groups, facilitating role-based access control and organizational structuring.

**app/spec/data/config.yml**
     **Role:** Defines the data model for application-wide configuration settings.
     **Detailed Description:** This file specifies the `Config` data model, which is used to store various configuration parameters for the application. It includes fields for a value and its type, allowing for flexible storage of different data types. The `provider` and `group` mixins indicate that configurations can be associated with specific providers and groups, enabling granular control and organization of settings. It also defines a `config_ensure` trigger for validation.

**app/spec/data/host.yml**
     **Role:** Defines the data model for representing external hosts or services that the application interacts with.
     **Detailed Description:** This file defines the `Host` data model, which stores information about external systems, including their URL, command and data ports, user credentials, and encryption keys. This model is essential for managing connections and secure communication with other services or remote environments, providing a centralized way to configure and access external resources.

**app/spec/data/user.yml**
     **Role:** Defines the data model for user accounts and their associated properties.
     **Detailed Description:** This file specifies the `User` data model, which includes standard user attributes like email, first name, last name, and active status. It also incorporates fields for authentication (password, temporary tokens, encryption key) and preferences related to AI/language processing, such as language, text splitter, and encoder providers, along with search limits and minimum scores. This comprehensive model supports user management, authentication, and personalized AI interactions.

**app/spec/data/schedule.yml**
     **Role:** Defines data models for scheduling tasks, including intervals, crontabs, and specific datetimes.
     **Detailed Description:** This file defines the `ScheduledTask` model, which represents a task to be executed at a future time. It can be linked to `TaskInterval`, `TaskCrontab`, or `TaskDatetime` models to specify the recurrence pattern. `ScheduledTask` also includes fields for arguments, keyword arguments, headers, and the user who scheduled the task, enabling flexible and robust task automation within the system.

**app/spec/data/notification.yml**
     **Role:** Defines data models for managing notifications and their associated recipient groups.
     **Detailed Description:** This file specifies the `Notification` data model, which represents a notification event. It also defines `NotificationGroup` and `NotificationFailureGroup` models, which link notifications to specific user groups for successful delivery and failure reporting, respectively. These models are critical for implementing a flexible and targeted notification system within the application.

**app/spec/data/module.yml**
     **Role:** Defines the data model for managing application modules, including their remote sources and versions.
     **Detailed Description:** This file defines the `Module` data model, which stores information about various modules integrated into the application. This includes details like the remote repository URL, reference (e.g., branch or tag), and dynamic fields for status, version, and compatibility. This model is fundamental for managing the lifecycle and dependencies of modular components within the system.

**app/spec/data/dataset.yml**
     **Role:** Defines the data model for managing datasets within the application.
     **Detailed Description:** This file specifies the `DataSet` data model, which represents collections of data. It includes `provider` and `group` mixins, indicating that datasets can be associated with specific data providers and user groups. The `dynamic_fields` attribute for `data` suggests that the actual data content might be dynamically loaded or generated, making this model central to data management and access control.

**app/spec/data/state.yml**
     **Role:** Defines a generic data model for storing application state.
     **Detailed Description:** This file defines the `State` data model, a simple yet powerful model for storing arbitrary application state information. It includes a `value` field of type `DataField`, allowing it to hold any type of data. This model is useful for persisting temporary or dynamic application states that need to be accessible across different parts of the system.

**app/spec/data/scaling.yml**
     **Role:** Defines the data model for tracking scaling events and worker statistics.
     **Detailed Description:** This file specifies the `ScalingEvent` data model, which records information related to the scaling of worker processes. It includes fields such as the command executed, worker type, maximum worker count, current worker count, task count, and the number of workers created. This model is crucial for monitoring and managing the dynamic scaling of background tasks and services.

**app/spec/data/log.yml**
     **Role:** Defines data models for logging application events and messages.
     **Detailed Description:** This file defines the `Log` data model, which records application events, including the user, command, status, task ID, associated schedule, and worker. It also defines `LogMessage`, which stores individual messages related to a specific log entry. These models are essential for auditing, debugging, and monitoring the application's operations.

**app/spec/data/cache.yml**
     **Role:** Defines the data model for managing application-level caching.
     **Detailed Description:** This file specifies the `Cache` data model, which is used to store and track cached items within the application. It includes fields for the cache item's name and the number of requests it has served. This model is important for optimizing application performance by providing a mechanism to store frequently accessed data.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The files in `app/spec/data` are primarily declarative definitions rather than executable code. Their "execution flow" is indirect:
   1.  During application startup or schema migration, the core framework reads these YAML files.
   2.  The framework parses the definitions (e.g., `memory.yml`, `user.yml`, `config.yml`).
   3.  It then uses these definitions to dynamically generate or update database tables, Django models, and API serializers.
   4.  When a user or an internal process interacts with a data entity (e.g., creating a `User` or updating a `Config`), the application's ORM and API layers utilize the structures defined in these YAML files to validate data, enforce roles, and manage persistence.

**External Interfaces**
   The data models defined in this directory primarily interface with:
   *   **Database (PostgreSQL):** The definitions are translated into SQL schema for the underlying PostgreSQL database, dictating table structures, relationships, and constraints.
   *   **Application APIs:** The models form the basis for the application's RESTful APIs, defining the structure of data that can be created, read, updated, and deleted.
   *   **User Interface (UI):** The metadata within these files (e.g., roles, field types) can inform the rendering and behavior of administrative and user-facing interfaces.
   *   **Other Internal Services:** Services like the scheduler (`schedule.yml`), notification system (`notification.yml`), and module manager (`module.yml`) directly consume and operate on the data structures defined here.
