Zimagi Command System Specification Guide
========================================

Overview
--------

This guide provides comprehensive instructions for generating and updating Zimagi command specifications and implementations within Zimagi modules. Zimagi uses a meta-programming architecture where command behavior is defined through YAML specifications that generate dynamic parent classes, which are then extended by Python implementations.

**Important**: All new commands, command mixins, and base commands must be added within Zimagi modules (separate Git projects), not in the Zimagi core project. The core project provides the framework, while modules extend it with custom functionality.

Architecture Components
-----------------------

1. **Command Specifications** (lib/modules/[module_name]/spec/): YAML files defining command structure, parameters, and behavior
2. **Command Implementations** (lib/modules/[module_name]/commands/): Python classes containing execution logic
3. **Command Mixin Implementations** (lib/modules/[module_name]/commands/mixins/): Python classes containing reusable execution logic
4. **Base Command System** (app/systems/commands/): Core framework providing meta-programming capabilities
5. **API Integration** (app/systems/api/command/): Automatic API endpoint generation

Command Tree Structure
----------------------

All commands exist in a hierarchical command tree that can be completely defined by the user. The top-level commands are directly accessible as top-level paths in the command API or CLI. For example:

.. code-block:: bash

    # Top level command
    zimagi mycommand

    # Nested command
    zimagi myservice mycommand

The command tree structure is defined through the specification hierarchy which must match precisely the directory hierarchy within the commands directory and determines both CLI accessibility and API endpoint paths.

Command Generation Process
--------------------------

1. Define specification in lib/modules/[module_name]/spec/
2. System generates parent command class that inherits from base command class via meta-programming
3. Create implementation class extending generated parent class in lib/modules/[module_name]/commands/
4. Add exec() method with business logic
5. System automatically creates API endpoints based on command tree position

Phase 1: Understanding Command Specifications
============================================

Specification Structure
-----------------------

Command specifications are defined in YAML format with the following hierarchy:

.. code-block:: yaml

    command:
      [command_name]:
        [subcommand_name]:
          base: [base_command_name]
          [properties]: [values]
          parameters:
            [param_name]:
              parser: [flag|variable|variables|fields]
              [properties]: [values]
          parse:
            - [parameter_names]

Key Properties
--------------

- **base**: Specifies the base command class to inherit from
- **priority**: Execution priority (lower numbers occur first in help lists)
- **background**: Whether command runs in background (async in an automatically managed Celery worker)
- **confirm**: Whether confirmation is required before execution
- **api_enabled**: Whether API endpoint is generated
- **mcp_enabled**: Whether command is available via MCP protocol
- **worker_type**: Type of worker to execute command
- **groups_allowed**: User groups permitted to execute command

Parameter Types
---------------

1. **flag**: Boolean toggle parameters
2. **variable**: Single value parameters
3. **variables**: Multiple value parameters (comma-separated on CLI or list in JSON)
4. **fields**: Key-value pair parameters (field=value on CLI or dictionary in JSON)

Common Parameter Properties
---------------------------

- **parser**: Type of parameter (flag, variable, variables, fields)
- **type**: Item data type (str, int, float, bool)
- **optional**: Flag for optional parameters (false for required, true for optional argument name, --[field name] for option name)
- **default**: Default value
- **help**: Help text description
- **value_label**: Label for value in help text
- **tags**: Categorization tags (add mcp tag if this parameter should be included in MCP API if mcp_enabled on command specification)
- **system**: Whether parameter is system-only
- **choices**: List of valid value options

Phase 2: Analyzing Existing Commands
====================================

Base Command Types
------------------

Examine app/spec/base/command.yml to understand available base commands:

- **platform**: Platform management commands
- **host**: Host management commands
- **user**: User management commands
- **config**: Configuration commands
- **module**: Module management commands
- **db**: Database commands
- **cache**: Cache management commands
- **log**: Log management commands
- **agent**: Service agent commands

Zimagi modules can also add new base commands that have different configuration variations.

Common Patterns
---------------

1. Action Commands:
   - Direct implementation with custom parameters
   - Use mixins for additional functionality
   - Define exec and optional parse methods

2. Agent Commands:
   - Background controller managed service commands
   - Use process-based architecture that can run multiple processes concurrently
   - Implement specific process methods
   - Usually implement the listen and send methods from the base agent command library

