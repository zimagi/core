=======================
Zimagi Build System Spec
=======================

Overview
========

The Zimagi build system uses command profiles to generate data models, roles, and commands from YAML specifications. This document describes how to create build profiles that can be executed with the ``build`` command to automatically generate the necessary specification files.

Profile Structure
=================

Build profiles are defined in ``profiles/build.yml`` files within modules. These profiles use components to generate various parts of the system:

1. **roles** - Creates role definitions
2. **models** - Creates data models using templates

Model Component
===============

The model component generates data model specifications using templates from ``app/templates/data/model``. Each model definition supports the following properties:

Data Model Template Variables
-----------------------------

These are the variables defined in ``app/templates/data/model/index.yml`` that can be used when defining models:

- ``name`` (required) - Name of data model
- ``plural_suffix`` (default: "s") - Suffix to use when many to many relationship
- ``plural`` (default: null) - Plural name of data model (overrides default: {name}{plural_suffix})
- ``base`` (default: "id_resource") - Base data model name
- ``extend`` (default: false) - Whether or not to extend the base model (``base`` field must be a regular data model)
- ``mixins`` (default: null) - Shared data / command mixins
- ``data_mixins`` (default: null) - Extra data mixins
- ``command_mixins`` (default: null) - Extra command mixins
- ``plugin`` (default: False) - Data model is a plugin and supports providers
- ``default_provider`` (default: "base") - Default model plugin provider (if plugin)
- ``command_base`` - Command prefix
- ``id`` (default: null) - Data model id field
- ``id_fields`` (default: null) - Data model id fields (for generated id)
- ``key`` (default: null) - Data model name field
- ``name_field`` (default: true) - Whether or not include a name field on the model (if false must specify 'key')
- ``unique_fields`` (default: <{ id_fields }>) - Data model unique field constraints
- ``default_ordering`` (default: <{ key }>) - Default ordering fields
- ``display`` (default: null) - Display format for model (fields are interpolated with <field> syntax)
- ``auto_create`` (default: false) - Whether or not to auto create instances on attachment to other instance types
- ``admin_roles`` (default: "admin") - Data model administrative roles
- ``view_roles`` (default: "public") - Data model view roles
- ``priority`` (default: 100) - Priority level for the model resource command set
- ``data_api`` (default: true) - Whether or not to generate data API endpoints for this model
- ``mcp_api`` (default: false) - Whether or not to generate MCP API endpoints for this model
- ``disable_ops`` (default: null) - List of disabled operations for model (options- list, retrieve, update, destroy, clear)

Model Relationship Strategies
=============================

The Zimagi build system provides three primary strategies for creating relationships between data models:

1. **Base Model Inheritance (Foreign Key Relationship)**
2. **Base Model Extension (One-to-One Relationship)**
3. **Abstract Base Models (id_resource and name_resource)**

Base Model Inheritance (Foreign Key Relationship)
-------------------------------------------------

When you specify a ``base`` model without the ``extend`` flag, you create a foreign key relationship between the child model and the parent model. This is the most common pattern where one model belongs to another.

Characteristics:
- Creates two separate database tables
- Child model has a foreign key field pointing to the parent model
- Multiple child instances can reference the same parent instance
- Child model instances cannot be accessed through parent model endpoints
- Child model inherits the fields structure but maintains separate data

Example:
.. code-block:: yaml

    # Parent model
    organization:
      base: name_resource
      display: '<name>'
      fields:
        address:
          type: string
          options:
            max_length: 256

    # Child model with foreign key relationship
    employee:
      base: organization  # References parent model
      display: '<organization_id>/<name>'  # Shows relationship in display
      fields:
        position:
          type: string
          options:
            max_length: 128
        salary:
          type: integer

    # This creates:
    # - organizations table with id, name, address
    # - employees table with id, name, organization_id (FK), position, salary
    # - Multiple employees can belong to the same organization

Base Model Extension (One-to-One Relationship)
----------------------------------------------

When you specify a ``base`` model with ``extend: true``, you create a one-to-one relationship where the child model extends the parent model with additional fields. This is used when the child is a specialized version of the parent.

