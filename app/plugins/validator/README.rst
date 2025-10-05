=====================================================
README for Directory: app/plugins/validator
=====================================================

Directory Overview
------------------

**Purpose**
   This directory houses a collection of reusable data validation plugins for the Zimagi platform. These plugins enforce data integrity and business rules across various parts of the application by providing mechanisms to check input values against predefined criteria.

**Key Functionality**
   *   **Data Type Validation:** Ensuring values conform to expected types like numbers, strings, or dates.
   *   **Existence and Uniqueness Checks:** Verifying if data already exists or is unique within a specified scope.
   *   **Pattern Matching:** Validating string formats against regular expressions.
   *   **Range Validation:** Checking if numerical values fall within acceptable minimum and maximum bounds.

Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for execution within a Python 3.x environment, specifically as part of the Zimagi application framework. It integrates with the Zimagi plugin system and relies on standard Python libraries.

**Local Dependencies**
   *   `systems.plugins.index`: Provides the `BaseProvider` class, which is the foundation for all validator plugins.
   *   `utility.data`: Utilized for data manipulation functions like `number` and `ensure_list`.
   *   `math`: Used for numerical operations, specifically `math.isnan` for checking "Not a Number" values.
   *   `re`: The standard Python regular expression module for pattern matching in string validation.
   *   `datetime`: The standard Python module for date and time parsing and validation.

File Structure and Descriptions
-------------------------------

**app/plugins/validator/unique.py**
     **Role:** Defines a validator plugin that checks for the uniqueness of a given value within a specified data model and optional scope.
     **Detailed Description:** This file contains the `Provider` class for the "unique" validator. It leverages the Zimagi command's facade system to query a data model and determine if a value for a particular field already exists. It can operate within a defined scope, allowing for uniqueness checks that are conditional on other record attributes. If a duplicate is found, a warning is issued, and validation fails.

**app/plugins/validator/string.py**
     **Role:** Implements a validator plugin for string values, allowing checks for emptiness and adherence to regular expression patterns.
     **Detailed Description:** This file provides the `Provider` class for the "string" validator. It ensures that a given value is indeed a string. It can be configured to disallow empty strings and to validate the string's format against a supplied regular expression pattern. If the value is not a string, is empty when not allowed, or does not match the pattern, a warning is generated, and validation fails.

**app/plugins/validator/date_time.py**
     **Role:** Provides a validator plugin to ensure that a given value represents a valid date and/or time according to specified formats.
     **Detailed Description:** This file contains the `Provider` class for the "date_time" validator. It attempts to parse the input value against one or more specified date/time formats. It handles both string and float inputs (converting floats to integers for parsing). If the value cannot be successfully parsed by any of the provided formats, a warning is issued, and validation fails. It also supports checking for non-empty values.

**app/plugins/validator/exists.py**
     **Role:** Defines a validator plugin that checks for the existence of a given value within a specified data model and optional scope.
     **Detailed Description:** This file implements the `Provider` class for the "exists" validator. Similar to the "unique" validator, it uses the Zimagi command's facade to query a data model. Its purpose is to confirm that a value for a particular field already exists in the system, optionally within a specific scope defined by other record attributes. If the value does not exist, a warning is generated, and validation fails.

**app/plugins/validator/number.py**
     **Role:** Implements a validator plugin for numerical values, including checks for type, NaN, and range constraints.
     **Detailed Description:** This file contains the `Provider` class for the "number" validator. It first attempts to convert the input value to a numerical type. It can then check if the value is "Not a Number" (NaN) if `field_nan` is set to `False`. Additionally, it supports validating if the number falls within a specified minimum (`field_min`) and maximum (`field_max`) range. If the value is not a number, is NaN when not allowed, or falls outside the defined range, a warning is issued, and validation fails.

**app/plugins/validator/base.py**
     **Role:** Serves as the abstract base class for all validator plugins, providing common initialization and a `validate` method interface.
     **Detailed Description:** This file defines the `BaseProvider` class, which all concrete validator plugins inherit from. It extends `systems.plugins.index.BasePlugin` and provides a constructor that initializes the plugin with its type, name, command context, and configuration. It includes a placeholder `validate` method that concrete validator implementations must override to provide their specific validation logic. It also offers a `warning` helper method to consistently report validation failures through the command's logging system.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  A Zimagi command or system component initiates a validation request, typically by calling a validator plugin.
   2.  The `BaseProvider` in `app/plugins/validator/base.py` is implicitly used for common setup.
   3.  A specific validator plugin (e.g., `app/plugins/validator/number.py`, `app/plugins/validator/string.py`) is instantiated.
   4.  The `validate` method of the instantiated plugin is invoked with the value to be validated and the current record.
   5.  The plugin's `validate` method performs its specific checks (e.g., type conversion, pattern matching, database lookup).
   6.  If validation fails, the plugin's `warning` method (inherited from `base.py`) is called to log the issue.
   7.  The `validate` method returns `True` for success or `False` for failure.

**External Interfaces**
   *   **Zimagi Command System:** Validator plugins interact directly with the Zimagi command system to report warnings and potentially access facade objects for data model queries (as seen in `unique.py` and `exists.py`).
   *   **Zimagi Data Models:** The `unique.py` and `exists.py` validators query Zimagi's internal data models via facades to check for data existence and uniqueness.
   *   **Standard Python Libraries:** These plugins utilize standard Python libraries such as `math`, `re`, and `datetime` for core data manipulation and validation logic.
