Task Scheduling
===============

Zimagi provides robust capabilities for defining, scheduling, and managing automated tasks, enabling efficient workflows and system maintenance.

Overview
--------
Tasks are defined using YAML and can be executed by the Zimagi scheduler and controller services. This allows for automated workflows, system maintenance, and integration with core functionalities.

Key Task Scheduling Features
----------------------------
*   **YAML-based Task Definitions**: Define reusable command-line and script-based tasks.
*   **Flexible Scheduling**: Support for interval, crontab, and specific datetime-based schedules.
*   **Asynchronous Execution**: Tasks are executed asynchronously by Celery workers.
*   **Task Lifecycle Management**: Track task status, abort running tasks, and rerun past executions.
*   **Database Migrations**: Orchestrate database migrations as tasks.

Task Definitions (`app/tasks`)
------------------------------
The `app/tasks/` directory contains YAML-based task definitions:

*   **`app/tasks/utility.yml`**: General-purpose utility tasks (e.g., echoing text, delays, waiting for services).
*   **`app/tasks/zimagi.yml`**: Tasks related to Zimagi's database migration and schema management.

Data Models for Scheduling (`app/data/schedule`)
------------------------------------------------
The `app/data/schedule/` directory defines the Django models for managing schedules and periodic tasks:

*   **`app/data/schedule/models.py`**: Defines `ScheduledTask`, `TaskInterval`, `TaskCrontab`, `TaskDatetime` models.
*   **`app/data/schedule/migrations`**: Database migration files for scheduled tasks.

Core Celery Integration (`app/systems/celery`)
----------------------------------------------
*   **`app/systems/celery/app.py`**: Custom Celery application instance.
*   **`app/systems/celery/scheduler.py`**: Custom Celery Beat scheduler using the Django database.
*   **`app/systems/celery/registry.py`**: Custom task registry for command-based tasks.
*   **`app/systems/celery/worker.py`**: Manages the lifecycle and health of Celery worker processes.
*   **`app/systems/celery/task.py`**: Custom base class for Celery tasks.

Using Task Scheduling
---------------------

1.  **Defining a Task**: Tasks are defined in YAML files.

    Example from `app/tasks/utility.yml`:

    .. code-block:: yaml

        echo_hello:
            provider: script
            script: echo "Hello, Zimagi!"

2.  **Scheduling a Task via CLI**: Use the `zimagi schedule save` command.

    .. code-block:: bash

        zimagi schedule save my-hourly-echo --command "utility echo_hello" --interval "hours=1"

    This schedules the `echo_hello` task to run every hour.

3.  **Managing Logs for Tasks**: Monitor and manage logs of executed tasks.

    .. code-block:: bash

        zimagi log list --command "utility echo_hello"
        zimagi log abort [task_id]
        zimagi log rerun [task_id]

4.  **Database Migrations**: Trigger migrations as a task.

    .. code-block:: bash

        zimagi run migrate

This executes the `migrate` profile, which includes tasks for building and applying database migrations.
