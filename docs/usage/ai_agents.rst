AI Agents
=========

Zimagi's AI agents are specialized, long-running processes designed to listen for specific events or messages, perform designated tasks, and interact with various internal and external services. They form the backbone of Zimagi's asynchronous processing and automation capabilities.

Overview
--------
AI agents provide the core intelligence and interaction logic for the Zimagi platform. They process sensory input, manage internal state and memory, formulate responses, and execute external tools.

Key Agent Functionality
-----------------------
*   **Asynchronous Task Execution**: Agents operate asynchronously, responding to events and messages.
*   **External Service Integration**: Seamlessly integrate with web browsers, language models, and vector databases.
*   **Data Processing & Encoding**: Handle data processing, text encoding into vector embeddings, and archival.
*   **System Monitoring**: Monitor and manage resources for other agents and system events.
*   **Conversational Memory**: Maintain context across AI-driven interactions.

Agent Directory Structure (`app/commands/agent`)
------------------------------------------------
*   **`app/commands/agent/archiver.py`**: Handles archival of system events (e.g., scaling events).
*   **`app/commands/agent/file_parser.py`**: Parses various file types and extracts textual content.
*   **`app/commands/agent/controller.py`**: Manages and orchestrates the scaling and lifecycle of other Zimagi agents.
*   **`app/commands/agent/language_model.py`**: Facilitates interaction with language models for text generation.
*   **`app/commands/agent/qdrant.py`**: Manages backup, cleaning, and restoration for Qdrant.
*   **`app/commands/agent/encoder.py`**: Handles text encoding into vector embeddings and Qdrant interactions.
*   **`app/commands/agent/browser.py`**: Provides web browsing capabilities (e.g., fetching HTML).

Core AI Agent System (`app/systems/cell`)
-----------------------------------------
The `app/systems/cell/` directory encapsulates the core intelligence and interaction logic:

*   **`app/systems/cell/prompt.py`**: Manages the creation and rendering of prompts for AI models.
*   **`app/systems/cell/communication.py`**: Handles message reception, processing, and sending.
*   **`app/systems/cell/state.py`**: Provides persistent and thread-safe state management.
*   **`app/systems/cell/error.py`**: Centralized handler for errors during command execution.
*   **`app/systems/cell/memory.py`**: Manages the agent's long-term and short-term conversational memory.
*   **`app/systems/cell/actor.py`**: Orchestrates decision-making, response generation, and tool execution.

Interacting with AI Agents
--------------------------

1.  **Asking Questions**: Use the `ai ask` command to interact with a language model.

    .. code-block:: bash

        zimagi ai ask "Explain the concept of quantum entanglement."

2.  **Chat Interactions**: Engage in real-time conversations.

    .. code-block:: bash

        zimagi chat listen my-ai-chat
        # In another terminal
        zimagi chat send my-ai-chat "Hi Zimagi agent, how can you help me today?"

3.  **Encoding Text**: Generate vector embeddings from text.

    .. code-block:: bash

        zimagi ai encode "This is a sample text for embedding."

4.  **Agent Scaling**: Manage the number of running agent instances.

    .. code-block:: bash

        zimagi service scale language_model --count 2

Agents are dynamically configured and can leverage various plugins (e.g., `language_model`, `encoder`, `file_parser`, `search_engine`) to perform their tasks.
