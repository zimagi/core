Troubleshooting
===============

This section provides common troubleshooting tips and solutions for issues you might encounter while using or developing with Zimagi.

General Tips
------------
*   **Check Logs**: Always start by checking the logs of relevant services.
    *   For Docker Compose: `docker-compose logs [service_name]`
    *   For Kubernetes: `kubectl logs [pod_name]`
    *   For Zimagi command logs: `zimagi log list` or `zimagi log get [log_key]`
*   **Environment Variables**: Ensure all necessary environment variables are correctly set. Refer to :doc:`hosting/environment_variables`.
*   **Dependencies**: Verify that all required external and Python/JavaScript libraries are installed.
*   **Network Connectivity**: Check if services can communicate with each other (e.g., Zimagi API to PostgreSQL, Redis, Qdrant).

Common Issues
-------------

1.  **Services Not Starting**
    *   **Issue**: Docker containers fail to start or exit immediately.
    *   **Solution**:
        *   Check `docker-compose logs` for errors.
        *   Ensure Docker is running and has enough resources.
        *   Verify `env/secret` is correctly populated.
        *   Check for port conflicts.

2.  **API Connection Errors**
    *   **Issue**: Python/JavaScript SDK clients cannot connect to Zimagi APIs.
    *   **Solution**:
        *   Verify `ZIMAGI_COMMAND_HOST`, `ZIMAGI_COMMAND_PORT`, `ZIMAGI_DATA_HOST`, `ZIMAGI_DATA_PORT` environment variables.
        *   Ensure Zimagi API services are running (`zimagi platform info`).
        *   Check firewall rules.

3.  **Authentication Failures**
    *   **Issue**: API requests return "Authentication Failed" or "Permission Denied".
    *   **Solution**:
        *   Verify `user` and `token` (or `api_key`) are correct.
        *   Rotate user tokens if they might be expired or compromised: `zimagi user rotate [username]`.
        *   Check user roles and permissions in `app/spec/roles.yml` and data model specifications.

4.  **Task Scheduling Issues**
    *   **Issue**: Scheduled tasks are not running or are failing.
    *   **Solution**:
        *   Check Celery worker logs.
        *   Verify Redis connectivity.
        *   Ensure the scheduler service is running.
        *   Check `zimagi log list --command "schedule"` for task-specific errors.

5.  **AI Agent Problems**
    *   **Issue**: AI agents are not responding or generating incorrect output.
    *   **Solution**:
        *   Check agent logs (`zimagi log list --command "agent [agent_name]"`).
        *   Verify connectivity to external LLM providers (if used).
        *   Check Qdrant status if embeddings are involved.
        *   Review agent prompts and configurations in `app/templates/cell/prompt` and `app/spec/commands/chat.yml`.

6.  **Data Model/Migration Errors**
    *   **Issue**: Database schema issues or migration failures.
    *   **Solution**:
        *   Run `zimagi build` to rebuild specifications and migrations.
        *   Check Django migration logs.
        *   Ensure data model YAML files in `app/spec/data` are correctly formatted.

If you encounter issues not covered here, please refer to the `app/help/en` directory for command-specific documentation or consult the Zimagi community forums.
