# Zimagi Model Parsers Directory

## Overview

The `app/systems/models/parsers` directory contains Python modules that implement parsing functionality for the Zimagi platform's data modeling system. These parsers are responsible for processing query expressions, field calculations, data transformations, and function evaluations that enable dynamic data manipulation within the platform.

This directory plays a critical architectural role by providing the parsing infrastructure that translates human-readable expressions into executable database operations. The parsers here are consumed by:

- **Developers** working on data models and query operations
- **System administrators** configuring data processing workflows
- **AI models** analyzing and generating data processing components

## Directory Contents

### Files

| File                | Purpose                                                                                         | Format |
| ------------------- | ----------------------------------------------------------------------------------------------- | ------ |
| base.py             | Implements the base parser functionality and common parsing infrastructure for all parser types | Python |
| data_processors.py  | Provides parsing capabilities for data processing pipeline expressions and transformations      | Python |
| field_processors.py | Implements parsing for field-level data processing and transformation expressions               | Python |
| fields.py           | Provides field reference and calculation parsing functionality                                  | Python |
| filters.py          | Implements query filter expression parsing for data retrieval operations                        | Python |
| function.py         | Provides database function parsing capabilities for complex operations                          | Python |
| order.py            | Implements query ordering expression parsing for result sorting                                 | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/systems/models` directory which contains the core data modeling functionality for the Zimagi platform
- **Model Facades**: Parsers are utilized by model facade classes in `app/data/*/facade.py` files for query building and data processing
- **Model Mixins**: Works with parsing functionality in `app/systems/models/mixins` for query and filter processing
- **Specifications**: Consumes data model specifications defined in `app/spec/data` for expression evaluation
- **Settings**: Integrates with database configurations defined in `app/settings` for query execution

## Key Concepts and Patterns

### Parser Architecture

The parsing system implements a modular approach to expression evaluation:

- **Base Parsing**: Common infrastructure provided by `base.py` using PLY (Python Lex-Yacc) for robust parsing
- **Specialized Parsers**: Each parser file handles specific expression types (filters, fields, functions, etc.)
- **Expression Evaluation**: Parsers convert text expressions into executable Python objects and database operations
- **Integration with Models**: Parsers work directly with Django ORM to generate efficient database queries

### Parser Types

Each parser file implements parsing for a specific domain:

- **FieldParser** (`fields.py`): Handles field assignments and calculations
- **FunctionParser** (`function.py`): Processes database function expressions
- **OrderParser** (`order.py`): Parses sorting and ordering expressions
- **FilterParser** (`filters.py`): Handles query filter expressions
- **DataProcessorParser** (`data_processors.py`): Processes data transformation pipelines
- **FieldProcessorParser** (`field_processors.py`): Handles field-level data transformations

### Naming Conventions

- Files are named by their parsing domain (fields, filters, order, etc.)
- Parser classes follow descriptive naming with `*Parser` suffix
- Token names use UPPER_CASE to match PLY conventions
- Parser rule methods use `p_*` prefix to indicate parser rules

### File Organization

Files are organized by parsing domain:

- Query filtering operations in `filters.py`
- Field calculation and reference in `fields.py`
- Result ordering in `order.py`
- Database functions in `function.py`
- Data processing pipelines in `data_processors.py`
- Field transformations in `field_processors.py`
- Common parsing infrastructure in `base.py`

### Domain-Specific Patterns

- All parsers extend the `BaseParser` class for consistent behavior
- PLY (Python Lex-Yacc) is used for robust parsing of complex expressions
- Parsers support field calculations, database functions, and data transformations
- Integration with Django's ORM for efficient database query generation
- Thread-safe parser instances for concurrent operation

## Developer Notes and Usage Tips

### Integration Requirements

These modules require:

- PLY library for parsing operations
- Django framework access for ORM integration
- Proper database configuration in settings

### Usage Patterns

- Parsers are instantiated by model facades during query building
- Expressions are evaluated through the `evaluate()` method
- Results are integrated with Django QuerySets for database operations
- Custom parsers can extend `BaseParser` for new expression types

### Dependencies

- PLY library for parsing infrastructure
- Django ORM for database integration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for data handling

### AI Development Guidance

When generating or modifying parsers:

1. Maintain consistency with the PLY-based parsing patterns
2. Ensure proper error handling with descriptive exception messages
3. Follow established patterns for token and rule definitions
4. Respect the separation of concerns between different parser types
5. Consider performance implications for parsing operations that may run frequently
6. Maintain consistency with existing naming and API patterns
7. Document all parser rules with clear docstrings explaining the grammar
8. Follow the established patterns for integration with Django ORM operations
