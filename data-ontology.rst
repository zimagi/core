====================
Zimagi Data Ontology
====================

Overview
========

This document provides a comprehensive data ontology for the Zimagi platform, outlining all core data models and their relationships. This ontology serves as a reference for connecting Zimagi module data models to core data models when generating AI data models.

Core Data Models
================

The Zimagi platform consists of several core data models that provide essential functionality for the system.

User Model
----------

The User model represents system users and their associated configurations.

**Fields:**
- name (CharField, primary_key): Unique identifier for the user
- email (EmailField): User's email address
- first_name (CharField): User's first name
- last_name (CharField): User's last name
- is_active (BooleanField): Whether the user account is active
- last_login (DateTimeField): Timestamp of last login
- password (CharField): User's password hash
- temp_token (CharField): Temporary authentication token
- temp_token_time (DateTimeField): Expiration time for temp token
- encryption_key (CharField): User-specific encryption key
- language_provider (CharField): Language model provider name
- language_provider_options (DictionaryField): Configuration for language provider
- text_splitter_provider (CharField): Text splitting provider name
- text_splitter_provider_options (DictionaryField): Configuration for text splitter
- encoder_provider (CharField): Text encoding provider name
- encoder_provider_options (DictionaryField): Configuration for encoder
- search_limit (IntegerField): Maximum search results to return
- search_min_score (FloatField): Minimum search score threshold

**Relationships:**
- groups (ManyToMany): Groups this user belongs to
- schedules (OneToMany): Scheduled tasks created by this user
- logs (OneToMany): Log entries associated with this user
- memories (OneToMany): Memory entries owned by this user

Group Model
-----------

The Group model represents user groups and their hierarchical relationships.

**Fields:**
- name (CharField, primary_key): Unique identifier for the group
- parent (ForeignKey): Parent group in hierarchy
- config (DictionaryField): Group-specific configuration
- provider_type (CharField): Provider implementation type
- variables (DictionaryField): Group variables

**Relationships:**
- children (OneToMany): Child groups
- users (ManyToMany): Users belonging to this group
- configs (ManyToMany): Configuration items associated with this group
- modules (ManyToMany): Modules associated with this group
- datasets (ManyToMany): Datasets associated with this group
- notifications (OneToMany): Notification groups
- notification_failure_groups (OneToMany): Notification failure groups

Config Model
------------

The Config model stores system configuration values.

**Fields:**
- name (CharField, primary_key): Unique identifier for the configuration item
- value (DataField): Configuration value in appropriate data type
- value_type (CharField): Type of the configuration value (str, int, bool, etc.)
- config (DictionaryField): Configuration-specific configuration
- provider_type (CharField): Provider implementation type
- variables (DictionaryField): Configuration variables

**Relationships:**
- groups (ManyToMany): Groups that have access to this configuration

Module Model
------------

The Module model represents installed modules and their configurations.

**Fields:**
- name (CharField, primary_key): Unique identifier for the module
- remote (CharField): Remote repository URL
- reference (CharField): Version reference (branch, tag, commit)
- config (DictionaryField): Module-specific configuration
- provider_type (CharField): Provider implementation type
- variables (DictionaryField): Module variables

**Relationships:**
- groups (ManyToMany): Groups that have access to this module

DataSet Model
-------------

The DataSet model represents data sources and their configurations.

**Fields:**
- name (CharField, primary_key): Unique identifier for the dataset
- config (DictionaryField): Dataset-specific configuration
- provider_type (CharField): Provider implementation type
- variables (DictionaryField): Dataset variables

**Relationships:**
- groups (ManyToMany): Groups that have access to this dataset

Host Model
----------

The Host model stores connection information for remote hosts.

**Fields:**
- name (CharField, primary_key): Unique identifier for the host
- host (URLField): Host URL
- command_port (IntegerField): Port for command API
- data_port (IntegerField): Port for data API
- user (CharField): Username for authentication
- token (CharField): Authentication token
- encryption_key (CharField): Encryption key for communication

Scheduled Task Models
---------------------

Scheduled tasks allow for recurring or time-based execution of commands.

ScheduledTask Model
~~~~~~~~~~~~~~~~~~~