Note: Resource management commands (list, get, save, remove, clear) are automatically generated during the Zimagi build process based on data models. See build-spec.rst for details on how these are created.

Phase 3: Command Specification Creation
======================================

Step 1: Identify Command Purpose
--------------------------------

Determine what the command should accomplish:
- Action execution (one-time operations)
- Background processing (continuous operations)
- Data processing (import/export/transform)

Step 2: Select Base Command
---------------------------

Choose appropriate base from app/spec/base/command.yml or design your own:
- For actions: use platform, user, config, etc.
- For background services: use agent

Step 3: Define Parameters
-------------------------

Based on command purpose, define required parameters:
- Use existing mixins for common functionality
- Design your own command mixins for new reusable parameters and optional method implementations
- Define custom parameters for unique requirements
- Apply appropriate parser types
- Set sensible defaults

Step 4: Configure Properties
----------------------------

Set command properties based on requirements:
- priority: Lower for frequently used commands
- background: True for long-running operations
- confirm: True for destructive operations
- api_enabled: False for CLI-only commands
- groups_allowed: Restrict to appropriate user groups

Creating Base Command Specifications
====================================

Base commands provide reusable configuration templates that can be inherited by multiple commands within a module or across modules. They establish common behavior, parameters, and access controls.

Base Command Structure
----------------------

Base commands are defined in lib/modules/[module_name]/spec/base/command.yml or in module-specific base command files:

.. code-block:: yaml

    command_base:
      [base_name]:
        groups_allowed: [admin]
        background: false
        priority: 10
        mixins: [mixin1, mixin2]
        parameters:
          common_param:
            parser: variable
            type: str
            optional: '--common'
            help: 'Common parameter for all inheriting commands'
            tags: [common]

Inheriting Base Commands
------------------------

Commands can inherit from base commands using the base property:

.. code-block:: yaml

    command:
      my_command:
        base: [base_name]
        # Override or extend base properties
        groups_allowed: [admin, user]
        # Add specific parameters
        parameters:
          specific_param:
            parser: variable
            type: str
            optional: false
            help: 'Specific parameter for this command'

Creating Command Mixin Specifications
====================================

Command mixins provide reusable parameter combinations and method implementations that can be included in multiple commands. They are defined in lib/modules/[module_name]/spec/mixins/command.yml or in module-specific mixin files.

Mixin Structure
---------------

Mixins are defined with a class name and can include meta properties, parameters, and method implementations:

.. code-block:: yaml

    command_mixins:
      [mixin_name]:
        class: [MixinClassName]
        parameters:
          [param_name]:
            parser: [flag|variable|variables|fields]
            [properties]: [values]

Using Mixins in Commands
------------------------

Commands can include multiple mixins using the mixins property:

.. code-block:: yaml

    command:
      my_command:
        base: platform
        mixins: [mixin1, mixin2]
        parameters:
          # Command-specific parameters

Mixin Implementation
--------------------

Mixin implementations are created in lib/modules/[module_name]/commands/mixins/ and can provide both parameter parsing and method implementations that are automatically available to inheriting commands.

Phase 4: Implementation Creation
================================

Step 1: Create Implementation Class
----------------------------------

Create Python file in lib/modules/[module_name]/commands/ with class structure:

The command specification YAML path should directly match the directory path in the command tree for the command.

.. code-block:: python

    from systems.commands.index import Command

    class [CommandName](Command("[spec_path]")):
        def exec(self):
            # Implementation logic here
            pass

Step 2: Implement Business Logic
--------------------------------

In the exec() method, implement the command's functionality:
- Access parameters via generated property accessors
- Use mixin methods for common operations
- Handle errors appropriately
- Provide user feedback via message methods

Step 3: Leverage System Capabilities
------------------------------------

Utilize built-in functionality:
- self.[parameter_name] for parameter access
- self.success(), self.warning(), self.error(), self.info(), etc. for user feedback
- self.run_list() for parallel processing
- self.run_exclusive() for mutex operations
- Mixin methods for specialized functionality

Phase 4: Detailed Implementation Guide
=====================================

Parameter Access Patterns
-------------------------

All parameters defined in specifications are automatically available as properties:

.. code-block:: python

    # For variable parameter
    value = self.parameter_name

    # For variables parameter (returns list)
    values = self.parameter_names

    # For fields parameter (returns dict)
    fields = self.parameter_fields

