Qdrant Management
=================

Zimagi integrates with Qdrant, a high-performance vector database, for efficient semantic search, similarity matching, and managing vector embeddings.

Overview
--------
Qdrant is crucial for AI-driven interactions, allowing the platform to store and query vector representations of text and other data.

Key Qdrant Management Features
------------------------------
*   **Collection Management**: Create, list, and manage Qdrant collections.
*   **Snapshot Management**: Create, restore, and clean up Qdrant snapshots for backup and recovery.
*   **Semantic Search**: Perform similarity searches using vector embeddings.
*   **Embedding Storage**: Store vector representations of text, conversational memory, and content sections.

Qdrant Commands (`app/commands/qdrant`)
---------------------------------------
*   **`app/commands/qdrant/remove.py`**: Removes a specific Qdrant snapshot.
*   **`app/commands/qdrant/clean.py`**: Cleans up old Qdrant snapshots.
*   **`app/commands/qdrant/snapshot.py`**: Creates a new Qdrant snapshot.
*   **`app/commands/qdrant/restore.py`**: Restores a Qdrant collection from a snapshot.
*   **`app/commands/qdrant/list.py`**: Lists Qdrant collections and their snapshots.

Qdrant Mixin (`app/commands/mixins/qdrant.py`)
----------------------------------------------
*   **`app/commands/mixins/qdrant.py`**: Facilitates interaction with the Qdrant vector database.

Qdrant Collection Plugins (`app/plugins/qdrant_collection`)
-----------------------------------------------------------
*   **`app/plugins/qdrant_collection/library.py`**: Provider for library content.
*   **`app/plugins/qdrant_collection/memory.py`**: Provider for conversational memory.
*   **`app/plugins/qdrant_collection/base.py`**: Base class for all Qdrant collection plugins.
*   **`app/plugins/qdrant_collection/section.py`**: Provider for sections of library content.

AI Agent Integration (`app/commands/agent/encoder.py`, `app/commands/agent/qdrant.py`)
-------------------------------------------------------------------------------------
*   **`app/commands/agent/encoder.py`**: Handles text encoding into vector embeddings and manages Qdrant interactions for storage and search.
*   **`app/commands/agent/qdrant.py`**: Manages backup, cleaning, and restoration operations for Qdrant.

Using Qdrant Management
-----------------------

1.  **Listing Qdrant Collections**: Use the `zimagi qdrant list` command.

    .. code-block:: bash

        zimagi qdrant list

    This will show details about your Qdrant collections and their snapshots.

2.  **Creating a Snapshot**:

    .. code-block:: bash

        zimagi qdrant snapshot my_collection_name

3.  **Restoring from a Snapshot**:

    .. code-block:: bash

        zimagi qdrant restore my_collection_name --snapshot my_snapshot_name

4.  **Cleaning Old Snapshots**:

    .. code-block:: bash

        zimagi qdrant clean my_collection_name --keep-num 3

5.  **Semantic Search (via AI Agents)**: AI agents leverage Qdrant for semantic search. For example, the `encoder` agent processes search requests by encoding query text and performing a similarity search in Qdrant.

Qdrant management is essential for building powerful AI-driven search and recommendation systems within Zimagi.
