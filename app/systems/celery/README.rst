=====================================================
README for Directory: app/systems/celery
=====================================================

Directory Overview
------------------

**Purpose**
   This directory encapsulates the core Celery integration for the application, managing asynchronous task processing, scheduling, and worker management. It provides the necessary components to define, register, and execute background tasks, ensuring efficient and scalable operations.

**Key Functionality**
   Asynchronous task definition and execution, task scheduling with various triggers (intervals, crontabs, specific datetimes), custom task registry for command-based tasks, robust worker management for graceful shutdown and resource optimization, and task-specific notification handling.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for Python 3.x environments, specifically within a Django framework context, leveraging Docker for containerization and Redis as a message broker and result backend. It integrates with the Celery distributed task queue system.

**Local Dependencies**
   *   `celery`: The core distributed task queue system.
   *   `django-celery-beat`: Provides a Django database-backed scheduler for Celery.
   *   `redis`: Client library for interacting with the Redis message broker.
   *   `django.conf.settings`: Accesses application-wide settings for configuration.
   *   `systems.commands.action`: Integrates with the application's command execution framework.
   *   `utility.data`: Provides utility functions for data manipulation, such as `ensure_list`.
   *   `utility.filesystem`: Provides utility functions for file system operations, such as `save_file`.


File Structure and Descriptions
-------------------------------

**app/systems/celery/app.py**
     **Role:** Defines the custom Celery application instance for the project.
     **Detailed Description:** This file extends the base Celery application to integrate a custom task registry. It serves as the central point for configuring and initializing the Celery application, ensuring that all tasks and workers use the project's specific registry for command-based tasks.

**app/systems/celery/scheduler.py**
     **Role:** Implements a custom Celery Beat scheduler that uses the Django database for scheduled tasks.
     **Detailed Description:** This file extends `django_celery_beat.schedulers.DatabaseScheduler` to provide enhanced scheduling capabilities. It defines `ScheduleEntry` to manage scheduled tasks, including intervals, crontabs, and specific datetimes. It also includes logic for optimizing crontab queries to reduce database load and handles the asynchronous application of scheduled tasks, setting worker type and priority.

**app/systems/celery/registry.py**
     **Role:** Provides a custom task registry for Celery that supports command-based tasks.
     **Detailed Description:** This file defines `CommandTaskRegistry`, which overrides the default Celery task registry. It ensures that tasks retrieved from the registry are deep-copied to prevent unintended modifications and provides a mechanism to retrieve the original task definition. It also includes a helper function `_unpickle_task` for proper task deserialization.

**app/systems/celery/worker.py**
     **Role:** Manages the lifecycle and health of Celery worker processes.
     **Detailed Description:** This file defines `WorkerManager`, a threading-based component responsible for monitoring Celery workers. It uses Redis to check queue lengths and the Celery inspector to monitor active and reserved tasks. The manager can gracefully terminate workers that become idle for a configurable timeout, ensuring efficient resource utilization and preventing zombie processes.

**app/systems/celery/task.py**
     **Role:** Defines a custom base class for Celery tasks, providing common functionalities for command execution and notifications.
     **Detailed Description:** This file introduces `CommandTask`, which extends `celery.Task`. It includes methods for executing application commands within a task context (`exec_command`) and sending email notifications (`send_notification`). This base class ensures that all tasks inherit essential functionalities, such as user context management for commands and robust email delivery with error handling.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `app/systems/celery/app.py` file initializes the custom Celery application, which uses the `app/systems/celery/registry.py` for task registration.
   2.  Scheduled tasks are managed by `app/systems/celery/scheduler.py`, which retrieves task definitions from the Django database and uses the Celery application to apply them asynchronously.
   3.  When a task is executed, it typically inherits from `app/systems/celery/task.py`, allowing it to execute application commands via `exec_command` or send notifications via `send_notification`.
   4.  Celery worker processes, potentially managed by `app/systems/celery/worker.py`, pick up and execute these tasks. The `WorkerManager` monitors the queues and active tasks to ensure workers are operating efficiently and can be terminated if idle.

**External Interfaces**
   *   **Redis:** Used as the message broker and result backend for Celery, handling task queues and storing task results.
   *   **Django Database:** The `app/systems/celery/scheduler.py` interacts with the Django database to store and retrieve scheduled task definitions (e.g., `ScheduledTask`, `TaskInterval`, `TaskCrontab`, `TaskDatetime`).
   *   **SMTP Server:** The `app/systems/celery/task.py` uses Django's email backend to send notifications via an SMTP server configured in `settings.EMAIL_HOST`.
   *   **Operating System (Docker):** The `app/systems/celery/worker.py` interacts with the operating system (specifically, Docker when `WORKER_PROVIDER` is "docker") to manage worker processes, including sending `SIGTERM` signals to terminate idle workers.
   *   **Application Commands:** Tasks defined using `app/systems/celery/task.py` can execute other application commands through the `systems.commands.action` framework.