**Fields:**
- name (CharField, primary_key): Unique identifier for the task
- task (CharField): Name of the Celery task to execute
- args (ListField): Positional arguments for the task
- kwargs (DictionaryField): Keyword arguments for the task
- headers (DictionaryField): Headers for the task execution
- queue (CharField): Queue to execute the task on
- exchange (CharField): AMQP exchange for routing
- routing_key (CharField): AMQP routing key
- priority (PositiveIntegerField): Task priority
- expires (DateTimeField): When the task expires
- expire_seconds (PositiveIntegerField): Seconds until task expires
- one_off (BooleanField): Whether to run only once
- start_time (DateTimeField): When to start scheduling
- enabled (BooleanField): Whether the task is enabled
- last_run_at (DateTimeField): When the task last ran
- total_run_count (PositiveIntegerField): Number of times task has run
- date_changed (DateTimeField): When task was last modified
- description (TextField): Description of the task
- user (ForeignKey): User who created the task
- interval (ForeignKey): Interval schedule
- crontab (ForeignKey): Crontab schedule
- clocked (ForeignKey): One-time execution time

TaskInterval Model
~~~~~~~~~~~~~~~~~~

**Fields:**
- every (IntegerField): Number of periods to wait
- period (CharField): Type of period (days, hours, minutes, etc.)

TaskCrontab Model
~~~~~~~~~~~~~~~~~

**Fields:**
- minute (CharField): Minutes specification
- hour (CharField): Hours specification
- day_of_month (CharField): Days of month specification
- month_of_year (CharField): Months of year specification
- day_of_week (CharField): Days of week specification
- timezone (TimeZoneField): Timezone for execution

TaskDatetime Model
~~~~~~~~~~~~~~~~~~

**Fields:**
- clocked_time (DateTimeField): Specific time for execution

Log Models
----------

Log models store execution logs and their messages.

Log Model
~~~~~~~~~

**Fields:**
- name (CharField, primary_key): Unique identifier for the log
- command (CharField): Command that generated the log
- status (CharField): Execution status (running, success, failed)
- task_id (CharField): Celery task ID
- worker (CharField): Worker that executed the task
- user (ForeignKey): User who initiated the command
- schedule (ForeignKey): Scheduled task that triggered execution
- config (DictionaryField): Log-specific configuration

**Relationships:**
- messages (OneToMany): Log messages

LogMessage Model
~~~~~~~~~~~~~~~~

**Fields:**
- id (CharField, primary_key): Unique identifier for the log message
- log (ForeignKey): Parent log entry
- data (DataField): Message data
- name (CharField): Name field (null)

**Relationships:**
- log (ForeignKey): Parent log entry

Notification Models
-------------------

Notification models manage system notifications and their recipient groups.

Notification Model
~~~~~~~~~~~~~~~~~~

**Fields:**
- name (CharField, primary_key): Unique identifier for the notification

**Relationships:**
- groups (OneToMany): Groups to receive notifications
- failure_groups (OneToMany): Groups to receive failure notifications

NotificationGroup Model
~~~~~~~~~~~~~~~~~~~~~~~

**Fields:**
- id (CharField, primary_key): Unique identifier for the notification group
- notification (ForeignKey): Parent notification
- group (ForeignKey): Group to receive notifications
- name (CharField): Name field (null)

NotificationFailureGroup Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Fields:**
- id (CharField, primary_key): Unique identifier for the notification failure group
- notification (ForeignKey): Parent notification
- group (ForeignKey): Group to receive failure notifications
- name (CharField): Name field (null)

State Model
-----------

The State model stores system state values.

**Fields:**
- name (CharField, primary_key): Unique identifier for the state item
- value (DataField): State value in appropriate data type

Memory Models
-------------

Memory models store conversation histories for AI interactions.

Memory Model
~~~~~~~~~~~~

**Fields:**
- id (CharField, primary_key): Unique identifier for the memory
- name (CharField): Name of the memory
- label (CharField): Human-readable label
- user (ForeignKey): User who owns this memory

**Relationships:**
- dialogs (OneToMany): Conversation dialogs
- messages (OneToMany): Memory messages

MemoryDialog Model
~~~~~~~~~~~~~~~~~~

**Fields:**
- id (CharField, primary_key): Unique identifier for the memory dialog
- memory (ForeignKey): Parent memory
- created (DateTimeField): When the dialog was created
- name (CharField): Name field (null)