Characteristics:
- Creates two database tables linked by an automatically generated reference field
- Child model instances share all fields of the parent model
- Can be accessed through parent model endpoints
- Each parent instance has exactly one extended child instance
- Child model inherits both structure and data from parent

Example:
.. code-block:: yaml

    # Parent model
    organization:
      base: name_resource
      display: '<name>'
      fields:
        address:
          type: string
          options:
            max_length: 256

    # Child model extending parent (one-to-one)
    business:
      base: organization  # References parent model
      extend: true        # Creates extension relationship
      display: '<organization_id>/business-<name>'
      fields:
        tax_id:
          type: string
          options:
            max_length: 50
        revenue:
          type: integer

    # This creates:
    # - organizations table with id, name, address
    # - businesses table with organization_id (PK, FK), tax_id, revenue
    # - Each business record extends exactly one organization record
    # - Business instances inherit organization fields and can be accessed via organization endpoints

Abstract Base Models
--------------------

Zimagi provides two abstract base models that serve as the foundation for most data models:

id_resource
~~~~~~~~~~~

The ``id_resource`` base model provides:
- Auto-generated string primary key field (64 character max)
- Name field (256 character max)
- Primary key is generated based on combination of field values specified with ``id_fields``
- Standard created/updated timestamp fields
- Default ordering by name

Use when you need:
- Auto-generated unique identifiers
- Flexible naming
- Standard resource behavior

Example:
.. code-block:: yaml

    product:
      base: id_resource
      display: '<type>: <name>'
      id_fields: [type, name]
      fields:
        type:
          type: string
          options:
            max_length: 100
        category:
          type: string
          options:
            max_length: 100
        price:
          type: float

name_resource
~~~~~~~~~~~~~

The ``name_resource`` base model provides:
- Name field as the primary key (256 character max)
- Standard created/updated timestamp fields
- Default ordering by name

Use when you need:
- Natural key identification
- Unique named resources
- Simpler data structures

Example:
.. code-block:: yaml

    category:
      base: name_resource  # Name is the primary key
      display: '<name>'
      fields:
        description:
          type: text

API Endpoint Generation
=======================

The build system automatically generates three types of API endpoints for each data model:

1. **Data API** - OpenAPI 3.1 compatible REST endpoints for CRUD operations
2. **Command API** - Streaming command endpoints for executing operations
3. **MCP API** - Model Context Protocol endpoints for LLM integration

Data API Endpoints
------------------

For each data model, the build system generates a complete set of REST endpoints:

- ``GET /{model_name}/`` - List all instances with filtering, ordering, and pagination
- ``POST /{model_name}/`` - Create a new instance
- ``GET /{model_name}/{id}/`` - Retrieve a specific instance
- ``PUT /{model_name}/{id}/`` - Update a specific instance
- ``DELETE /{model_name}/{id}/`` - Delete a specific instance
- ``GET /{model_name}/csv/`` - Export specific data fields as CSV
- ``GET /{model_name}/json/`` - Export specific data fields as JSON
- ``GET /{model_name}/values/{field}/`` - Get distinct values for a specific field
- ``GET /{model_name}/count/{field}/`` - Get count of instances grouped by field

The Data API is OpenAPI 3.1 compatible and includes automatic schema generation with field-level filtering capabilities.

Command API Endpoints
---------------------

For each data model, the build system generates command endpoints:

- ``POST /{model_name}/list`` - List instances (equivalent to GET /{model_name}/)
- ``POST /{model_name}/get`` - Retrieve instance (equivalent to GET /{model_name}/{id}/)
- ``POST /{model_name}/save`` - Create or update instance (equivalent to POST/PUT)
- ``POST /{model_name}/remove`` - Delete instance (equivalent to DELETE /{model_name}/{id}/)
- ``POST /{model_name}/clear`` - Delete all instances

The Command API uses streaming JSON responses with newline-separated messages, allowing real-time feedback during operations.

MCP API Endpoints
-----------------

When ``mcp_api: true`` is specified for a model, the build system generates Model Context Protocol endpoints that are accessible to LLMs:

- ``POST /{model_name}/list`` - List instances with simplified response format
- ``POST /{model_name}/get`` - Retrieve instance with simplified response format
- ``POST /{model_name}/save`` - Create or update instance with simplified response format
- ``POST /{model_name}/remove`` - Delete instance with simplified response format

