=====================================================
README for Directory: sdk/javascript/src/messages
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is dedicated to defining and managing the message system for the Zimagi JavaScript SDK. It provides a structured way to handle various types of messages, including status updates, data payloads, informational messages, warnings, and errors, ensuring consistent communication within the SDK and with external systems.

**Key Functionality**
   *   Standardized message creation and handling.
   *   Serialization and deserialization of messages to and from JSON.
   *   Categorization of messages into different types (e.g., `StatusMessage`, `ErrorMessage`).
   *   Formatting and display mechanisms for different message types.
   *   Support for message decryption when a cipher is provided.


Dependencies
-------------------------

The code in this directory primarily relies on internal utilities within the Zimagi JavaScript SDK, specifically `normalizeValue` from `../utility`. It also implicitly depends on the standard JavaScript `console` object for displaying messages and `JSON` for serialization/deserialization.


File Structure and Descriptions
-------------------------------

**sdk/javascript/src/messages/README.rst**
     **Role:** This file serves as the documentation for the `sdk/javascript/src/messages` directory.
     **Detailed Description:** It provides an overview of the directory's purpose, key functionalities, dependencies, and detailed descriptions of the files contained within it. This README is crucial for understanding the architecture and usage of the message system in the Zimagi JavaScript SDK.

**sdk/javascript/src/messages/index.ts**
     **Role:** This file defines the core message classes and the message handling logic for the Zimagi JavaScript SDK.
     **Detailed Description:** It contains the base `Message` class, which all other message types extend, providing common properties and methods like `render`, `toJSON`, `format`, and `display`. It also defines specialized message classes such as `StatusMessage`, `DataMessage`, `InfoMessage`, `NoticeMessage`, `SuccessMessage`, `WarningMessage`, `ErrorMessage`, `TableMessage`, and `ImageMessage`, each with specific behaviors and properties. This file is the central hub for all message-related operations within the SDK, including the static `get` method for instantiating message objects from raw data.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The `index.ts` file acts as the primary entry point for message-related operations. When a message needs to be created, an instance of `Message` or one of its derived classes is instantiated. The `load` method is used to populate message data, and `render` is used to prepare the message for serialization. For displaying messages, the `display` method is invoked, which internally calls `format` to structure the message content. When receiving messages from an external source, the static `Message.get` method is used to parse the incoming data and return the appropriate message instance.

**External Interfaces**
   The message system primarily interacts with the broader Zimagi JavaScript SDK. It uses the `normalizeValue` utility for data processing. Messages, particularly `ErrorMessage` and `WarningMessage`, interact with the browser's `console.error` and `console.warn` respectively for output. The `toJSON` method facilitates communication with external APIs or other parts of the application that expect JSON-formatted messages. The `Message.get` method can optionally interact with a `cipher` object for decrypting incoming message packages, implying an interface with a cryptographic utility.
