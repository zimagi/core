Chat Interactions
=================

Zimagi provides capabilities for real-time chat interactions, enabling communication between users and AI agents within the platform.

Overview
--------
The chat system supports sending and receiving messages on designated channels, maintaining conversational memory, and integrating with AI agents for intelligent responses.

Key Chat Interaction Features
-----------------------------
*   **Channel-Based Communication**: Send and listen for messages on specific chat channels.
*   **Conversational Memory**: AI agents maintain context across interactions.
*   **User Message Persistence**: Store chat messages for historical reference.
*   **AI Agent Integration**: AI agents can participate in and respond to chat messages.

Chat Commands (`app/commands/chat`)
-----------------------------------
*   **`app/commands/chat/send.py`**: Defines the command for sending chat messages.
*   **`app/commands/chat/listen.py`**: Defines the command for listening to incoming chat messages.

Chat Mixin (`app/commands/mixins/chat.py`)
------------------------------------------
*   **`app/commands/mixins/chat.py`**: Facilitates management of chat conversation memory and saving user messages.

Conversational Memory (`app/data/memory`)
-----------------------------------------
*   **`app/data/memory/models.py`**: Defines `Memory`, `MemoryDialog`, and `MemoryMessage` models for storing conversational context.
*   **`app/data/memory/migrations`**: Database migration files for memory models.

AI Agent Integration (`app/systems/cell`)
-----------------------------------------
*   **`app/systems/cell/memory.py`**: Manages the agent's long-term and short-term conversational memory.
*   **`app/systems/cell/actor.py`**: Orchestrates AI decision-making and response generation in chat.

Using Chat Interactions
-----------------------

1.  **Listening to a Chat Channel**: Use the `zimagi chat listen` command.

    .. code-block:: bash

        zimagi chat listen my-team-channel

    This command will continuously display messages sent to `my-team-channel`.

2.  **Sending a Chat Message**: In a separate terminal, use the `zimagi chat send` command.

    .. code-block:: bash

        zimagi chat send my-team-channel "Hello everyone, I need help with Zimagi."

3.  **AI Agent Participation**: AI agents can be configured to listen to chat channels and respond intelligently. The `app/spec/commands/chat.yml` file defines directives for AI agents, including their core mission, communication protocols, and available tools.

    Example from `app/spec/commands/chat.yml` (conceptual):

    .. code-block:: yaml

        _chat_directive:
            mission: "Assist users with Zimagi platform queries."
            communication:
                channels:
                    - chat:message
            tools:
                - web:search@local
                - web:fetch@local

Chat interactions are a powerful way to engage with Zimagi's AI capabilities and facilitate team communication within the platform.