MCP endpoints only expose parameters tagged with ``mcp`` in their field definitions and return responses formatted for LLM consumption.

API Field Configuration
-----------------------

Fields can be configured for different API exposure:

- By default, all fields are exposed in Data API
- Fields with ``mcp`` tag are exposed in MCP API when enabled
- ``system: true`` fields are hidden from regular users but available to admins
- ``editable: false`` fields are read-only in API operations

Example API Configuration:
.. code-block:: yaml

    models:
      product:
        base: name_resource
        display: '<name>'
        mcp_api: true  # Enable MCP endpoints
        fields:
          name:
            type: string
            options:
              max_length: 256
          price:
            type: float
            options:
              tags: [mcp]  # Expose in MCP API
          internal_code:
            type: string
            options:
              max_length: 50
              system: true  # Hidden from regular users
          created_by:
            type: string
            options:
              max_length: 100
              editable: false  # Read-only field

Choosing the Right Strategy
---------------------------

1. **Use base model inheritance (foreign key)** when:
   - One model "belongs to" another model
   - Multiple child instances relate to the same parent
   - You want separate data management for parent and child
   - Example: Employee belongs to Organization

2. **Use base model extension (one-to-one)** when:
   - Child model is a specialized version of the parent
   - Each parent instance has exactly one extended version
   - You want to share data and access through parent endpoints
   - Example: Business is a type of Organization with additional fields

3. **Use id_resource** when:
   - You need auto-generated unique identifiers
   - Natural keys are not suitable
   - You want flexibility in naming

4. **Use name_resource** when:
   - The name itself is a natural unique identifier
   - You want simpler primary key management
   - Examples: Categories, Tags, Configuration items

Field Template Variables
========================

Each field type has specific template variables defined in ``app/templates/field/{field_type}/index.yml``. These variables control how fields are generated in the data model specifications.

Binary Field
------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of binary field on data model
- ``nullable`` (default: true) - Whether or not this binary field can be NULL
- ``max_length`` (default: 256) - Maximum length for this field
- ``editable`` (default: true) - Whether or not this field is editable by users

Boolean Field
-------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of boolean field on data model
- ``nullable`` (default: true) - Whether or not this boolean field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users

Date Field
----------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of date field on data model
- ``nullable`` (default: true) - Whether or not this date field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users
- ``primary_key`` (default: false) - Whether or not this field is the primary key of the model

Datetime Field
--------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of datetime field on data model
- ``nullable`` (default: true) - Whether or not this datetime field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users
- ``primary_key`` (default: false) - Whether or not this field is the primary key of the model

Dictionary Field
----------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of dictionary field on data model
- ``editable`` (default: true) - Whether or not this field is editable by users

Duration Field
--------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of duration field on data model
- ``nullable`` (default: true) - Whether or not this duration field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users

Float Field
-----------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of float field on data model
- ``nullable`` (default: true) - Whether or not this float field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users
- ``primary_key`` (default: false) - Whether or not this field is the primary key of the model

Foreign Key Field
-----------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of foreign key field on data model
- ``related_data_name`` (required) - Name of data model relation
- ``reverse_related_name`` (default: null) - Name of data field for reverse relation lookup on attached data model
- ``nullable`` (default: true) - Whether or not this foreign key field can be NULL (false if default specified)
- ``on_delete`` (default: "SET_NULL") - How to handle deletion of related data (options: SET_NULL, SET_DEFAULT, CASCADE, PROTECT, RESTRICT, DO_NOTHING)
- ``editable`` (default: true) - Whether or not this field is editable by users

Integer Field
-------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of integer field on data model
- ``nullable`` (default: true) - Whether or not this integer field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users
- ``primary_key`` (default: false) - Whether or not this field is the primary key of the model

Big Integer Field
-----------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of big integer field on data model
- ``nullable`` (default: true) - Whether or not this integer field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users
- ``primary_key`` (default: false) - Whether or not this field is the primary key of the model

List Field
----------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of list field on data model
- ``editable`` (default: true) - Whether or not this field is editable by users