Common Implementation Patterns
------------------------------

1. Simple Action Execution:

.. code-block:: python

    def exec(self):
        # Process parameter
        name = self.resource_name

        # Perform action
        result = self.do_something(name)

        # Provide feedback
        self.success(f"Successfully processed {name}: {result}")

2. Background Processing:

.. code-block:: python

    def exec(self):
        # Listen for events
        for package in self.listen("channel:name"):
            # Process event
            self.process_event(package.message)

            # Send response
            self.send("response:channel", result)

API Endpoint Generation
-----------------------

API endpoints are automatically generated based on:
- Command path in specification hierarchy
- api_enabled property
- Parameter definitions
- User access controls

The endpoint will be available at: <command.api.host>/[command]/[subcommand]/...

The command API endpoint accepts a POST parameter / value dictionary and streams newline separated JSON messages that are generated by the message commands like self.info(), self.success(), self.warning(), self.data(), and self.table, and self.error().

Message Functions and Cross-Platform Behavior
============================================

Zimagi provides several message functions that allow commands to communicate status, results, and errors to users. These functions behave differently depending on the execution context (CLI, Command API, MCP API, or background workers), but the core interface remains consistent.

Message Function Types
----------------------

The following message functions are available in all command implementations:

1. **self.info(message, name=None, prefix=None, log=True, system=False)**
   - General informational messages
   - Used for standard command output

2. **self.data(label, value, name=None, prefix=None, silent=False, system=False, log=True)**
   - Structured data output
   - Useful for programmatic consumption
   - Provide a name parameter to help with access on the client with the same name adding to a list

3. **self.table(data, name=None, prefix=None, silent=False, system=False, row_labels=False, log=True)**
   - Tabular data presentation
   - Good for lists and structured information
   - Provide a name parameter to help with access on the client

4. **self.warning(message, name=None, prefix=None, system=False, log=True)**
   - Non-fatal warning messages
   - Indicates potential issues

5. **self.notice(message, name=None, prefix=None, system=False, log=True)**
   - Important informational messages
   - More prominent than standard info

6. **self.success(message, name=None, prefix=None, system=False, log=True)**
   - Success confirmation messages
   - Indicates successful completion of operations

7. **self.error(message, name=None, prefix=None, system=False, terminate=True, traceback=None, error_cls=CommandError, silent=False)**
   - Error messages that can terminate execution
   - Critical for error handling
   - Raises a error_cls exception if terminate option is true

Common Parameters
-----------------

All message functions accept these common parameters:

- **message/label/value/data**: The main content to display
- **name**: Identifier for the message (used in API contexts)
- **prefix**: Prefix text for the message
- **system**: Whether this is a system message (may be hidden from regular users)
- **log**: Whether to log the message
- **silent**: Whether to suppress display (still logged and sent via API)

Behavior Across Execution Contexts
----------------------------------

CLI Execution
~~~~~~~~~~~~~

In CLI mode, messages are displayed directly to the terminal with appropriate coloring:

- info(): Standard output with default coloring
- data(): Label in key color, value in value color
- table(): Formatted table output with header coloring
- warning(): Yellow warning text
- notice(): Notice text with special formatting
- success(): Green success text
- error(): Red error text with optional traceback

Command API Execution
~~~~~~~~~~~~~~~~~~~~~

In Command API mode, messages are streamed as newline-separated JSON objects:

- Each message function generates a specific message type
- Messages include metadata like type, name, and content
- Data is encrypted based on user permissions
- Messages are streamed in real-time as they're generated

MCP API Execution
~~~~~~~~~~~~~~~~~

In MCP API mode, messages are formatted for LLM consumption:

- Simplified output format optimized for language models
- Structured data is formatted as code blocks
- Messages are categorized by type for appropriate handling
- Error messages include tracebacks when debugging is enabled

Background Worker Execution
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In background workers, messages are:

- Logged to the system log
- Stored in the command execution log
- Available for later retrieval via log commands
- Processed for notifications if configured

Implementation Examples
-----------------------

1. Simple Information Output:

.. code-block:: python

    def exec(self):
        # Basic info message
        self.info("Starting processing...")

        # Success message
        self.success("Processing completed successfully")

2. Structured Data Output:

.. code-block:: python

    def exec(self):
        results = {"processed": 100, "errors": 0}

        # Output structured data
        self.data("Processing Results", results, "results")

        # Output as table
        self.table([
            ["Metric", "Value"],
            ["Processed", results["processed"]],
            ["Errors", results["errors"]]
        ], "summary")

