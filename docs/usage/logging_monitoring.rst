Logging & Monitoring
====================

Zimagi provides robust logging and monitoring capabilities to track system events, command executions, and agent activities, which is crucial for auditing, debugging, and operational insights.

Overview
--------
The platform centralizes log data, allowing for detailed historical records of command operations, task statuses, and system health.

Key Logging & Monitoring Features
---------------------------------
*   **Command Execution Logs**: Detailed records of every command executed, including user, status, task ID, and associated schedule.
*   **Log Messages**: Individual messages associated with each log entry, capturing command output and events.
*   **Log Cleaning**: Automatically remove old log entries based on retention policies.
*   **Real-time Service Monitoring**: Follow real-time messages from Zimagi service channels.
*   **Agent Activity Archival**: Archive system events, such as worker scaling activities.

Log Data Models (`app/data/log`)
---------------------------------
*   **`app/data/log/models.py`**: Defines the `Log` and `LogMessage` Django models.
*   **`app/data/log/migrations`**: Database migration files for log-related models.

Log Commands (`app/commands/log`)
---------------------------------
*   **`app/commands/log/clean.py`**: Cleans up old log entries.
*   **`app/commands/log/rerun.py`**: Reruns previously executed commands.
*   **`app/commands/log/abort.py`**: Aborts running or pending command tasks.
*   **`app/commands/log/get.py`**: Retrieves and displays detailed log information.

Service Monitoring Commands (`app/commands/service`)
----------------------------------------------------
*   **`app/commands/service/follow.py`**: Follows and displays real-time messages from Zimagi service channels.

Agent Archiving (`app/commands/agent/archiver.py`)
--------------------------------------------------
*   **`app/commands/agent/archiver.py`**: Agent responsible for archiving system events, specifically scaling events.

Using Logging & Monitoring
--------------------------

1.  **Retrieving Log Information**: Use the `zimagi log get` command.

    .. code-block:: bash

        zimagi log get [log_key]

    You can also list logs with filters:

    .. code-block:: bash

        zimagi log list --status failed --command "module install"

2.  **Cleaning Old Logs**:

    .. code-block:: bash

        zimagi log clean --log-days 30 --log-message-days 7

    This removes logs older than 30 days and log messages older than 7 days.

3.  **Following Service Messages**: Monitor real-time communication.

    .. code-block:: bash

        zimagi service follow command-api

    This will display messages flowing through the `command-api` channel.

4.  **Rerunning/Aborting Tasks**:

    .. code-block:: bash

        zimagi log rerun [log_key]
        zimagi log abort [log_key]

Effective logging and monitoring are essential for maintaining the health, performance, and security of your Zimagi deployment.
