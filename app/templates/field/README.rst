=====================================================
README for Directory: app/templates/field
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as a central repository for defining various data field templates used throughout the Zimagi application. These templates standardize the creation and configuration of different field types for data models, ensuring consistency and reusability across the system.

**Key Functionality**
   *   Standardized definition of data model field types.
   *   Configuration of field properties such as nullability, default values, and editability.
   *   Facilitates automated generation of data model specifications.
   *   Ensures consistent data handling and validation across the application.


Dependencies
-------------------------

The files in this directory primarily rely on the core Zimagi application's templating and data specification generation mechanisms. They define structures that are consumed by other parts of the system responsible for building data models and their associated database schemas. Specifically, they interact with the `app/systems/manage/service.py` for service management and potentially other internal Zimagi components for data model compilation.


File Structure and Descriptions
-------------------------------

**app/templates/field/README.rst**
     **Role:** This file provides an overview and documentation for the `app/templates/field` directory.
     **Detailed Description:** This README explains the purpose, key functionalities, dependencies, and file structure of the `app/templates/field` directory. It serves as a guide for developers and AI models to understand how different field templates are organized and utilized within the Zimagi project.

**app/templates/field/binary**
     **Role:** This directory contains templates for defining binary data fields.
     **Detailed Description:** The `binary` directory holds the `index.yml` and `spec.yml` files that specify how binary fields are configured. `index.yml` defines the variables and mapping for binary fields, including `data_name`, `field_name`, `nullable`, `max_length`, and `editable`. `spec.yml` translates these variables into a `@django.BinaryField` type with corresponding options for nullability, maximum length, and editability, which are used during data model generation.

**app/templates/field/text**
     **Role:** This directory contains templates for defining text data fields.
     **Detailed Description:** The `text` directory includes `index.yml` and `spec.yml` for text fields. `index.yml` outlines variables such as `data_name`, `field_name`, `nullable`, `default`, and `editable`. `spec.yml` maps these to a `@django.TextField` type, configuring options like nullability, default values, and editability for text-based data fields in the application's data models.

**app/templates/field/dict**
     **Role:** This directory contains templates for defining dictionary data fields.
     **Detailed Description:** The `dict` directory provides `index.yml` and `spec.yml` for dictionary fields. `index.yml` defines variables like `data_name`, `field_name`, and `editable`. `spec.yml` specifies the field as a `@zimagi.DictionaryField` with options for editability and system status, allowing for structured key-value pair data within models.

**app/templates/field/list**
     **Role:** This directory contains templates for defining list data fields.
     **Detailed Description:** The `list` directory contains `index.yml` and `spec.yml` for list fields. `index.yml` defines variables such as `data_name`, `field_name`, and `editable`. `spec.yml` configures the field as a `@zimagi.ListField` with options for editability and system status, enabling the storage of ordered collections of data within models.

**app/templates/field/boolean**
     **Role:** This directory contains templates for defining boolean data fields.
     **Detailed Description:** The `boolean` directory includes `index.yml` and `spec.yml` for boolean fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, and `editable`. `spec.yml` maps these to a `@django.BooleanField` type, setting options for nullability, default values, and editability for true/false data fields.

**app/templates/field/duration**
     **Role:** This directory contains templates for defining duration data fields.
     **Detailed Description:** The `duration` directory provides `index.yml` and `spec.yml` for duration fields. `index.yml` defines variables such as `data_name`, `field_name`, `nullable`, `default`, and `editable`. `spec.yml` configures the field as a `@django.DurationField` with options for nullability, default values, and editability, used for storing periods of time.

**app/templates/field/string**
     **Role:** This directory contains templates for defining string (character) data fields.
     **Detailed Description:** The `string` directory includes `index.yml` and `spec.yml` for string fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, `choices`, `max_length`, `editable`, and `primary_key`. `spec.yml` maps these to a `@django.CharField` type, configuring options for nullability, default values, choices, maximum length, editability, and primary key status.

