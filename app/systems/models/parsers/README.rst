=====================================================
README for Directory: app/systems/models/parsers
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is responsible for defining and managing various parsing functionalities within the Zimagi application. It provides a flexible and extensible framework for interpreting and processing different types of input, such as filter expressions, field assignments, data transformations, and ordering specifications, using a PLY (Python Lex-Yacc) based approach.

**Key Functionality**
   *  Parsing of complex filter expressions for data querying.
   *  Handling of field assignments and transformations using field processors.
   *  Interpretation of database functions and their parameters.
   *  Processing of data structures like lists and dictionaries within expressions.
   *  Defining custom ordering logic for query results.


Platform and Dependencies
-------------------------

**Target Platform/Environment**
   This code is designed for execution within a Python 3.x environment, specifically leveraging the Django framework for database interactions and the PLY library for parsing. It is intended to run within the Zimagi application's server-side components.

**Local Dependencies**
   *  `ply`: A Python Lex-Yacc library that provides the lexical analysis and parsing capabilities.
   *  `django.db.models.F`: Utilized for creating database expressions, allowing references to model fields and performing database-level operations.
   *  `logging`: Standard Python library for logging events and debugging information during parsing.
   *  `utility.data`: An internal Zimagi utility for data manipulation, including JSON dumping and loading, and collection management.


File Structure and Descriptions
-------------------------------

**app/systems/models/parsers/order.py**
     **Role:** Defines the parser for handling ordering expressions in queries.
     **Detailed Description:** This file contains the `OrderParser` class, which extends `BaseParser` to provide specific rules for parsing order-by clauses. It supports both ascending and descending order for fields and database functions, allowing users to specify how query results should be sorted. It processes field names and database functions, optionally prefixed with a dash (`-`) or tilde (`~`) for descending order.

**app/systems/models/parsers/fields.py**
     **Role:** Implements the parser for field assignment and processing within expressions.
     **Detailed Description:** The `FieldParser` class in this file extends both `FieldProcessorParser` and `BaseParser`. It is designed to parse expressions that involve assigning values to fields or applying field processors to them. It handles direct value assignments to fields and integrates with `FieldProcessor` objects to apply complex transformations to field data.

**app/systems/models/parsers/function.py**
     **Role:** Provides a specialized parser for database function expressions.
     **Detailed Description:** This file contains the `FunctionParser` class, which is a simplified parser focused solely on recognizing and processing database function calls. It extends `BaseParser` and primarily uses the `p_expression_db_function` rule to identify and interpret database functions within a given expression, returning the Django `F` object representation of the function.

**app/systems/models/parsers/README.rst**
     **Role:** This file provides comprehensive documentation for the `app/systems/models/parsers` directory.
     **Detailed Description:** This README.rst file serves as the primary documentation for the parsing system, outlining its purpose, key functionalities, dependencies, file structure, and execution flow. It is intended to provide a high-level overview and detailed descriptions of each component within the directory for developers and AI models.

**app/systems/models/parsers/data_processors.py**
     **Role:** Defines the structure and parsing logic for generic data processors.
     **Detailed Description:** This file introduces the `DataProcessor` class, a representation of a data transformation operation, and the `DataProcessorParser` class. The parser is responsible for interpreting expressions that involve applying data processors, which can take arguments and options. It handles the extraction of the processor name, its arguments, and options from the parsed input.

**app/systems/models/parsers/filters.py**
     **Role:** Implements the parser for filtering expressions used in data queries.
     **Detailed Description:** The `FilterParser` class in this file extends `BaseParser` and is specifically designed to parse complex boolean and comparison expressions used for filtering data. It incorporates rules for numbers, strings, boolean values, field references, database functions, and parenthesized expressions, allowing for the construction of sophisticated query filters.

**app/systems/models/parsers/field_processors.py**
     **Role:** Defines the base classes and parsing rules for field-specific data processors.
     **Detailed Description:** This file contains the `FieldProcessor` class, which represents a processor applied to a specific field, and the `FieldProcessorParser` class. The parser handles expressions where a named processor is applied to a field, potentially with additional arguments and options. It is crucial for transforming or manipulating individual field values within the data processing pipeline.

**app/systems/models/parsers/base.py**
     **Role:** Provides the foundational classes and common utilities for all parsers in the system.
     **Detailed Description:** This file defines the `BaseParser` class, which serves as the abstract base for all other parsers in the directory. It sets up the PLY lexer and parser, defines common tokens (like numbers, strings, operators, parentheses), and includes fundamental parsing rules for basic data types and operations. It also provides error handling and a mechanism for dynamically attaching parser rules from subclasses.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The parsing process typically begins with an external component (e.g., a query builder or API endpoint) instantiating a specific parser from this directory, such as `FilterParser`, `FieldParser`, `OrderParser`, `FunctionParser`, or `DataProcessorParser`. The `evaluate` method of the chosen parser (inherited from `base.py`) is then called with the input string. The `base.py` module's lexer (`ply.lex`) first tokenizes the input, and then the parser (`ply.yacc`) constructs an Abstract Syntax Tree (AST) based on the defined grammar rules. Finally, the `process` method (overridden in specific parsers like `order.py`, `fields.py`, `function.py`, `data_processors.py`, and `field_processors.py`) transforms the AST into a usable representation, often Django `F` objects or custom data structures like `FieldProcessor` or `DataProcessor` instances.

**External Interfaces**
   The parsers in this directory primarily interact with the Django ORM through `django.db.models.F` objects, which represent database expressions. They also log information using the standard Python `logging` module. The `utility.data` module is used for serializing and deserializing data structures. The parsed output, typically `F` objects or custom processor objects, is then consumed by other parts of the Zimagi application, such as query builders or data transformation pipelines, to interact with the underlying PostgreSQL database.