Many To Many Field
------------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of many to many field on data model
- ``related_data_name`` (required) - Name of data model relation
- ``reverse_related_name`` (default: null) - Name of data field for reverse relation lookup on attached data model

String Field
------------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of character field on data model
- ``nullable`` (default: true) - Whether or not this string field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``choices`` (default: null) - Choices available for field value
- ``max_length`` (default: 256) - Maximum character length for this field
- ``editable`` (default: true) - Whether or not this field is editable by users
- ``primary_key`` (default: false) - Whether or not this field is the primary key of the model

Text Field
----------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of text field on data model
- ``nullable`` (default: true) - Whether or not this text field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``editable`` (default: true) - Whether or not this field is editable by users

URL Field
---------

- ``data_name`` (required) - Name of data model
- ``field_name`` (required) - Name of URL field on data model
- ``nullable`` (default: true) - Whether or not this URL field can be NULL (false if default specified)
- ``default`` (default: null) - Default value for this field
- ``max_length`` (default: 256) - Maximum character length for this field
- ``editable`` (default: true) - Whether or not this field is editable by users

Common Field Patterns
=====================

When defining fields in your build profile, follow these common patterns:

String Fields
-------------

For simple text fields:
.. code-block:: yaml

  fields:
    name:
      type: string
      options:
        max_length: 256

For choice fields:
.. code-block:: yaml

  fields:
    status:
      type: string
      options:
        choices: [active, inactive, pending]
        max_length: 20
        default: pending

Numeric Fields
--------------

For integer fields:
.. code-block:: yaml

  fields:
    count:
      type: integer
      options:
        default: 0

For float fields:
.. code-block:: yaml

  fields:
    price:
      type: float
      options:
        nullable: true

Boolean Fields
--------------

.. code-block:: yaml

  fields:
    is_active:
      type: boolean
      options:
        default: true

Date/Time Fields
----------------

.. code-block:: yaml

  fields:
    created_at:
      type: datetime
      options:
        editable: false

Relationship Fields
-------------------

Foreign key relationships:
.. code-block:: yaml

  fields:
    category:
      type: foreign_key
      options:
        related_data_name: category
        nullable: true

Many-to-many relationships:
.. code-block:: yaml

  fields:
    tags:
      type: many_to_many
      options:
        related_data_name: tag

Collection Fields
-----------------

For list data:
.. code-block:: yaml

  fields:
    tags:
      type: list

For dictionary/JSON data:
.. code-block:: yaml

  fields:
    metadata:
      type: dict

URL Fields
----------

.. code-block:: yaml

  fields:
    website:
      type: url
      options:
        nullable: true

Field Definitions
-----------------

Fields are defined with a type and options. Common field types include:

- ``string`` - Character fields with max_length
- ``text`` - Large text fields
- ``integer`` - Integer fields
- ``float`` - Floating point fields
- ``boolean`` - True/False fields
- ``foreign_key`` - References to other models
- ``many_to_many`` - Many-to-many relationships
- ``datetime`` - Date and time fields
- ``date`` - Date only fields
- ``dict`` - Dictionary/JSON fields
- ``list`` - List/array fields
- ``url`` - URL fields
- ``binary`` - Binary data fields
- ``duration`` - Time duration fields
- ``big_integer`` - Large integer fields

Each field type uses templates from ``app/templates/field/{type}`` to generate specification files.

Role Component
==============

The roles component defines system roles with help text that describes their purpose.

Build Process
=============

When a build profile is executed with the ``build`` command:

1. Roles defined in the profile are generated using the roles component
2. Models are generated using the model component
3. For each model:
   - Data model specification is created in ``spec/auto/data/{model_name}.yml``
   - Command specification is created in ``spec/auto/commands/{model_name}.yml``
   - If plugin is true, plugin specification is created in ``spec/auto/plugins/{model_name}.yml``
4. For each field in models:
   - Field specifications are generated in the data model files using field templates
5. API endpoints are automatically generated based on model configuration

Template Generation
===================

The system uses Jinja2 templates to generate specification files:

