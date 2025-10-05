=====================================================
README for Directory: app/commands/chat
=====================================================

Directory Overview
------------------

**Purpose**
   This directory encapsulates the command-line interface (CLI) commands related to chat functionality within the Zimagi application. It provides the means for users to send and listen to chat messages through the Zimagi command system.

**Key Functionality**
   * Sending chat messages to a specified channel.
   * Listening for incoming chat messages on a specified channel.
   * Integration with the Zimagi command processing system.


Dependencies
-------------------------

The code in this directory relies on the core Zimagi command system, specifically `systems.commands.index.Command`, for command registration and execution. It also interacts with internal Zimagi services for message broadcasting and user message persistence.


File Structure and Descriptions
-------------------------------

**app/commands/chat/send.py**
     **Role:** Defines the command for sending chat messages.
     **Detailed Description:** This file contains the `Send` class, which inherits from `systems.commands.index.Command`. It implements the `exec` method to handle the logic for sending a chat message. The command constructs a message payload including the user, chat name, message content, and timestamp, and then broadcasts it to a specified chat channel. It also includes functionality to save the user's outgoing message.

**app/commands/chat/listen.py**
     **Role:** Defines the command for listening to incoming chat messages.
     **Detailed Description:** This file contains the `Listen` class, also inheriting from `systems.commands.index.Command`. Its `exec` method continuously listens for messages on a designated chat channel. Upon receiving a message, it processes the message, displays it to the user, and saves incoming messages from other users. It uses a state key to manage the listening process and can be configured with a timeout.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1. A user executes a chat command (e.g., `zimagi chat send` or `zimagi chat listen`) via the Zimagi CLI.
   2. The Zimagi command system dispatches the request to the appropriate command class (`Send` or `Listen`) within this directory.
   3. For `send.py`, the `exec` method is invoked, which constructs a message and uses an internal Zimagi mechanism (`self.send`) to broadcast the message to a chat channel. It also calls `self.save_user_message` to persist the message.
   4. For `listen.py`, the `exec` method enters a loop, using `self.listen` to receive messages from a chat channel. Received messages are then processed and displayed using `self.data` and saved using `self.save_user_message`.

**External Interfaces**
   The commands in this directory primarily interact with the Zimagi core messaging system for broadcasting and receiving chat messages. They also interact with the Zimagi data persistence layer to save user chat history. While not directly interacting with external APIs in these specific files, the underlying Zimagi system handles the communication infrastructure.
