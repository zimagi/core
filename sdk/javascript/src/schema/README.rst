=====================================================
README for Directory: sdk/javascript/src/schema
=====================================================

Directory Overview
------------------

**Purpose**
   This directory defines the data structures and schema classes used throughout the Zimagi JavaScript SDK. It provides a structured way to represent API responses, commands, actions, and other data entities, ensuring consistency and type safety across the client-side application.

**Key Functionality**
   *   Defines core schema classes for API responses, including Root, Router, Action, Field, Error, Object, and Array.
   *   Implements sorting mechanisms for command and data items within schema objects.
   *   Provides utility functions for managing and accessing nested command structures.
   *   Facilitates the parsing and interpretation of API metadata into structured JavaScript objects.


Dependencies
-------------------------

This directory primarily relies on standard JavaScript features and does not have external third-party library dependencies beyond the core JavaScript runtime environment. It is designed to be a foundational layer for the Zimagi JavaScript SDK.


File Structure and Descriptions
-------------------------------

**sdk/javascript/src/schema/index.ts**
     **Role:** This file serves as the main entry point and central definition for all schema classes and related utilities within the Zimagi JavaScript SDK.
     **Detailed Description:** It exports classes such as `Root`, `Router`, `Action`, `Field`, `Error`, `SchemaObject` (aliased as `Object`), and `SchemaArray` (aliased as `Array`). It includes mixins like `SortedItemsMixin` for ordered data handling and `CommandIndexMixin` for categorizing commands, routers, and actions. This file is crucial for constructing and navigating the API's command structure and data responses in a type-safe and organized manner. It defines how API metadata is represented and interacted with in the client-side application.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The `index.ts` file acts as the primary definition module. When the Zimagi JavaScript SDK is initialized or interacts with the Zimagi API, the schema definitions within `index.ts` are used to parse and structure the incoming JSON responses. For example, an API response representing the root of the Zimagi command structure would be instantiated as a `Root` object, which then contains `Router` and `Action` objects, all defined within this file. The `_keySorter` function and the `SortedItemsMixin` and `CommandIndexMixin` classes provide the underlying logic for organizing and accessing these schema objects.

**External Interfaces**
   The schema definitions in this directory are designed to mirror the structure of the Zimagi API's metadata and data responses. They serve as the client-side representation of the API. While this directory itself does not directly make external calls, the classes defined here are consumed by other parts of the Zimagi JavaScript SDK (e.g., the command execution layer) to interact with the Zimagi backend API.
