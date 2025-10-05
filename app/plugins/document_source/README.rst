=====================================================
README for Directory: app/plugins/document_source
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is responsible for providing a standardized interface for integrating with various external document storage services. It abstracts the complexities of different APIs, allowing the application to download and process documents from diverse sources consistently.

**Key Functionality**
   *   Standardized document download from external services.
   *   Handling of service-specific authentication and API interactions.
   *   Conversion and processing of documents into a unified format for the application.
   *   Management of document metadata and versioning.

Dependencies
-------------------------

The code in this directory relies on several external libraries and internal components:
*   **`google-api-python-client`**: For interacting with Google Drive APIs.
*   **`google-auth-httplib2`**: For handling HTTP client authentication with Google APIs.
*   **`google-auth-oauthlib`**: For OAuth 2.0 authentication flows with Google services.
*   **`python-dateutil`**: For robust parsing of various date and time string formats.
*   **`django.conf.settings`**: To access application-wide configuration, such as API keys and project IDs.
*   **`systems.plugins.index.BaseProvider`**: The base class for all document source providers, defining the common interface.
*   **`utility.filesystem`**: For file system operations like saving files.
*   **`utility.data`**: For data manipulation, including JSON dumping.

File Structure and Descriptions
-------------------------------

**app/plugins/document_source/google_drive.py**
     **Role:** This file implements the document source provider specifically for Google Drive.
     **Detailed Description:** This module contains the `Provider` class, which extends `BaseProvider` to interact with the Google Drive API. It handles authentication using service accounts, lists files and folders, and downloads documents, including native Google Workspace files (like Docs, Sheets, Slides) by exporting them to standard formats (e.g., .docx, .xlsx, .pptx). It also manages file metadata, such as modification times and MD5 checksums, to determine if a file needs to be re-downloaded. The module ensures that downloaded files are saved to the local filesystem and then processed by the application's file parsing mechanism.

**app/plugins/document_source/base.py**
     **Role:** This file defines the abstract base class for all document source providers.
     **Detailed Description:** This module contains the `BaseProvider` class, which serves as the foundational interface for any document source integration. It inherits from `systems.plugins.index.BasePlugin` and enforces the implementation of a `download` method, which is crucial for any concrete document source provider. It also provides a common utility method, `_parse_file`, which delegates the task of parsing a downloaded file to the application's command system, ensuring consistent post-download processing across all document sources.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The application's command system (not directly in this directory) initiates a document download request, specifying a document source type (e.g., 'google_drive') and target folders.
   2.  The `BaseProvider` (from `app/plugins/document_source/base.py`) is instantiated for the specified source type.
   3.  The `download` method of the specific provider (e.g., `app/plugins/document_source/google_drive.py`) is invoked.
   4.  The provider handles authentication and API calls to the external document service.
   5.  It recursively traverses folders and files, downloading or exporting them to the local filesystem.
   6.  For each downloaded file, the provider calls `_parse_file` (defined in `base.py`), which in turn submits a `file:parse` command to the application's command system for further processing.

**External Interfaces**
   *   **Google Drive API**: The `google_drive.py` provider directly interacts with the Google Drive API for file listing, metadata retrieval, and content download/export.
   *   **Local Filesystem**: Both providers interact with the local filesystem to save downloaded documents and their parsed content.
   *   **Application Command System**: The `_parse_file` method in `base.py` acts as an interface to the broader application's command processing system, specifically invoking the `file:parse` command.
   *   **Django Settings**: Both providers access `django.conf.settings` to retrieve configuration parameters necessary for their operation (e.g., Google Drive API credentials).
