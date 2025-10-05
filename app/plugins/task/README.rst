=====================================================
README for Directory: app/plugins/task
=====================================================

Directory Overview
------------------

**Purpose**
   This directory is dedicated to defining and managing various types of automated tasks that can be executed within the Zimagi platform. It provides a structured way to implement different task functionalities, ranging from executing shell commands locally or remotely to managing file uploads and script executions.

**Key Functionality**
   *   Defining base structure and common utilities for all task plugins.
   *   Executing arbitrary shell commands on the local system.
   *   Executing shell commands on remote systems via SSH.
   *   Running local scripts with dynamic arguments and environment variables.
   *   Running remote scripts on target systems.
   *   Uploading files to remote systems.


Dependencies
-------------------------

The plugins in this directory primarily rely on internal Zimagi modules for core functionalities such as plugin management (`systems.plugins.index`), shell command execution (`utility.shell`), data manipulation (`utility.data`), and text templating (`utility.text`). Specific plugins may also interact with external libraries like `shlex` for command parsing or `os` for file system operations.


File Structure and Descriptions
-------------------------------

**app/plugins/task/script.py**
     **Role:** Implements a task provider for executing local scripts.
     **Detailed Description:** This file defines the `Provider` class for running scripts located on the local file system. It handles the retrieval of the script path, environment variable injection, input/output redirection, and argument interpolation. It leverages the `utility.shell` module for secure script execution and raises `ShellError` on failure.

**app/plugins/task/remote_script.py**
     **Role:** Implements a task provider for executing scripts on remote systems.
     **Detailed Description:** This file defines the `Provider` class that enables the execution of scripts on remote machines via SSH. It manages the temporary upload of the script to the remote host, execution with interpolated arguments and environment variables, and subsequent cleanup of the temporary file. It relies on an internal SSH utility for remote operations.

**app/plugins/task/upload.py**
     **Role:** Implements a task provider for uploading files to remote systems.
     **Detailed Description:** This file defines the `Provider` class responsible for securely uploading files from the local system to a specified remote path. It ensures the source file exists locally and utilizes an internal SSH utility to perform the file transfer, allowing for custom permissions, owner, and group settings on the remote file.

**app/plugins/task/README.rst**
     **Role:** This file serves as the documentation for the `app/plugins/task` directory.
     **Detailed Description:** This reStructuredText file provides an overview of the task plugin directory, detailing its purpose, key functionalities, dependencies, and a description of each file within it. It also outlines the general execution flow and external interfaces for these task plugins.

**app/plugins/task/remote_command.py**
     **Role:** Implements a task provider for executing arbitrary commands on remote systems.
     **Detailed Description:** This file defines the `Provider` class for executing shell commands on remote servers using SSH. It handles the interpolation of command options and environment variables before sending the command for remote execution. It relies on an internal SSH utility for secure remote command execution.

**app/plugins/task/command.py**
     **Role:** Implements a task provider for executing arbitrary commands on the local system.
     **Detailed Description:** This file defines the `Provider` class for executing general shell commands directly on the local system where the Zimagi platform is running. It processes command arguments, environment variables, and input/output streams, utilizing the `utility.shell` module for execution and error handling.

**app/plugins/task/base.py**
     **Role:** Provides the foundational abstract class and common utilities for all task plugins.
     **Detailed Description:** This file defines `BaseProvider`, which all specific task plugins inherit from. It establishes the common interface for task execution, handles configuration parsing, role-based access checks, path resolution for module-specific files, and utility methods for option merging and variable interpolation. It also defines the `TaskResult` class for standardizing task outcomes.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   The execution flow for task plugins typically begins with an external request or an internal system trigger that invokes a specific task.
   1.  A task is initiated, specifying a task plugin (e.g., `command`, `script`, `upload`).
   2.  The `BaseProvider` in `app/plugins/task/base.py` is instantiated for the chosen task type.
   3.  The `exec` method of the `BaseProvider` is called, which first performs access checks based on defined roles.
   4.  If access is granted, the `execute` method (overridden in the specific task plugin, e.g., `app/plugins/task/command.py`, `app/plugins/task/script.py`) is invoked.
   5.  The specific task plugin then performs its designated action, such as calling `self.command.sh` for local shell execution (in `command.py` and `script.py`) or `self._ssh_exec` for remote operations (in `remote_command.py` and `remote_script.py`) or `ssh.upload` (in `upload.py`).
   6.  Results are captured in a `TaskResult` object and returned.

**External Interfaces**
   *   **SSH:** The `remote_command.py`, `remote_script.py`, and `upload.py` plugins interact with remote systems via SSH for command execution, script execution, and file transfers, respectively. This involves establishing SSH connections and executing commands or transferring files over these connections.
   *   **Local Shell:** The `command.py` and `script.py` plugins directly interact with the local operating system's shell to execute commands and scripts.
   *   **Zimagi Command System:** All task plugins interact with the broader Zimagi command system (represented by `self.command`) for logging, error reporting, and accessing global options and utilities.
   *   **File System:** Plugins like `script.py` and `upload.py` interact with the local file system to locate scripts or files for execution or upload.
