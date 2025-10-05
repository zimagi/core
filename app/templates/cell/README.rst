=====================================================
README for Directory: app/templates/cell
=====================================================

Directory Overview
------------------

**Purpose**
   This directory serves as a central repository for template files specifically designed for "cell" components within the Zimagi application. These templates are crucial for defining the structure and content of various prompts and configurations used by the system, particularly in AI-driven interactions and dynamic content generation.

**Key Functionality**
   The primary functionality of this directory revolves around providing structured templates for system prompts, chat interactions, and tool definitions. It enables the dynamic generation of context-rich messages for AI models and facilitates the configuration of how these models interact with available tools and users.

Dependencies
-------------------------

The templates within this directory are primarily consumed by the Zimagi application's core logic, particularly components responsible for AI agent orchestration and prompt engineering. They rely on the application's templating engine (likely Jinja2, given the syntax in the provided files) for rendering and interpolation of dynamic values. There are no direct external library dependencies for the templates themselves, but the rendering process depends on Python's standard library and potentially specific Zimagi internal utilities for data handling and interpolation.

File Structure and Descriptions
-------------------------------

**app/templates/cell/prompt**
     **Role:** This subdirectory contains various prompt templates used to guide AI model behavior and interactions.
     **Detailed Description:** The `prompt` directory houses different types of prompt templates, such as `system.md`, `default.md`, `chat.md`, and `tools.md`. These Markdown files define the initial instructions, general message formatting, chat-specific interaction guidelines, and tool usage instructions for AI agents. They are critical for establishing the persona, goals, rules, and operational procedures of the AI within the Zimagi ecosystem. Each file within this directory serves a distinct purpose in shaping the AI's responses and actions.

**app/templates/cell/README.rst**
     **Role:** This file provides documentation for the `app/templates/cell` directory.
     **Detailed Description:** This `README.rst` file offers a comprehensive overview of the `app/templates/cell` directory, detailing its purpose, key functionalities, dependencies, file structure, and execution flow. It serves as a guide for developers and AI models to understand how the templates within this directory contribute to the Zimagi application's AI-driven interactions and dynamic content generation.

Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The templates in `app/templates/cell` are not directly executable files but rather static resources consumed by the Zimagi application. Typically, an AI agent or a system component requiring a specific prompt will load and render one of these templates. For instance, when an AI agent is initialized, it might load `system.md` to establish its core identity and rules. During a chat interaction, `chat.md` would be used to format incoming messages and guide the AI's response generation, while `tools.md` would be used to instruct the AI on how to utilize available tools. The rendering process involves interpolating dynamic data into the template placeholders, which is handled by the application's templating engine.

**External Interfaces**
   The templates themselves do not directly interface with external systems. Their primary interaction is internal to the Zimagi application, where they are processed by the templating engine and then fed as input to AI models (which might be external services like OpenAI, or internal AI components). The AI models, in turn, might use the instructions from these templates to interact with other external services or databases as defined by the tools described in `tools.md`.
