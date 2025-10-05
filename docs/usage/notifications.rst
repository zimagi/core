Notifications
=============

Zimagi provides a flexible notification system to keep users informed about command execution statuses and other system events.

Overview
--------
The notification system allows you to subscribe user groups to receive alerts for specific commands, including success and failure notifications.

Key Notification Features
-------------------------
*   **Command Status Notifications**: Receive alerts when commands complete successfully or fail.
*   **Group-Based Subscriptions**: Target notifications to specific user groups.
*   **Configurable Notification Types**: Subscribe to general command notifications or only to failure notifications.
*   **Email Integration**: Notifications are typically sent via email.

Notification Data Models (`app/data/notification`)
--------------------------------------------------
*   **`app/data/notification/models.py`**: Defines `Notification`, `NotificationGroup`, and `NotificationFailureGroup` models.
*   **`app/data/notification/migrations`**: Database migration files for notification models.

Notification Commands (`app/commands/notification`)
--------------------------------------------------
*   **`app/commands/notification/save.py`**: Saves notification subscriptions.
*   **`app/commands/notification/remove.py`**: Removes notification subscriptions.
*   **`app/commands/notification/clear.py`**: Clears all existing notification preferences.

Using Notifications
-------------------

1.  **Subscribing to Notifications**: Use the `zimagi notification save` command.

    .. code-block:: bash

        zimagi notification save my-command --notify-command "module install" --notify-groups "admin_group"

    This subscribes the `admin_group` to receive notifications for the `module install` command.

    To subscribe only to failure notifications:

    .. code-block:: bash

        zimagi notification save my-failure-alert --notify-command "my-critical-task" --notify-groups "dev_ops" --notify-failure true

2.  **Removing Subscriptions**:

    .. code-block:: bash

        zimagi notification remove my-command --notify-groups "admin_group"

3.  **Clearing All Preferences**:

    .. code-block:: bash

        zimagi notification clear

4.  **Email Configuration**: Ensure your email settings are configured in `app/settings/full.py` and via environment variables (e.g., `ZIMAGI_EMAIL_HOST`, `ZIMAGI_EMAIL_HOST_USER`, `ZIMAGI_EMAIL_HOST_PASSWORD`).

Notifications are an important tool for maintaining awareness of system operations and responding promptly to issues.
