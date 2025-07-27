# Zimagi Chat Commands Directory

## Overview

The `app/commands/chat` directory contains specialized command implementations that provide chat functionality within the Zimagi platform. These commands enable real-time communication between users and AI agents through message sending and listening capabilities.

This directory plays a critical architectural role by implementing the chat command layer that powers the platform's conversational interfaces. The commands defined here are automatically exposed through RESTful API endpoints and CLI interfaces, enabling consistent access to chat functionality regardless of the interaction method.

The directory is used by:

- **Developers** working on chat functionality and messaging systems
- **System administrators** managing Zimagi deployments and communications
- **AI models** analyzing and generating conversational components
- **End users** engaging in chat interactions through CLI or API

## Directory Contents

### Files

| File      | Purpose                                                                      | Format |
| --------- | ---------------------------------------------------------------------------- | ------ |
| listen.py | Implements the chat listen command for monitoring chat messages in real-time | Python |
| send.py   | Implements the chat send command for sending messages to chat channels       | Python |

There are no subdirectories in this directory.

## Cross-Referencing

This directory integrates with several other parts of the Zimagi project:

- **Parent Context**: Part of the `app/commands` directory which contains executable commands and agents available through CLI or APIs
- **Specifications**: Command interfaces are defined in `app/spec/commands/chat.yml` which drives the command system through YAML specifications
- **Command Systems**: Connects to `app/systems/commands` for command execution framework and dynamic class generation
- **API Systems**: Works with `app/systems/api/command` for REST API exposure of commands
- **Chat Data Models**: Integrates with `app/data/chat` for chat message persistence and retrieval
- **Plugin Systems**: Connects to `app/plugins` for extensible chat functionality
- **Settings**: Uses configurations defined in `app/settings` for chat behavior parameters

## Key Concepts and Patterns

### Command Architecture

The chat command system implements a specification-driven approach to command generation:

- YAML specifications in `app/spec/commands/chat.yml` define command structures and parameters
- The `app/systems/commands/index.py` module dynamically generates command classes at runtime
- Commands are created with appropriate parsing rules and execution logic
- Base command classes provide consistent interfaces for command extension operations

### Chat Operations

The chat system implements two primary operations:

- **Send Command** (`send.py`): Sends messages to chat channels

  - Base: chat
  - Priority: 800
  - Parse configurations: Uses the chat mixin's parsing capabilities
  - Implements message sending with user context and timestamp tracking
  - Takes parameters: chat_name and chat_text

- **Listen Command** (`listen.py`): Monitors chat channels for incoming messages
  - Base: chat
  - Priority: 800
  - Parse configurations: Uses the chat mixin's parsing capabilities
  - Implements real-time message listening with state tracking and timeout handling
  - Takes parameters: listen_timeout and listen_state_key

### Agent Directives

The chat system also implements AI agent functionality through specifications in `app/spec/commands/chat.yml`:

- **Agent Goal**: Engage naturally, execute tools intelligently, adapt to context, bridge modalities, and guide users
- **Agent Rules**: Be honest, use tools responsibly, preserve user intent, stay within scope, respond efficiently, and maintain state awareness
- **Agent Sensors**: Uses chat:message sensor with mentions_me filter
- **Agent Memory**: Uses message field for search with user, name, time, and message fields
- **Agent Templates**: Uses chat template with configurable agent tools

### Naming Conventions

- Command files are named by their functional operation (e.g., `send.py`, `listen.py`)
- Command classes extend the base command with the command name as a parameter using `Command("chat.operation")`
- Method names follow Python conventions with descriptive names
- Agent classes follow the pattern defined in the specification with dsr1 and dsv3 implementations

### File Organization

Files are organized by chat operation:

- Each chat operation has its own file
- Related chat functionality is grouped in this directory
- Agent implementations are defined in the specification file

### Domain-Specific Patterns

- All chat commands integrate with the command facade pattern through inheritance
- Error handling follows consistent patterns with custom exception classes
- Integration with communication channels for message passing
- Support for both synchronous and asynchronous execution patterns
- Agent implementations follow specific directive patterns for AI behavior

## Developer Notes and Usage Tips

### Integration Requirements

These commands require:

- Django framework access for settings and configuration management
- Proper command specification files in `app/spec/commands/chat.yml` for command generation
- Access to chat data models in `app/data/chat` for message persistence
- Utility functions from `app/utility` for common operations

### Usage Patterns

- Chat commands are accessed through the indexing system in `app/systems/commands/index.py` using the `Command()` function
- Implement commands by extending base command classes
- Follow established patterns for message processing and error handling
- Access command functionality through the standard Zimagi command execution system
- Agent commands are accessed through `Agent()` function in the indexing system

### Dependencies

- Django framework for settings and configuration
- Standard Python libraries for data processing
- Utility functions from `app/utility` for common operations
- Command specifications from `app/spec/commands/chat.yml` for generation
- Chat data models from `app/data/chat` for message persistence
- Communication channel system from `app/systems/communication` for message passing

### AI Development Guidance

When generating or modifying chat commands:

1. Maintain consistency with the specification-driven generation patterns
2. Ensure proper error handling with command-specific exception classes
3. Follow established patterns for message processing and communication channel integration
4. Respect the separation of concerns between different chat operations
5. Consider performance implications for real-time message processing
6. Maintain consistency with existing naming and API patterns
7. Document all public methods with clear docstrings
8. Follow the established patterns for dynamic class generation and indexing
9. Reference existing chat commands as examples for new implementations
10. Ensure command specifications in `app/spec/commands/chat.yml` properly define the interface with appropriate base commands and mixins
11. Follow agent directive patterns for AI behavior implementation
12. Maintain consistency with agent sensor and memory patterns for contextual awareness