**Relationships:**
- messages (OneToMany): Dialog messages

MemoryMessage Model
~~~~~~~~~~~~~~~~~~~

**Fields:**
- id (CharField, primary_key): Unique identifier for the memory message
- memory (ForeignKey): Parent memory
- dialog (ForeignKey): Parent dialog
- role (CharField): Role of message sender (user/assistant)
- sender (CharField): Name of message sender
- content (TextField): Message content
- name (CharField): Name field (null)

Cache Model
-----------

The Cache model tracks cached items and their usage.

**Fields:**
- id (CharField, primary_key): Unique identifier for the cache entry
- name (CharField): Cache key name
- requests (PositiveBigIntegerField): Number of requests for this cache entry

ScalingEvent Model
------------------

The ScalingEvent model tracks auto-scaling events.

**Fields:**
- name (CharField, primary_key): Unique identifier for the event
- command (CharField): Command that triggered scaling
- worker_type (CharField): Type of worker being scaled
- worker_max_count (IntegerField): Maximum worker count
- worker_count (IntegerField): Current worker count
- task_count (IntegerField): Number of pending tasks
- workers_created (IntegerField): Number of workers created

Model Relationships
===================

The following diagram illustrates the relationships between core data models:

::

    User 1-----* ScheduledTask
    User 1-----* Log
    User 1-----* Memory
    
    Group *-----* User
    Group *-----* Config
    Group *-----* Module
    Group *-----* DataSet
    Group *-----* NotificationGroup
    Group *-----* NotificationFailureGroup
    Group *-----* Notification
    Group 1-----* Group (parent/child)
    
    Config *-----* Group
    
    Module *-----* Group
    
    DataSet *-----* Group
    
    ScheduledTask *-----* TaskInterval
    ScheduledTask *-----* TaskCrontab
    ScheduledTask *-----* TaskDatetime
    ScheduledTask 1-----* User
    
    Log *-----* LogMessage
    Log 1-----* User
    Log 1-----* ScheduledTask
    
    Notification 1-----* NotificationGroup
    Notification 1-----* NotificationFailureGroup
    NotificationGroup *-----* Group
    NotificationFailureGroup *-----* Group
    
    Memory 1-----* User
    Memory 1-----* MemoryDialog
    Memory 1-----* MemoryMessage
    MemoryDialog 1-----* MemoryMessage

Abstract Base Models
====================

Zimagi provides two abstract base models that serve as foundations for data models:

NameResourceBase
----------------

Provides a named resource with automatic timestamps.

**Fields:**
- name (CharField, primary_key): Primary key identifier
- created (DateTimeField): Creation timestamp
- updated (DateTimeField): Last update timestamp

IdResourceBase
--------------

Provides an auto-generated ID resource with name and timestamps.

**Fields:**
- id (CharField, primary_key): Auto-generated primary key
- name (CharField): Human-readable name
- created (DateTimeField): Creation timestamp
- updated (DateTimeField): Last update timestamp

Model Mixins
============

Zimagi provides several mixins that can be applied to data models:

Resource Mixin
--------------

Provides automatic timestamp management.

**Fields:**
- created (DateTimeField): Creation timestamp
- updated (DateTimeField): Last update timestamp

Provider Mixin
--------------

Enables provider pattern for extensible functionality.

**Fields:**
- provider_type (CharField): Provider implementation type
- config (DictionaryField): Provider configuration
- variables (DictionaryField): Provider variables

Group Mixin
-----------

Provides group-based access control.

**Fields:**
- groups (ManyToManyField): Groups with access to this resource

Usage Guidelines
================

When creating module data models that integrate with Zimagi core models:

1. **Inherit from appropriate base models**: Use NameResourceBase or IdResourceBase as appropriate
2. **Apply relevant mixins**: Use ProviderMixin for extensible functionality, GroupMixin for access control
3. **Establish proper relationships**: Link to core models using ForeignKey or ManyToManyField relationships
4. **Follow naming conventions**: Use descriptive, consistent names for models and fields
5. **Define clear access controls**: Specify which groups should have access to your models
6. **Consider data lifecycle**: Think about how your data relates to logs, notifications, and state

This ontology provides a foundation for understanding how Zimagi's core data models interconnect and how module developers can effectively extend the platform while maintaining consistency with the overall system architecture.
