=====================================================
README for Directory: app/commands/log
=====================================================

Directory Overview
------------------

**Purpose**
   This directory centralizes the command-line interface (CLI) operations related to managing and interacting with system logs within the Zimagi platform. It provides functionalities for viewing, cleaning, rerunning, and aborting command executions that have been logged.

**Key Functionality**
   *  Retrieving and displaying detailed information about past command executions.
   *  Cleaning up old log entries and associated messages to manage storage.
   *  Aborting currently running or pending command tasks.
   *  Rerunning previously executed commands with their original configurations.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed to run within the Zimagi platform, which typically operates in a Dockerized environment. It relies on Python 3.x and the Django framework for its core functionality and ORM.

**Local Dependencies**
   *  `systems.commands.index.Command`: This is the base class for all Zimagi CLI commands, providing the fundamental structure and utilities for command execution and interaction.
   *  `yaml`: Used for dumping complex Python objects (like dictionaries or lists) into a human-readable YAML string format for display purposes.
   *  `copy`: Utilized for creating deep copies of command configurations when rerunning tasks to ensure immutability of original log data.


File Structure and Descriptions
-------------------------------

**app/commands/log/clean.py**
     **Role:** Defines the CLI command for cleaning up log entries.
     **Detailed Description:** This file contains the `Clean` command, which allows users to remove old log entries and their associated messages from the system. It leverages internal methods to specify retention periods for logs and messages, helping to maintain database size and relevance.

**app/commands/log/rerun.py**
     **Role:** Defines the CLI command for rerunning previously executed commands.
     **Detailed Description:** This file implements the `Rerun` command. It enables users to select one or more past command executions by their log keys and re-execute them with their original configuration parameters. This is crucial for debugging, re-attempting failed tasks, or repeating successful operations.

**app/commands/log/abort.py**
     **Role:** Defines the CLI command for aborting running or pending command tasks.
     **Detailed Description:** This file provides the `Abort` command, which allows users to gracefully terminate command tasks that are currently in progress or queued for execution. It publishes an abort signal and waits for the tasks to acknowledge and stop, ensuring a controlled shutdown.

**app/commands/log/get.py**
     **Role:** Defines the CLI command for retrieving and displaying detailed log information.
     **Detailed Description:** This file contains the `Get` command, which is used to fetch and present comprehensive details about a specific command execution log. It displays information such as the command name, status, associated user and schedule, worker details, and timestamps. It also includes the command's parameters and, if the command is still running, streams its messages in real-time.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   All files in this directory define specific CLI commands that inherit from `systems.commands.index.Command`. When a user executes a `zimagi log <subcommand>` command (e.g., `zimagi log get <log_key>`), the corresponding Python file's `exec` method is invoked. These `exec` methods then interact with the Zimagi ORM (`_log` attribute) to retrieve, modify, or query log data. For commands like `rerun` and `abort`, they might trigger new internal command executions or publish messages to the system's message queue.

**External Interfaces**
   The commands in this directory primarily interact with the Zimagi database (via Django ORM) to store and retrieve log entries and messages. The `abort.py` and `rerun.py` commands also interact with the Zimagi message queue (e.g., Celery) to publish signals for task management. The `get.py` command, when following a running task, continuously polls the database for new log messages.
