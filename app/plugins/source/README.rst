=====================================================
README for Directory: app/plugins/source
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses the core plugin providers for data sourcing within the Zimagi platform. These plugins are responsible for loading data from various external systems and transforming it into a standardized format for further processing and integration.

**Key Functionality**
   Data ingestion from diverse sources, standardization of incoming data, and integration with the Zimagi command and facade systems for data manipulation and persistence.

Dependencies
-------------------------

The files in this directory heavily rely on the following:
*   **`pandas`**: For efficient data manipulation and handling of DataFrames.
*   **`django.conf.settings`**: To access global application settings and configurations.
*   **`systems.plugins.index.BasePlugin`**: The foundational class for all Zimagi plugins, providing common functionalities and registration mechanisms.
*   **`systems.plugins.parser.FormatterParser`**: For parsing and applying data formatting rules.
*   **`utility.data`**: A collection of utility functions for data handling, including JSON serialization/deserialization, list manipulation, and data prioritization.
*   **`logging`**: For logging events and debugging information during data processing.

File Structure and Descriptions
-------------------------------

**app/plugins/source/README.rst**
     **Role:** Provides comprehensive documentation for the `app/plugins/source` directory.
     **Detailed Description:** This file serves as the primary documentation for the data source plugin directory, detailing its purpose, key functionalities, dependencies, file structure, and execution flow. It is designed to provide a high-level overview and detailed descriptions of the core components within this module for both human developers and AI models.

**app/plugins/source/csv_file.py**
     **Role:** Implements a data source provider specifically designed to load data from CSV files.
     **Detailed Description:** This file defines the `Provider` class, which extends `BaseProvider`. It overrides the `load` method to read data from a specified CSV file, applying configurations such as separators, header presence, and data types. It leverages internal utility functions to handle file archiving and column mapping, making it a concrete implementation for CSV-based data ingestion. This file directly interacts with the `BaseProvider` to inherit common data processing and saving mechanisms.

**app/plugins/source/base.py**
     **Role:** Provides the abstract base class and common functionalities for all data source plugins.
     **Detailed Description:** This file defines the `BaseProvider` class, which all specific data source plugins (like `csv_file.py`) must inherit from. It establishes the core framework for data loading, processing, validation, and saving. Key functionalities include managing plugin configuration, handling data pagination, updating data series, and interacting with Zimagi's facade system for data persistence. It also includes methods for managing relations, field mapping, and running validators and formatters on incoming data. This file is central to how data is structured and processed across all source plugins.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A command or process initiates a data import operation, typically by calling a specific data source plugin (e.g., `csv_file.py`).
   2.  The `BaseProvider` (or its subclass, e.g., `csv_file.Provider`) is instantiated with relevant configuration.
   3.  The `process` method of the provider (defined in `base.py`) is invoked, which orchestrates the data loading.
   4.  The `load` method (overridden in specific providers like `csv_file.py`) retrieves raw data from the external source.
   5.  The `update_series` method in `BaseProvider` (from `base.py`) then takes this raw data, converts it into a Pandas DataFrame, and applies validation and formatting rules.
   6.  Finally, the `save` method in `BaseProvider` (from `base.py`) interacts with the Zimagi facade system to persist the processed data into the application's database.

**External Interfaces**
   The code in this directory primarily interacts with:
   *   **External Data Sources:** Specific providers (e.g., `csv_file.py`) read data from external files or APIs.
   *   **Zimagi Command System:** The `command` object (an instance of `systems.command.base.Command`) is used for logging, accessing other providers (validators, formatters), and interacting with facades.
   *   **Zimagi Facade System:** The `facade_index` (from `settings.MANAGER.index.get_facade_index()`) is used to retrieve and interact with model facades for saving validated data into the Zimagi database.
   *   **Filesystem:** For reading input files (e.g., CSV files) and potentially archiving them.
