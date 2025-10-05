=====================================================
README for Directory: app/systems/api/mcp
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains the core components for the Zimagi Management Control Plane (MCP) API, providing the interface for external systems and AI agents to interact with Zimagi's command and data services. It defines the API's structure, authentication mechanisms, tool indexing, and request handling.

**Key Functionality**
   *   Defines the API endpoints and request/response schemas for the MCP.
   *   Handles authentication and authorization for incoming API requests.
   *   Indexes and exposes Zimagi commands as callable tools for external agents.
   *   Manages the execution of these tools and formats their responses.
   *   Provides error handling and session management for API interactions.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed to run within a Python 3.x environment, specifically integrated with the Django framework and leveraging ASGI for asynchronous operations. It operates within a Dockerized environment, often orchestrated by Docker Compose or Kubernetes, and relies on Starlette for its web framework capabilities.

**Local Dependencies**
   *   ``django.conf.settings``: Used for accessing global application settings and configurations.
   *   ``starlette``: Provides the ASGI web framework for handling HTTP requests and responses.
   *   ``mcp``: The core Management Control Plane library, defining types and client/server communication.
   *   ``asyncio``: Python's built-in library for writing concurrent code using the async/await syntax.
   *   ``docker``: The Docker SDK for Python, used by the service manager for container operations (though not directly in the MCP API files themselves, it's a broader system dependency).
   *   ``utility.data``: Provides utility functions for data manipulation, such as `Collection`, `dump_json`, and `flatten`.
   *   ``systems.commands``: Provides access to the Zimagi command system, including `action` commands and the `router`.


File Structure and Descriptions
-------------------------------

**app/systems/api/mcp/errors.py**
     **Role:** Defines custom exception classes for the MCP API.
     **Detailed Description:** This file contains custom exception classes, such as `ServerError` and `SessionNotFoundError`, which are used throughout the MCP API to provide structured error handling. `ServerError` includes an HTTP status code, allowing for more specific error responses to clients. These exceptions help in clearly communicating issues that arise during API request processing or session management.

**app/systems/api/mcp/tools.py**
     **Role:** Manages the indexing and execution of Zimagi commands as callable tools for the MCP API.
     **Detailed Description:** This file is central to exposing Zimagi's internal commands as external tools. It includes functions like `get_type` for mapping internal data types to MCP-compatible types, and `index_tools` which recursively traverses the Zimagi command tree to build a list of available tools. It also defines `tool_call_handler` to execute these indexed tools based on incoming requests, handling command parsing, option formatting, and converting command responses into MCP-compatible content types (text, JSON, images).

**app/systems/api/mcp/routes.py**
     **Role:** Defines the API routes and connection handling logic for the MCP API.
     **Detailed Description:** This file sets up the routing for the MCP API, including a basic status endpoint (`/status`) and the main connection handler. The `get_connection_handler` function is responsible for initializing the connection, performing authentication checks, and indexing available tools for the connected user before delegating to the session manager. It also includes `get_connection_lifespan` for managing the application's lifecycle with the streamable HTTP session manager.

**app/systems/api/mcp/auth.py**
     **Role:** Implements the authentication backend for the MCP API.
     **Detailed Description:** This file defines the `TokenAuthBackend` class, which is a Starlette `AuthenticationBackend` responsible for validating incoming authentication tokens. It extends `APITokenAuthenticationMixin` to handle token parsing and user authentication. The `authenticate` method extracts the bearer token from the request headers, verifies it against the Zimagi user's credentials (including temporary tokens), and raises `AuthenticationError` if validation fails, ensuring secure access to the MCP API.

**app/systems/api/mcp/client.py**
     **Role:** Provides a client-side interface for interacting with the MCP API.
     **Detailed Description:** This file contains the `MCPClient` class, which acts as a wrapper for making requests to MCP servers. It manages connections to multiple MCP servers (local and remote), handles token authentication, lists available tools from these servers, and executes specific tools with provided arguments. The `connect` asynchronous context manager establishes streamable HTTP connections, and `format_tool_message` converts various MCP content types into a readable format. This client is crucial for any internal Zimagi component or external application that needs to programmatically interact with the MCP.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  An incoming request to the MCP API first hits the `handle_connection` function in `app/systems/api/mcp/routes.py`.
   2.  `_initialize_connection` (also in `routes.py`) is called, which performs authentication using the `TokenAuthBackend` from `app/systems/api/mcp/auth.py`.
   3.  Upon successful authentication, `index_tools` from `app/systems/api/mcp/tools.py` is invoked to discover and register all available Zimagi commands as callable tools for the authenticated user.
   4.  The request is then passed to the `session_manager` (an external component) for further processing.
   5.  If the request is a `ListToolsRequest`, the `tools_list_handler` in `app/systems/api/mcp/tools.py` is executed, returning a list of indexed tools.
   6.  If the request is a `CallToolRequest`, the `tool_call_handler` in `app/systems/api/mcp/tools.py` is executed. This handler finds the specified Zimagi command, formats the arguments, executes the command, and converts its output into MCP-compatible messages.
   7.  Errors encountered during this flow are typically handled by exceptions defined in `app/systems/api/mcp/errors.py`.

**External Interfaces**
   *   **Zimagi Command System:** The MCP API heavily interfaces with the core Zimagi command system (defined in `systems.commands`) to discover, parse, and execute commands.
   *   **Django Settings:** It relies on Django's settings (`django.conf.settings`) for configuration, including API service names, Kubernetes namespaces, and temporary token expiration.
   *   **Streamable HTTP (mcp library):** Communication between the MCP client (`app/systems/api/mcp/client.py`) and the MCP server is facilitated by the `mcp` library's streamable HTTP implementation, allowing for efficient asynchronous request/response handling.
   *   **User Authentication:** It interacts with the Zimagi user model to verify credentials and manage temporary tokens.
   *   **Docker (indirectly):** While not directly managed by these files, the underlying Zimagi services that the MCP API interacts with are often Docker containers, and the `ManagerServiceMixin` (from `app/systems/manage/service.py`) handles their lifecycle.
