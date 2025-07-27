# Zimagi File Parser Plugin Directory

## Overview

The `app/plugins/file_parser` directory contains plugin implementations that provide file parsing capabilities for the Zimagi platform's data import system. These file parser plugins enable dynamic parsing of various file formats during data import workflows, allowing the platform to extract text content from different document types including PDFs, Word documents, and plain text files.

This directory plays a critical architectural role by providing swappable file parsing implementations that extend the platform's data import capabilities. The plugins work with the dynamic class generation system in `app/systems/plugins` to create runtime plugin classes based on specifications in `app/spec/plugins/file_parser.yml`. The plugins here are consumed by:

- **Developers** working on data import and file processing features
- **System administrators** configuring data import workflows
- **AI models** analyzing and generating file parsing components

## Directory Contents

### Files

| File      | Purpose                                                                                                             | Format |
| --------- | ------------------------------------------------------------------------------------------------------------------- | ------ |
| base.py   | Implements the base file parser provider class with core parsing functionality and content cleaning                 | Python |
| binary.py | Implements base provider for binary file parsers with abstract parse_content method                                 | Python |
| docx.py   | Implements DOCX file parser provider using docx2python library for Word document parsing                            | Python |
| pdf.py    | Implements PDF file parser provider with both text extraction and OCR capabilities using pdfplumber and pytesseract | Python |
| txt.py    | Implements plain text file parser provider that passes through text content with minimal processing                 | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/plugins` directory which contains plugin implementations that extend platform functionality
- **Specifications**: File parser plugin interfaces are defined in `app/spec/plugins/file_parser.yml` which drives the plugin system through YAML specifications
- **Plugin Systems**: Connects to `app/systems/plugins` for dynamic plugin generation and provider loading using the BasePlugin and BaseProvider functions
- **Command Systems**: Works with `app/commands` for command plugin integrations, particularly data import commands
- **Settings**: Uses configurations defined in `app/settings` for plugin behavior parameters like PDF OCR settings
- **Utility Systems**: Leverages utilities in `app/utility` for filesystem operations and content processing

## Key Concepts and Patterns

### Plugin Architecture

The file parser plugin system implements a specification-driven approach to plugin generation:

- **Plugin Types** are defined in YAML specifications in `app/spec/plugins/file_parser.yml` that specify interfaces and provider structures
- **Providers** are concrete implementations of file parsing operations stored in this directory
- **Base Plugin** provides common functionality that all file parser providers inherit through the BaseProvider class
- **Dynamic Generation** uses the indexing system in `app/systems/plugins/index.py` to create plugin classes at runtime

### File Parsing Operations

All file parser plugins follow consistent processing patterns based on:

- **BaseProvider**: Foundational plugin class that all file parser providers extend
- **Content Extraction**: Standardized content extraction operations performed on input files
- **Content Cleaning**: Text cleaning and normalization to remove formatting artifacts and control characters
- **Binary File Handling**: Special handling for binary files through the binary base class

### File Organization

Files are organized by file format:

- Each file parser provider has its own file named by the format it parses (e.g., `pdf.py`, `docx.py`)
- Base implementation is in `base.py`
- Binary file handling base class is in `binary.py`

### Naming Conventions

- File parser provider files are named by their specific format (e.g., `pdf.py`, `docx.py`)
- Provider classes are named `Provider` and are dynamically generated with appropriate naming
- Base plugin files are named by their functional purpose (`base.py`, `binary.py`)

### Domain-Specific Patterns

- All file parser plugins extend base plugin classes from `systems.plugins.base` through the dynamic generation system
- Plugins define parsing logic in the `parse_file` or `parse_content` methods with typed parameters
- Error handling uses custom exception classes for file parsing operations
- Content cleaning and normalization ensures consistent output across different file formats
- Binary file parsers inherit from the binary base class to indicate binary file handling requirements

## Developer Notes and Usage Tips

### Integration Requirements

These plugins require:

- Django framework access for settings and configuration management
- Proper plugin specification files in `app/spec/plugins/file_parser.yml` for plugin generation
- Access to plugin systems in `app/systems/plugins` for provider loading and dynamic class generation
- Utility functions from `app/utility` for common operations

### Usage Patterns

- File parser plugins are accessed through the indexing system using `BaseProvider("file_parser", provider_name)` function
- Implement parsers by creating Python files with Provider classes that extend BaseProvider
- Use existing parsers as templates for new implementations
- Follow established patterns for content extraction and cleaning
- Access plugin functionality through the manager's get_provider() method

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Plugin systems from `app/systems/plugins` for dynamic generation and indexing
- Plugin specifications from `app/spec/plugins/file_parser.yml` for generation
- Format-specific libraries (pdfplumber, pytesseract, pdf2image, docx2python) for specialized parsing

### AI Development Guidance

When generating or modifying file parser plugins:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with file parsing-specific exception classes
3. Follow established patterns for content extraction and cleaning operations
4. Respect the separation of concerns between different file format parsers
5. Consider performance implications for file parsing during data imports
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing parsers as examples for new implementations
10. Ensure plugin specifications in `app/spec/plugins/file_parser.yml` properly define the interface
