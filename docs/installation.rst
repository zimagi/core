Installation
============

This section details the steps required to install and set up the Zimagi platform.

Dependencies
------------

Before you begin, ensure you have the following installed on your system:

*   **Python 3.x**: For server services and Python SDK development.
*   **Unix-like operating system**: Linux (preferred) or macOS.
*   **Docker and Docker Compose** (or Kubernetes and Helm): For container orchestration.
*   **Node.js 24.x**: For JavaScript SDK development.

External Libraries (Python)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Zimagi Python SDK and server components rely on a variety of external Python libraries:

*   ``Django``
*   ``Celery``
*   ``Redis``
*   ``Qdrant``
*   ``requests``
*   ``pycryptodome``
*   ``terminaltables``
*   ``validators``
*   ``pandas``
*   ``oyaml``
*   ``python-magic``
*   ``urllib3``
*   ``ply``
*   ``inflect``
*   ``jinja2``
*   ``semantic_version``
*   ``pyperclip``
*   ``rich``
*   ``Textual``
*   ``google-api-python-client``, ``google-auth-httplib2``, ``google-auth-oauthlib``
*   ``python-dateutil``
*   ``statistics``
*   ``spacy``
*   ``docling``, ``docling_ocr_onnxtr``
*   ``litellm``, ``transformers``
*   ``paramiko``
*   ``pygit2``, ``github``
*   ``pynvml``
*   ``starlette``, ``mcp``

External Libraries (JavaScript)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Zimagi JavaScript SDK relies on these libraries:

*   ``papaparse``
*   ``@babel/core``, ``@babel/preset-env``, ``@babel/preset-typescript``
*   ``@rollup/plugin-babel``, ``@rollup/plugin-commonjs``, ``@rollup/plugin-node-resolve``, ``@rollup/plugin-terser``
*   ``eslint``, ``eslint-config-prettier``, ``eslint-plugin-prettier``
*   ``jest``
*   ``prettier``
*   ``typescript``

Installation Steps
------------------

1.  **Clone the repository:**

    .. code-block:: bash

        git clone https://github.com/zimagi/core.git [project-name]

2.  **Navigate to the project directory:**

    .. code-block:: bash

        cd [project-name]

3.  **Setup project, Install dependencies, and run services:**

    The `start` script is your entry point for setting up the Zimagi environment. It handles installing dependencies and launching services.

    .. code-block:: bash

        source start [type: standard | nvidia] [environment: local | test] [configuration: default | api | api.encrypted]

    *   **`type`**: Choose `standard` for CPU-only environments or `nvidia` if you have NVIDIA GPUs and want to leverage them for AI workloads.
    *   **`environment`**: Typically `local` for development or `test` for running tests.
    *   **`configuration`**:
        *   `default`: Standard configuration.
        *   `api`: Optimized for API services.
        *   `api.encrypted`: API services with encrypted communication.

    Example for a local standard setup:

    .. code-block:: bash

        source start standard local default

4.  **Run API commands locally:**

    Once services are up, you can interact with the Zimagi CLI:

    .. code-block:: bash

        zimagi info

    This command should display information about your Zimagi platform.
