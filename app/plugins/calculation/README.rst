=====================================================
README for Directory: app/plugins/calculation
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as a central repository for various mathematical and statistical calculation plugins within the larger application. It provides a standardized interface for defining and executing different types of calculations on data managed by the system.

**Key Functionality**
   *   Standardized calculation execution through a base plugin.
   *   Implementation of common arithmetic operations (addition, subtraction, multiplication, division).
   *   Statistical calculations such as standard deviation, z-score, and coefficient of variation.
   *   Data transformation utilities like min-max scaling and percentage change.
   *   Integration with a dynamic function loading mechanism for date and time operations.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for execution within a Python 3.x environment, specifically integrated with the Django framework and the Zimagi plugin system. It operates within a Dockerized environment as part of the broader Zimagi application.

**Local Dependencies**
   *   `systems.plugins.index.BaseProvider`: The core base class for all calculation plugins, providing common functionality and integration with the Zimagi plugin system.
   *   `django.conf.settings`: Used for accessing application-wide settings and configurations.
   *   `utility.data`: Provides utility functions for data manipulation, such as `ensure_list` for consistent data handling.
   *   `utility.text.Template`: Used for string interpolation and dynamic value replacement within plugin configurations.
   *   `datetime` and `timedelta`: Python's built-in modules for handling date and time objects and durations.
   *   `statistics`: Python's built-in module for common mathematical statistics functions like `mean` and `stdev`.
   *   `yaml`: Used for parsing YAML configurations, particularly for rendering record data in error messages.

File Structure and Descriptions
-------------------------------

**app/plugins/calculation/functions**
     **Role:** This is a directory containing Python modules that define various date and time-related utility functions.
     **Detailed Description:** This subdirectory holds Python files, each potentially defining one or more functions related to date and time manipulation. These functions are dynamically loaded by the `base.py` plugin to extend the capabilities of calculation providers, allowing them to perform complex date and time arithmetic or conversions.

**app/plugins/calculation/pchange.py**
     **Role:** Implements the percentage change calculation.
     **Detailed Description:** This file defines a `Provider` class that inherits from `BaseProvider`. Its `calc` method computes the percentage change between two input values (`p.a` and `p.b`), returning the result as a float. It includes a check to prevent division by zero and ensures valid inputs before performing the calculation.

**app/plugins/calculation/subtraction.py**
     **Role:** Implements the subtraction calculation.
     **Detailed Description:** This file contains a `Provider` class that extends `BaseProvider`. The `calc` method in this provider performs the subtraction of `p.a` from `p.b`, returning the difference. It includes input validation to ensure both operands are not `None` before proceeding.

**app/plugins/calculation/multiplication.py**
     **Role:** Implements the multiplication calculation.
     **Detailed Description:** This file defines a `Provider` class for multiplication. The `calc` method takes two parameters, `p.a` and `p.b`, and returns their product. It incorporates a check to ensure both input values are valid before executing the multiplication.

**app/plugins/calculation/min_max_scale.py**
     **Role:** Implements the min-max scaling calculation for a list of values.
     **Detailed Description:** This file provides a `Provider` class that calculates the min-max scaled value of the last element in a list relative to the minimum and maximum values within that list. The `calc` method handles lists of numbers, ensuring that the range is not zero to avoid division errors.

**app/plugins/calculation/zscore.py**
     **Role:** Implements the z-score calculation for a list of values.
     **Detailed Description:** This file defines a `Provider` class that computes the z-score of the last element in a given list of numerical values. It utilizes the standard deviation and mean of the list, ensuring that the standard deviation is not zero to prevent calculation errors.

**app/plugins/calculation/cov.py**
     **Role:** Implements the coefficient of variation calculation.
     **Detailed Description:** This file contains a `Provider` class that calculates the coefficient of variation (CoV) for a list of numerical data. The `calc` method uses the standard deviation and mean of the input data, including a check to prevent division by zero if the mean is zero.

**app/plugins/calculation/division.py**
     **Role:** Implements the division calculation.
     **Detailed Description:** This file defines a `Provider` class for performing division. Its `calc` method divides `p.a` by `p.b`, returning the quotient. It includes crucial validation to ensure both operands are not `None` and that the divisor (`p.b`) is not zero.

**app/plugins/calculation/addition.py**
     **Role:** Implements the addition calculation.
     **Detailed Description:** This file provides a `Provider` class that performs addition. The `calc` method adds `p.a` and `p.b`, returning their sum. It includes a check to ensure both input values are valid before performing the addition.

**app/plugins/calculation/stdev.py**
     **Role:** Implements the standard deviation calculation for a list of values.
     **Detailed Description:** This file defines a `Provider` class that calculates the standard deviation of a given list of numerical values. The `calc` method directly uses Python's `statistics.stdev` function after preparing the input list.

**app/plugins/calculation/base.py**
     **Role:** Provides the foundational `BaseProvider` class for all calculation plugins and handles dynamic function loading.
     **Detailed Description:** This is the core file for the calculation plugin system. It defines `BaseProvider`, which all specific calculation plugins inherit from. It includes methods for input validation (`check`), error handling (`set_null`, `abort`), data processing (`process`, `process_item`), and interaction with the application's facade system for loading and saving data. Crucially, it dynamically loads functions from the `app/plugins/calculation/functions` directory, making them globally available to calculation providers. It also manages parameter collection, value interpolation, and integration with validator and formatter plugins.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow typically begins when a command or process within the Zimagi application triggers a calculation. This involves instantiating a specific calculation `Provider` (e.g., `addition.py`, `zscore.py`) through the Zimagi plugin system. The `BaseProvider` in `base.py` acts as the entry point for processing. It loads items from a data facade based on configured filters, then iterates through each item, calling the specific `calc` method implemented in the child provider (e.g., `pchange.py`). The `calc` method performs the actual computation, potentially utilizing dynamically loaded functions from the `functions` directory. After calculation, `base.py` handles value validation and formatting before saving the result back to the data facade.

**External Interfaces**
   The code in this directory primarily interacts with the Zimagi application's internal systems:
   *   **Zimagi Facade System:** Calculation providers heavily rely on the `command.facade()` method to retrieve and store data from various application models. This allows calculations to operate on different data types and structures managed by Zimagi.
   *   **Zimagi Plugin System:** It integrates with other plugin types, specifically `validator` and `formatter` plugins, which are invoked by `base.py` to validate and format calculated values before persistence.
   *   **Django Settings:** Accesses `django.conf.settings` for configuration details, such as the manager instance.
   *   **Filesystem:** The `base.py` module dynamically loads Python files from the `app/plugins/calculation/functions` directory, indicating a dependency on the local filesystem for extending functionality.
