Management Control Plane (MCP) API
==================================

The Zimagi Management Control Plane (MCP) API provides an interface for external systems and AI agents to interact with Zimagi's command and data services, particularly for tool indexing and execution.

Overview
--------
The MCP API is designed for asynchronous, streamable communication, allowing AI agents to discover and execute Zimagi commands as "tools."

API Endpoint
------------
The MCP API typically runs on `localhost:5423` by default, but this can be configured.

Authentication
--------------
The MCP API uses token-based authentication.

*   **Python SDK**: The `mcp` library (used internally by Zimagi agents) handles authentication.
*   **JavaScript SDK**: Not directly exposed for client-side usage in the same way as Command/Data APIs, but internal agents would use it.

Tool Indexing and Execution
---------------------------
A core feature of the MCP API is its ability to index Zimagi commands as callable tools. AI agents can then list these tools and execute them with specific parameters.

*   **Tool Discovery**: Agents can query the MCP to get a list of available tools, their descriptions, and parameters.
*   **Tool Execution**: Agents can send requests to execute a specific tool (Zimagi command) with provided arguments. The MCP API handles the execution and streams back the results.

Core API Components (`app/systems/api/mcp`)
-------------------------------------------
*   **`app/systems/api/mcp/errors.py`**: Custom exception classes for MCP API.
*   **`app/systems/api/mcp/tools.py`**: Manages indexing and execution of Zimagi commands as tools.
*   **`app/systems/api/mcp/routes.py`**: Defines API routes and connection handling.
*   **`app/systems/api/mcp/auth.py`**: Implements the authentication backend.
*   **`app/systems/api/mcp/client.py`**: Client-side interface for interacting with the MCP API.

Using the MCP API (Internal/Agent Use)
--------------------------------------
While direct external client usage is less common, internal Zimagi components and AI agents leverage the `MCPClient` to interact with the MCP.

Example: Listing Tools (Conceptual)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An AI agent might conceptually perform:

.. code-block:: python

    # This is conceptual, actual usage is via internal Zimagi agent logic
    from mcp import MCPClient

    mcp_client = MCPClient(host="localhost", port=5423, token="agent_token")
    await mcp_client.connect()
    tools = await mcp_client.list_tools()
    for tool in tools:
        print(f"Tool: {tool.name}, Description: {tool.description}")

Example: Executing a Tool (Conceptual)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
An AI agent might then execute a tool:

.. code-block:: python

    # This is conceptual, actual usage is via internal Zimagi agent logic
    result = await mcp_client.exec_tool("web:search", {"query": "Zimagi platform"})
    print(result)

The MCP API is a critical component for enabling advanced AI agent capabilities and external system integrations within Zimagi.
