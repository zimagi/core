Web Operations
==============

Zimagi provides capabilities for interacting with web resources, including fetching content from URLs and performing web searches.

Overview
--------
These features allow the platform to integrate external web services and content into its ecosystem, enabling data collection, analysis, and AI agent interactions.

Key Web Operations Features
--------------------------
*   **Web Content Fetching**: Retrieve HTML content from specified URLs.
*   **Web Search**: Perform searches using configurable providers (e.g., Google Custom Search).
*   **Content Parsing**: Extract clean, readable text from HTML.
*   **Web Crawling**: Automate the process of traversing and collecting data from websites.
*   **Browser Automation**: High-level interface for headless browser interactions (Selenium).

Web Commands (`app/commands/web`)
---------------------------------
*   **`app/commands/web/fetch.py`**: Defines the `web.fetch` command for retrieving URL content.
*   **`app/commands/web/search.py`**: Defines the `web.search` command for performing web searches.

Web Agent (`app/commands/agent/browser.py`)
-------------------------------------------
*   **`app/commands/agent/browser.py`**: Agent providing web browsing capabilities, specifically for fetching HTML.

Utility Functions (`app/utility`)
---------------------------------
*   **`app/utility/request.py`**: Utilities for making HTTP requests and URL validation.
*   **`app/utility/web.py`**: Utility for parsing web pages and extracting text.
*   **`app/utility/crawler.py`**: Implements a web crawler.
*   **`app/utility/browser.py`**: High-level interface for browser automation using Selenium.

Search Engine Plugins (`app/plugins/search_engine`)
---------------------------------------------------
*   **`app/plugins/search_engine/google.py`**: Implements Google Custom Search API.
*   **`app/plugins/search_engine/base.py`**: Defines the base class for all search engine plugins.

Using Web Operations
--------------------

1.  **Fetching Web Content**: Use the `zimagi web fetch` command.

    .. code-block:: bash

        zimagi web fetch "https://www.zimagi.com" --library my-docs --file-path "zimagi_homepage.md"

    This fetches the content of `zimagi.com` and saves it as Markdown in your library.

2.  **Performing Web Searches**: Use the `zimagi web search` command.

    .. code-block:: bash

        zimagi web search "Zimagi platform features" --max-results 5

    This performs a search and stores the results.

3.  **Browser Agent**: The `browser` agent can be scaled and used for automated web interactions.

    .. code-block:: bash

        zimagi service scale browser --count 1

    The agent listens for `browser:request` messages to fetch URLs.

4.  **Custom Search Providers**: You can extend Zimagi with your own search engine plugins by implementing `app/plugins/search_engine/base.py`.

Web operations are essential for AI agents that need to gather information from the internet or interact with web-based services.