**app/templates/field/foreign_key**
     **Role:** This directory contains templates for defining foreign key relationship fields.
     **Detailed Description:** The `foreign_key` directory provides `index.yml` and `spec.yml` for foreign key fields. `index.yml` defines variables such as `data_name`, `field_name`, `related_data_name`, `reverse_related_name`, `nullable`, `on_delete`, and `editable`. `spec.yml` configures the field as a `@django.ForeignKey` type, specifying the related data model, nullability, deletion behavior (`on_delete`), and editability, establishing relationships between data models.

**app/templates/field/date**
     **Role:** This directory contains templates for defining date data fields.
     **Detailed Description:** The `date` directory includes `index.yml` and `spec.yml` for date fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, `editable`, and `primary_key`. `spec.yml` maps these to a `@django.DateField` type, configuring options for nullability, default values, editability, and primary key status for date-only data.

**app/templates/field/many_to_many**
     **Role:** This directory contains templates for defining many-to-many relationship fields.
     **Detailed Description:** The `many_to_many` directory provides `index.yml` and `spec.yml` for many-to-many fields. `index.yml` defines variables such as `data_name`, `field_name`, `related_data_name`, and `reverse_related_name`. `spec.yml` configures the field as a `@django.ManyToManyField` type, specifying the related data model and an optional reverse related name, enabling complex relationships between data models.

**app/templates/field/float**
     **Role:** This directory contains templates for defining floating-point number fields.
     **Detailed Description:** The `float` directory includes `index.yml` and `spec.yml` for float fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, `editable`, and `primary_key`. `spec.yml` maps these to a `@django.FloatField` type, configuring options for nullability, default values, editability, and primary key status for decimal number data.

**app/templates/field/url**
     **Role:** This directory contains templates for defining URL fields.
     **Detailed Description:** The `url` directory provides `index.yml` and `spec.yml` for URL fields. `index.yml` defines variables such as `data_name`, `field_name`, `nullable`, `default`, `max_length`, and `editable`. `spec.yml` configures the field as a `@django.URLField` type, setting options for nullability, default values, maximum length, and editability for storing web addresses.

**app/templates/field/big_integer**
     **Role:** This directory contains templates for defining big integer fields.
     **Detailed Description:** The `big_integer` directory includes `index.yml` and `spec.yml` for big integer fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, `editable`, and `primary_key`. `spec.yml` maps these to a `@django.BigIntegerField` type, configuring options for nullability, default values, editability, and primary key status for large integer data.

**app/templates/field/integer**
     **Role:** This directory contains templates for defining integer fields.
     **Detailed Description:** The `integer` directory includes `index.yml` and `spec.yml` for integer fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, `editable`, and `primary_key`. `spec.yml` maps these to a `@django.IntegerField` type, configuring options for nullability, default values, editability, and primary key status for standard integer data.

**app/templates/field/datetime**
     **Role:** This directory contains templates for defining datetime fields.
     **Detailed Description:** The `datetime` directory includes `index.yml` and `spec.yml` for datetime fields. `index.yml` defines variables like `data_name`, `field_name`, `nullable`, `default`, `editable`, and `primary_key`. `spec.yml` maps these to a `@django.DateTimeField` type, configuring options for nullability, default values, editability, and primary key status for date and time data.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The files within `app/templates/field` are not directly executable entry points. Instead, they are configuration templates that define the structure and properties of various data fields. When a new data model or a field within an existing model is to be created or modified, the Zimagi system (likely through a management command or an internal API) references these templates. For example, if a user or an automated process requests a "string" field, the system would look up `app/templates/field/string/index.yml` to understand the required variables (e.g., `data_name`, `field_name`, `max_length`) and then use `app/templates/field/string/spec.yml` to generate the actual Django field specification. The `index.yml` files act as a blueprint for the variables needed to define a field, while the `spec.yml` files translate these variables into the specific Django field type and its options.

**External Interfaces**
   The primary interaction of these template files is with the Zimagi core system's data model generation and management components. They serve as input for processes that dynamically construct Django models and their corresponding database schemas. While these files themselves do not directly interact with external databases or APIs, the data models they define will ultimately interface with the PostgreSQL database (as configured in `compose.db.yaml`) and potentially other services like Redis or Qdrant, depending on the data model's requirements. The `app/systems/manage/service.py` module, which handles service management and specification loading, is a key internal consumer of the definitions provided by these field templates.