3. Warning and Error Handling:

.. code-block:: python

    def exec(self):
        try:
            result = self.risky_operation()
        except Exception as e:
            # Warning that doesn't stop execution
            self.warning(f"Operation had issues: {e}")
            # Continue with fallback

        try:
            critical_result = self.critical_operation()
        except Exception as e:
            # Error that terminates execution
            self.error(f"Critical operation failed: {e}")

4. Cross-Platform Compatible Output:

.. code-block:: python

    def exec(self):
        # This will work consistently across all execution contexts
        self.info("Processing data...")

        data = self.get_data()
        self.data("Retrieved Data", data, "retrieved_data")

        # Table works in all contexts but displays differently
        if data:
            self.table([
                ["ID", "Name", "Status"],
                *[[item.id, item.name, item.status] for item in data]
            ], "data_summary")

        self.success("Data processing complete")

Best Practices for Message Functions
------------------------------------

1. Use appropriate message types:
   - info() for general progress
   - data() for structured output
   - table() for tabular information
   - warning() for non-fatal issues
   - success() for completion confirmation
   - error() for problems that need attention

2. Provide meaningful names for API consumption:
   .. code-block:: python
      self.data("User Profile", profile_data, "user_profile")
      self.table(user_list, "user_list", row_labels=True)

3. Consider system vs. user messages:
   .. code-block:: python
      self.info("Internal processing step", system=True)  # Hidden from regular users and MCP commands
      self.info("Processing complete")  # Visible to all users

4. Use silent parameter for programmatic consumption:
   .. code-block:: python
      self.data("Debug Info", debug_data, silent=True)  # Logged but not displayed

5. Handle errors appropriately:
   .. code-block:: python
      try:
          self.process_data()
      except ValueError as e:
          self.error(f"Invalid data format: {e}", terminate=False)  # Continue execution
      except Exception as e:
          self.error(f"Processing failed: {e}")  # Terminate execution

Phase 5: Advanced Features
==========================

Mixins Usage
------------

Leverage existing mixins for common functionality:
- config: Configuration management
- db: Database operations
- log: Logging capabilities
- notification: User notifications
- schedule: Scheduled execution

Custom Mixins
-------------

Create new mixins in lib/modules/[module_name]/spec/mixins/command.yml when needed:
- Add parameter definitions
- Implement common methods in lib/modules/[module_name]/commands/mixins/

Error Handling
--------------

Use appropriate error handling patterns:
- self.error() for user-facing errors
- Proper exception handling for system errors
- Validation before destructive operations

Testing Considerations
----------------------

- Test parameter parsing
- Test business logic
- Test error conditions
- Test API endpoint generation
- Test user access controls

Phase 6: Complete Example
=========================

Module Structure:
::

    mymodule/
    ├── spec/
    │   ├── base/
    │   │   └── command.yml
    │   ├── mixins/
    │   │   └── command.yml
    │   └── commands/
    │       └── process.yml
    └── commands/
        ├── mixins/
        │   └── file_processor.py
        │   └── message_handler.py
        └── process.py

Base Command Specification (lib/modules/mymodule/spec/base/command.yml):

.. code-block:: yaml

    command_base:
      data_processor:
        groups_allowed: [admin, data-user]
        background: true
        mixins: [log]
        parameters:
          input_file:
            parser: variable
            type: str
            optional: '--input'
            help: 'Input file path'
            value_label: PATH
            tags: [data]
          output_format:
            parser: variable
            type: str
            default: json
            optional: '--format'
            help: 'Output format'
            choices: [json, csv, xml]
            tags: [data]

Mixin Specification (lib/modules/[mymodule]/spec/mixins/command.yml):

.. code-block:: yaml

    command_mixins:
      file_processor:
        class: FileProcessorMixin
        parameters:
          file_path:
            parser: variable
            type: str
            optional: false
            help: 'Path to file for processing'
            value_label: PATH
            tags: [file]
      message_handler:
        class: MessageHandlerMixin

Command Specification (lib/modules/[mymodule]/spec/commands/process.yml):

