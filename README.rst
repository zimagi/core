=====================================================
[Zimagi]
=====================================================

.. Badges and status indicators go here
.. |build| image:: https://circleci.com/gh/zimagi/zimagi/tree/main.svg?style=svg
   :target: [https://circleci.com/gh/zimagi/zimagi/tree/main]
.. |pypi| image:: https://img.shields.io/pypi/v/zimagi.svg
   :target: https://pypi.org/project/zimagi/
.. |license| image:: https://img.shields.io/github/license/zimagi/core
   :target: [https://github.com/zimagi/core/blob/main/LICENSE]

|build| |pypi| |license|

Overview: The Zimagi Data Integration, AI Processing, and API Publishing Platform
---------------------------------------------------

Zimagi is an open-source platform designed for building, running, and extending AI-driven applications and services. It provides a modular, extensible, and dynamically configurable architecture for managing commands, data models, plugins, and microservices, facilitating consistent deployment and scalable operations.

Key Features
~~~~~~~~~~~~

1. **Core Platform Architecture & Extensibility**

 * Modular and extensible architecture for flexible application extension.
 * Dynamic loading, generation, and management of commands, models, and plugins.
 * Centralized management of application-wide settings and configurations.
 * Dynamic registration of Django applications and middleware.
 * Reusable mixins for common model functionalities like provider integration and access control.

2. **AI & Language Model Integration**

 * Core AI agent intelligence and interaction logic.
 * Conversational memory management for AI-driven interactions.
 * Integration with various language models (LLMs) for text generation and processing.
 * Text encoding functionalities for converting text into numerical vector representations (embeddings).
 * Integration with Qdrant vector database for semantic search and similarity matching.

3. **Data Management & Persistence**

 * Definition and management of data models and their associated database migrations.
 * Comprehensive data management, including schema evolution and caching.
 * Advanced querying capabilities with filtering, ordering, and DataFrame integration.
 * Standardized handling of resource creation and modification timestamps.
 * Support for various data formats (JSON, YAML, CSV) for serialization and deserialization.

4. **API & Communication**

 * Automatic generation of OpenAPI compatible REST APIs.
 * Integrated streaming command APIs for real-time interaction.
 * Scalable Management Control Plane (MCP) APIs for external systems and AI agents.
 * Secure API communication through authentication, authorization, and encryption.
 * Channel-based communication for inter-service messaging and event notification using Redis streams.

5. **Operations & Deployment**

 * Containerized service orchestration using Docker and Kubernetes.
 * Automated workflows and system maintenance via YAML-based task definitions.
 * Management of long-running tasks and their lifecycle, including abortion and status tracking.
 * Database management, including snapshotting, backup, restore, and cleaning operations.
 * Dynamic scaling of worker processes and agents based on demand and configuration.


Getting Started
-----------------------------

Dependencies
~~~~~~~~~~~~~~

**Platform/Environment:**
*   Python 3.x (for server services and Python SDK development)
*   Unix-like operating system (Linux - preferred, macOS)
*   Docker and Docker Compose or Kubernetes and Helm
*   Node.js 24.x (for JavaScript SDK development)

**External Libraries (Python):**
*   `Django` (for web framework, ORM, models, migrations)
*   `Celery` (for asynchronous task processing and scheduling)
*   `Redis` (for caching, message brokering, task queuing, inter-service communication)
*   `Qdrant` (vector similarity search engine)
*   `requests` (for HTTP requests)
*   `pycryptodome` (for cryptographic primitives)
*   `terminaltables` (for formatting tabular data)
*   `validators` (for URL validation)
*   `pandas` (for data manipulation, DataFrames, CSV handling)
*   `oyaml` (for YAML serialization/deserialization)
*   `python-magic` (for determining file mimetypes)
*   `urllib3` (for HTTP connection pools)
*   `ply` (Python Lex-Yacc for parsing)
*   `inflect` (for pluralization)
*   `jinja2` (for templating)
*   `semantic_version` (for version comparisons)
*   `pyperclip` (for clipboard functionality)
*   `rich` (for rich terminal output)
*   `Textual` (for TUI applications)
*   `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib` (for Google APIs)
*   `python-dateutil` (for date/time parsing)
*   `statistics` (for statistical functions)
*   `spacy` (for NLP, text splitting)
*   `docling`, `docling_ocr_onnxtr` (for document parsing)
*   `litellm`, `transformers` (for language models)
*   `paramiko` (for SSH)
*   `pygit2`, `github` (for Git/GitHub integration)
*   `pynvml` (for NVIDIA GPU management)
*   `starlette`, `mcp` (for ASGI/MCP API)

**External Libraries (JavaScript):**
*   `papaparse` (for CSV handling)
*   `@babel/core`, `@babel/preset-env`, `@babel/preset-typescript` (for Babel transpilation)
*   `@rollup/plugin-babel`, `@rollup/plugin-commonjs`, `@rollup/plugin-node-resolve`, `@rollup/plugin-terser` (for Rollup bundling)
*   `eslint`, `eslint-config-prettier`, `eslint-plugin-prettier` (for linting)
*   `jest` (for testing)
*   `prettier` (for code formatting)
*   `typescript` (for type checking)


Installation
~~~~~~~~~~~~

1. Clone the repository:
   ::
      git clone https://github.com/zimagi/core.git [project-name]

2. Navigate to the project directory:
   ::
      cd [project-name]

3. Setup project, Install dependencies, and run services:
   ::
      source start [type: standard | nvidia] [environment: local | test] [configuration: default | api | api.encrypted]

4. Run API commands locally:
   ::
      zimagi info


Project Architecture and Modules
---------------------------------------------

The codebase is organized into several key modules, each documented in detail within its respective subdirectory. The execution flow typically begins with shell scripts (e.g., `zimagi-cli.py`, `zimagi-client.py`) or Docker Compose configurations, which bootstrap the Django environment and delegate to the `app/systems/manager.py` to load and index all application components. Commands are then executed, interacting with models for data persistence, plugins for extensible functionalities, and services for API interactions or background tasks.

**Source Modules (`app/`)**
   The `app/` directory serves as the root for the entire Zimagi application codebase. It encapsulates all core functionalities, configurations, scripts, and specifications necessary to build, run, test, and extend the Zimagi platform. It manages application-wide settings, orchestrates background tasks, structures data models, specifies system components, commands, and plugins, and provides utility scripts for system operations. Key subdirectories include `settings/` for configurations, `data/` for data models, `systems/` for core functionalities, `plugins/` for extensible components, `commands/` for CLI/API commands, `services/` for microservice configurations, `templates/` for dynamic component generation, and `utility/` for reusable helper functions.

**Core API/Services**
   The Zimagi platform exposes several core APIs and services. The `app/systems/api/` directory defines and manages distinct API layers for commands, data, and the Model Context Protocol (MCP), handling authentication, authorization, encryption, routing, and schema generation. These APIs facilitate the execution of Zimagi commands and the retrieval/manipulation of data through standardized interfaces. The `app/services/` directory defines the configurations and entry points for these API services, along with background task processing via Celery.

**Documentation (`docs/`)**
   The `app/help/` directory serves as the central repository for all help documentation within the application. It organizes help content by language and command, providing descriptive overviews and detailed explanations for various functionalities. This structure ensures that both human users and AI models can easily access and understand the purpose and usage of different application commands and features.


Contributing and Development
--------------------------------------------

We welcome community contributions! Please review the contribution guide before submitting pull requests.

**Running Tests**
   The `app/tests/` directory serves as the central hub for all automated tests. To run the test suite, ensure a Docker daemon is running and Zimagi services are up. The tests interact with the Zimagi Command API and Data API, typically exposed via HTTP endpoints.
   ::
      python manage.py test

**License**
   This project is licensed under the **Apache 2 License**.