- Data model templates: ``app/templates/data/model/*.yml``
- Field templates: ``app/templates/field/{type}/*.yml``

Templates use variables defined in the build profile to customize generated specifications.

Example Build Profile Structure
===============================

A complete build profile should follow this structure:

.. code-block:: yaml

    # Reusable anchors for common configurations
    _base_model: &base_model
      base: id_resource
      admin_roles: [admin]
      view_roles: [public]
      priority: 100

    # Define roles needed by your models
    roles:
      custom-role: 'Description of what this role can do'

    # Define your data models
    models:
      model_name:
        <<: *base_model  # Inherit from base configuration
        # Model-specific properties
        base: name_resource
        display: '<name>'
        fields:
          # Field definitions
          field_name:
            type: field_type
            options:
              # Field options

Example Build Profile
=====================

.. code-block:: yaml

    _base_model: &base_model
      base: id_resource
      admin_roles: [project-team, ai-user]
      view_roles: [project-team]
      priority: 100

    _document_source_options: &document_source_options
      'null': true
      choices: [google_drive]

    roles:
      project-team: 'Project Team (shared access to project resources)'

    models:
      portfolio:
        <<: *base_model
        base: name_resource
        display: '<name>'
        plugin: true
        default_provider: github
        key: name
        fields:
          full_name:
            type: string
            options:
              max_length: 256
          url:
            type: url

      requirement:
        <<: *base_model
        base: portfolio
        display: '<portfolio_id>/requirement-<name>'
        mcp_api: true
        plugin: true
        default_provider: github
        id_fields: [portfolio, name]
        key: name
        fields:
          external_id:
            type: string
            options:
              max_length: 128
          description:
            type: text

          project_url:
            type: url
          default_branch:
            type: string
            options:
              max_length: 256
              default: main

          url:
            type: url
            options:
              'null': true
          document_source:
            type: string
            options:
              <<: *document_source_options
          folders:
            type: list
          topics:
            type: list

Generated Specifications
========================

Running the build profile generates the following specification files:

Data Models (spec/auto/data/)
-----------------------------

Each model generates a data specification file containing:
- Model class definition
- Base model inheritance
- Mixins (provider, group, etc.)
- Roles and permissions
- Field definitions with types and options
- Metadata (ordering, unique constraints, etc.)

Commands (spec/auto/commands/)
------------------------------

Each model generates command specifications for:
- Resource management (list, get, save, remove)
- Model-specific operations
- Priority settings
- Access control

Plugins (spec/auto/plugins/)
----------------------------

Plugin models generate plugin specifications that:
- Register the model as a plugin
- Define provider relationships
- Set default providers

Field Generation Process
========================

For each field in a model:

1. The system identifies the field type
2. Loads the corresponding template from ``app/templates/field/{type}/spec.yml``
3. Applies field options to customize the template
4. Embeds the generated field specification in the model's data file

Common Field Options
--------------------

All fields support these options:
- ``editable`` - Whether users can edit the field (default: true)
- ``system`` - Whether the field is system-managed (default: not editable)
- ``tags`` - List of tags for field categorization (e.g., mcp for MCP API exposure)

Type-specific options:
- String: max_length, choices, default
- Numeric: default, nullable
- Foreign Key: related_data_name, on_delete behavior
- DateTime: default, nullable

Creating New Build Profiles
===========================

To create a new build profile:

1. Define required roles in the ``roles`` section
2. Create model definitions in the ``models`` section
3. For each model, specify:
   - Base model and inheritance
   - Access roles
   - Display format
   - Fields with types and options
   - API configuration (data_api, mcp_api)
4. Run the build process with all the module build profiles with ``zimagi build``

Best Practices
==============

1. Use YAML anchors and aliases to reduce duplication
2. Define reusable option sets as anchors
3. Use descriptive role names and help text
4. Set appropriate access controls for models
5. Define clear display formats for user interfaces
6. Use consistent naming conventions across models
7. Specify all required template variables as defined in the data model template
8. Use appropriate base models for your data structure (id_resource, name_resource, etc.)
9. Set proper admin and view roles for security
10. Define unique constraints using unique_fields or id_fields when needed
11. Group related models together in the same build profile
12. Use meaningful names for anchors that describe their purpose
13. Document complex field configurations with comments
14. Configure API exposure appropriately using field tags
15. Test your build profile by running it and checking generated specifications
