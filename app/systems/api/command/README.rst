=====================================================
README for Directory: app/systems/api/command
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is responsible for defining the API interface and processing logic for command execution within the Zimagi platform. It translates incoming API requests into executable commands, handles authentication and authorization, formats responses, and manages the overall lifecycle of command-driven interactions.

**Key Functionality**
   *   Exposing Zimagi commands as RESTful API endpoints.
   *   Authenticating and authorizing API requests for command execution.
   *   Serializing and deserializing command data using a custom JSON format.
   *   Handling command execution and streaming responses.
   *   Generating API schemas for available commands.


Dependencies
-------------------------

The code in this directory heavily relies on the Django REST Framework for building the API, Docker for service management, and various internal Zimagi modules for command execution, schema definition, and utility functions. Specifically, it uses `django.conf.settings`, `django.urls.path`, `rest_framework`, `systems.commands`, `systems.api`, `systems.encryption.cipher`, and `utility.data`.


File Structure and Descriptions
-------------------------------

**app/systems/api/command/schema.py**
     **Role:** Defines the structure and generation logic for the API schema of Zimagi commands.
     **Detailed Description:** This file contains the `CommandSchemaGenerator` class, which is responsible for inspecting the available Zimagi commands and generating a machine-readable schema. It uses internal `schema` objects to represent root, router, and action commands, including their fields and metadata. It also includes `CommandSchema` for defining individual command schemas, detailing their name, overview, description, and fields. This file is crucial for documenting the API and enabling clients to understand the available commands and their parameters.

**app/systems/api/command/codecs.py**
     **Role:** Provides custom encoding and decoding mechanisms for Zimagi's command API data format.
     **Detailed Description:** The `ZimagiJSONCodec` class in this file handles the serialization and deserialization of command-related data to and from a custom `application/vnd.zimagi+json` media type. It converts between raw JSON data and internal schema objects (like `schema.Root`, `schema.Router`, `schema.Action`, `schema.Field`, `schema.Object`, `schema.Array`), ensuring that complex command structures are correctly represented and parsed. It also manages key escaping and unescaping for internal use.

**app/systems/api/command/response.py**
     **Role:** Defines a specialized encrypted response class for the command API.
     **Detailed Description:** This file introduces the `EncryptedResponse` class, which extends a shared encrypted response mechanism. Its primary purpose is to ensure that responses from the command API can be encrypted, providing a secure channel for sensitive command output. It specifically sets the `api_type` to "command_api" to distinguish its context within the broader API framework.

**app/systems/api/command/auth.py**
     **Role:** Implements authentication and permission checks for the command API.
     **Detailed Description:** This file contains `CommandAPITokenAuthentication` for authenticating API requests using tokens, specifically tailored for the command API. It also defines `CommandPermission`, which determines if a user has the necessary permissions to execute a given command, taking into account special cases like webhook commands. This ensures that only authorized users can interact with the command API.

**app/systems/api/command/routers.py**
     **Role:** Dynamically generates URL routes for all API-enabled Zimagi commands.
     **Detailed Description:** The `CommandAPIRouter` class in this file is a custom router that inspects the Zimagi command tree and creates Django URL patterns for each executable command that is enabled for API access. It recursively traverses the command structure, mapping command names to API endpoints and associating them with the `views.Command` class for handling requests. This automation simplifies the process of exposing new commands via the API.

**app/systems/api/command/views.py**
     **Role:** Handles incoming HTTP requests for command execution and returns appropriate responses.
     **Detailed Description:** The `Command` class, inheriting from `APIView`, is the central point for processing command API requests. It defines the `post` method to receive command parameters, decrypts them if necessary, executes the corresponding Zimagi command, and streams the results back to the client. It also provides methods for retrieving the command's schema, host, resource, and checking execution permissions. This file orchestrates the execution of commands based on API calls.

**app/systems/api/command/renderers.py**
     **Role:** Provides a custom renderer for serializing command API schema data into Zimagi's JSON format.
     **Detailed Description:** This file defines `CommandSchemaJSONRenderer`, a custom renderer that extends `rest_framework.renderers.BaseRenderer`. Its main function is to take the internal schema objects generated by `schema.py` and serialize them into the `application/vnd.zimagi+json` format using the `ZimagiJSONCodec`. This ensures that the API schema is presented to clients in the expected custom JSON structure.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1. An incoming HTTP POST request targeting a command endpoint is received by the Django REST Framework.
   2. The `routers.py` module, having dynamically generated the URL patterns, directs the request to the `views.Command` class.
   3. `auth.py` performs authentication using `CommandAPITokenAuthentication` and then permission checks via `CommandPermission` to ensure the user is authorized to execute the command.
   4. Inside `views.Command`, the request data is processed, potentially decrypted using `systems.encryption.cipher`, and then the corresponding Zimagi command is executed.
   5. The command's output is then packaged and streamed back to the client.
   6. For schema requests, `schema.py` generates the command schema, which is then rendered into the custom JSON format by `renderers.py` using `codecs.py`.

**External Interfaces**
   *   **Zimagi Command System:** The `views.Command` interacts directly with the core Zimagi command execution system to run commands.
   *   **Django REST Framework:** This directory heavily leverages DRF for API routing, views, authentication, permissions, and rendering.
   *   **Encryption System:** `views.py` utilizes `systems.encryption.cipher` for decrypting sensitive command parameters.
   *   **Utility Modules:** It uses `utility.data` for data manipulation, normalization, and JSON handling.
   *   **Client Applications:** The API defined here serves as the primary interface for client applications to interact with Zimagi commands.
