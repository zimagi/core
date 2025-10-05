=====================================================
README for Directory: app/commands/agent
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the agent-based command implementations within the Zimagi platform. These agents are specialized, long-running processes designed to listen for specific events or messages, perform designated tasks, and interact with various internal and external services. They form the backbone of Zimagi's asynchronous processing and automation capabilities.

**Key Functionality**
   *   Asynchronous task execution and event handling.
   *   Integration with external services like web browsers, language models, and vector databases.
   *   Data processing, encoding, and archival.
   *   System monitoring and resource management for other agents.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is primarily designed for execution within a Dockerized environment, specifically leveraging Python 3.x. It integrates with Docker Compose for service orchestration and relies on a Linux-based container runtime.

**Local Dependencies**
   *   `systems.commands.index.Agent`: The base class for all agents, providing core messaging and execution capabilities.
   *   `utility.data.Collection`: Used for flexible data handling and message parsing.
   *   `django.conf.settings`: Accesses application-wide configuration settings.
   *   `services.celery.app`: Integrates with Celery for task queuing and worker management.
   *   `docker`: Python client for Docker, used for managing containers and images.
   *   `qdrant_client`: Client library for interacting with the Qdrant vector database.
   *   `selenium`: Used for web browser automation.


File Structure and Descriptions
-------------------------------

**app/commands/agent/archiver.py**
     **Role:** Handles the archival of system events, specifically scaling events for workers.
     **Detailed Description:** This agent listens for `worker:scaling` messages, which contain information about worker scaling activities. Upon receiving such a message, it records the details of the scaling event, including command, worker type, counts, and timestamps, into a persistent storage. This provides an audit trail and historical data for system resource management.

**app/commands/agent/file_parser.py**
     **Role:** Provides functionality to parse various file types and extract their textual content.
     **Detailed Description:** This agent listens for `file:parse` messages, which include a file path. It determines the file type based on its extension and then uses appropriate file parser plugins to extract the text content from the file. The extracted text is then sent back to the original sender, enabling other parts of the system to process file contents.

**app/commands/agent/controller.py**
     **Role:** Manages and orchestrates the scaling and lifecycle of other Zimagi agents.
     **Detailed Description:** The controller agent is responsible for monitoring the desired state of other agents and adjusting their worker counts accordingly. It collects agent specifications, checks their scheduling, and uses a worker provider (e.g., Docker or Kubernetes) to scale agents up or down. It also records its own activity to indicate its operational status.

**app/commands/agent/language_model.py**
     **Role:** Facilitates interaction with language models for text generation and processing.
     **Detailed Description:** This agent listens for `language_model:generate` requests, which contain messages and options for a language model. It loads the appropriate language model provider based on the user's configuration, sends the request for text generation, and then returns the generated response, including metrics like token usage and cost, to the sender. It also handles potential errors during the language model interaction.

**app/commands/agent/qdrant.py**
     **Role:** Manages backup, cleaning, and restoration operations for the Qdrant vector database.
     **Detailed Description:** This agent listens for database-related messages specifically targeting Qdrant, such as `db:backup:init`, `db:clean`, and `db:restore:init`. It then triggers the corresponding Qdrant operations, including creating snapshots, cleaning old snapshots, and restoring the database from a snapshot, ensuring data integrity and recoverability for vector embeddings.

**app/commands/agent/encoder.py**
     **Role:** Handles the encoding of text into vector embeddings and manages interactions with Qdrant for storage and search.
     **Detailed Description:** The encoder agent processes requests to save, search, or remove text embeddings. For saving, it splits text into sections, encodes them into vectors using a configured encoder, and stores them in a Qdrant collection. For searching, it encodes query text and performs a similarity search in Qdrant. It also manages the removal of embeddings based on specified filters.

**app/commands/agent/browser.py**
     **Role:** Provides web browsing capabilities, specifically for fetching HTML content from URLs.
     **Detailed Description:** This agent listens for `browser:request` messages containing a URL. It uses a headless web browser (Selenium) to navigate to the specified URL, fetch its HTML source code, and return the content along with the final URL. It also captures and reports metrics such as HTML length, execution time, and memory usage for each browsing request.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The agents in this directory are primarily event-driven. The `app/commands/agent/controller.py` acts as a central orchestrator, periodically checking the desired state of other agents and scaling them up or down. Individual agents like `archiver.py`, `file_parser.py`, `language_model.py`, `qdrant.py`, `encoder.py`, and `browser.py` operate by listening for specific messages on designated channels. When a message is received, an agent processes the request, potentially interacting with other services or plugins, and then sends a response or completion message.

**External Interfaces**
   *   **Message Queues (Celery/Redis):** All agents communicate asynchronously via message queues, primarily managed by Celery and backed by Redis. This is the main mechanism for inter-agent communication and task distribution.
   *   **Qdrant Vector Database:** The `encoder.py` and `qdrant.py` agents directly interact with the Qdrant vector database for storing, searching, and managing vector embeddings.
   *   **PostgreSQL Database:** Agents may indirectly interact with the PostgreSQL database through the Zimagi ORM for persisting system state or configuration.
   *   **External Language Model APIs:** The `language_model.py` agent connects to various external language model providers (e.g., OpenAI, Hugging Face) to perform text generation tasks.
   *   **Web Browsers (Selenium):** The `browser.py` agent utilizes a headless web browser (Selenium) to fetch web content, effectively acting as an interface to the public internet.
   *   **Docker Daemon:** The `app/systems/manage/service.py` (which `ManagerServiceMixin` is part of) interacts with the Docker daemon to manage the lifecycle of agent containers.
