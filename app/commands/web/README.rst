=====================================================
README for Directory: app/commands/web
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the command-line interface (CLI) commands specifically designed for interacting with web-related functionalities within the Zimagi platform. It provides tools for fetching content from web URLs and performing web searches, integrating external web services into the Zimagi ecosystem.

**Key Functionality**
   *  Fetching and processing web content from specified URLs.
   *  Performing web searches using configurable providers.
   *  Storing fetched web content and search results within the Zimagi data store.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed to run within the Zimagi server environment, which typically operates on Python 3.x and leverages Docker for containerization. It is expected to function across various Linux distributions where Docker and Python are supported.

**Local Dependencies**
   *  `systems.commands.index.Command`: This is the base class for all Zimagi CLI commands, providing core command-line parsing, execution, and output formatting capabilities.
   *  `utility.browser.Browser`: Used by the `fetch` command for web content retrieval, likely handling HTTP requests and potentially parsing HTML.
   *  `app/systems/manage/service.py`: This module is implicitly used for managing the underlying Docker containers and services that might be spun up for web-related tasks, though not directly imported by the command files themselves.


File Structure and Descriptions
-------------------------------

**app/commands/web/fetch.py**
     **Role:** Defines the `web.fetch` command, responsible for retrieving content from a given URL.
     **Detailed Description:** This file contains the `Fetch` class, which inherits from `Command`. It implements the `exec` method to perform the web content fetching operation. It utilizes internal Zimagi helper methods like `fetch_web_content` to retrieve data from a URL and `upload_file` to store the content in a specified library and path. The command provides feedback on the success of the operation and displays the fetched Markdown content.

**app/commands/web/search.py**
     **Role:** Defines the `web.search` command, which allows users to perform web searches.
     **Detailed Description:** This file contains the `Search` class, also inheriting from `Command`. Its `exec` method orchestrates the web search functionality. It leverages the `search_web` helper method to query a specified web search provider with given text and a maximum number of results. Upon successful execution, it reports the number of results found and stores each result's URL and exported data within the Zimagi data store under the `web_search_results` type.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A user invokes a Zimagi CLI command, such as `zimagi web fetch <url>` or `zimagi web search <query>`.
   2.  The Zimagi command-line parser identifies the `web.fetch` or `web.search` command and instantiates the corresponding `Fetch` or `Search` class from this directory.
   3.  The `exec` method of the instantiated command is called.
   4.  For `web.fetch`, the `exec` method calls `self.fetch_web_content` (likely an inherited method from the base `Command` class or a mixin) to retrieve data from the specified URL. If a library and file path are provided, `self.upload_file` is then called to store the content.
   5.  For `web.search`, the `exec` method calls `self.search_web` (similarly, an inherited method) to perform the search. The results are then processed and stored using `self.data`.
   6.  Both commands provide user feedback via `self.success`, `self.notice`, and `self.info` methods.

**External Interfaces**
   *  **Web Services/APIs:** The commands in this directory directly interact with external web services and APIs to fetch content and perform searches. This involves making HTTP requests to various URLs and search engine endpoints.
   *  **Zimagi Data Store:** Fetched web content and search results are stored within the Zimagi platform's internal data store, making them accessible for further processing or retrieval by other Zimagi components.
   *  **File System:** When `web.fetch` is used to save content, it interacts with the underlying file system (managed by Zimagi's file storage mechanisms) to persist the retrieved data.