.. code-block:: yaml

    command:
      process:
        base: data_processor
        mixins: [file_processor, message_handler]
        priority: 200
        parameters:
          process_type:
            parser: variable
            type: str
            optional: '--type'
            help: 'Type of processing to perform'
            choices: [transform, validate, enrich]
            tags: [process]
        parse:
          - input_file
          - output_format
          - file_path
          - process_type

Mixin Implementation (lib/modules/[mymodule]/commands/mixins/file_processor.py):

.. code-block:: python

    from systems.commands.index import CommandMixin

    class FileProcessorMixin(CommandMixin("file_processor")):
        def process_file_data(self, file_path):
            # Common file processing logic
            return f"Processed data from {file_path}"

Mixin Implementation (lib/modules/[mymodule]/commands/mixins/message_handler.py):

.. code-block:: python

    from systems.commands.index import CommandMixin

    class MessageHandlerMixin(CommandMixin("message_handler")):
        def log_processing_step(self, step_name, details=None):
            """Log a processing step with optional details"""
            self.info(f"Processing step: {step_name}")
            if details:
                self.data(f"{step_name} Details", details, f"{step_name.lower()}_details")

Command Implementation (lib/modules/[mymodule]/commands/process.py):

.. code-block:: python

    from systems.commands.index import Command

    class Process(Command("process")):
        def exec(self):
            # Use message mixin for consistent logging
            self.log_processing_step("Initialization")

            # Access parameters via auto-generated properties
            input_file = self.input_file
            file_path = self.file_path
            process_type = self.process_type

            # Provide progress updates
            self.info(f"Processing file: {file_path}")
            self.info(f"Process type: {process_type}")

            # Use mixin methods if available
            processed_data = self.process_file_data(file_path)
            self.log_processing_step("File Processing", {"file": file_path, "data_size": len(processed_data)})

            # Perform business logic
            try:
                result = self.process_file(input_file, file_path, process_type, processed_data)

                # Provide success feedback with structured data
                self.success(f"Successfully processed {file_path}")

                # Output data in multiple formats for different consumption methods
                self.data("Processing Result", result, "result")

                # Provide summary table for easy scanning
                self.table([
                    ["Metric", "Value"],
                    ["File", file_path],
                    ["Process Type", process_type],
                    ["Status", "Success"],
                    ["Result Size", len(str(result))]
                ], "processing_summary")

            except Exception as e:
                # Handle errors appropriately for all contexts
                self.error(f"Failed to process file: {e}")

        def process_file(self, input_file, file_path, process_type, processed_data):
            # Implementation logic here
            return f"Processed {file_path} with {process_type}: {processed_data}"

This example demonstrates:
- Base command inheritance within a module
- Mixin inclusion with implementation
- Parameter definition and access
- Error handling
- Cross-context message output
- Data output capabilities

Phase 7: Best Practices
=======================

Specification Design
--------------------

1. Use descriptive command and parameter names
2. Provide clear help text for all parameters
3. Set appropriate defaults where possible
4. Use tags for categorization and filtering
5. Follow existing naming conventions
6. Create base commands for common patterns
7. Use mixins for reusable parameter sets

Implementation Patterns
-----------------------

1. Keep exec() method focused and readable
2. Extract complex logic to helper methods
3. Use appropriate error handling
4. Provide meaningful user feedback
5. Leverage system capabilities rather than reimplementing
6. Use mixin methods when available

Performance Considerations
--------------------------

1. Use self.run_list() for parallel processing
2. Use self.run_exclusive() for mutex operations
3. Consider background processing for long operations
4. Optimize database queries
5. Cache expensive operations when appropriate

Security Guidelines
-------------------

1. Set appropriate groups_allowed restrictions
2. Validate user input
3. Check access controls for sensitive operations
4. Sanitize output data
5. Follow principle of least privilege

Maintenance Tips
----------------

1. Keep specifications and implementations in sync
2. Document complex business logic
3. Follow consistent coding patterns
4. Test thoroughly before deployment
5. Monitor command usage and performance

Conclusion
----------

This specification guide provides a comprehensive framework for generating Zimagi commands within modules. By following these patterns and leveraging the system's meta-programming capabilities, you can efficiently create robust, maintainable commands with automatic API integration. Remember that resource management commands are automatically generated during the build process and should not be manually created.

All commands exist within a hierarchical command tree that determines both CLI accessibility and API endpoint paths. The top-level commands are directly accessible as top-level paths in the command API or CLI, making it easy to organize and access your custom functionality.
