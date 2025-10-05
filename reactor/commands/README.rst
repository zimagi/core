=====================================================
README for Directory: reactor/commands
=====================================================

Directory Overview
------------------

**Purpose**
   This directory contains shell scripts that define and execute Zimagi operations within a reactor environment context. These scripts serve as entry points for various Zimagi commands, facilitating interaction with the Zimagi application and its underlying Docker infrastructure.

**Key Functionality**
   *   Executing Zimagi commands within a Docker container.
   *   Setting up the necessary environment variables and Docker arguments for command execution.
   *   Providing a consistent interface for running Zimagi operations.


Dependencies
-------------------------

The scripts in this directory primarily rely on the `docker` command-line interface for container management and execution. They also depend on standard Unix utilities available in a typical shell environment.


File Structure and Descriptions
-------------------------------

**reactor/commands/zimagi.sh**
     **Role:** This script is the primary entry point for executing Zimagi operations within a Docker container.
     **Detailed Description:** It sets up the Docker environment, including volumes, network settings, and environment variables, to run Zimagi commands. It dynamically collects Zimagi-related environment variables and passes them to the Docker container. The script determines whether to run a Zimagi server image or a client image based on the command being executed, ensuring the correct environment for the operation.


Execution Flow and Interconnection
----------------------------------

**Control Flow Summary**
   1.  The `zimagi.sh` script is invoked with a Zimagi command and its arguments.
   2.  It first calls `zimagi_environment` to set up the reactor environment.
   3.  It then constructs a list of Docker arguments, including volume mounts, network settings, and environment variables.
   4.  It dynamically collects all environment variables starting with "ZIMAGI_" from the current shell and adds them to the Docker arguments.
   5.  Based on the command provided (e.g., "build", "agent"), it selects either the `zimagi_client:dev` image or `zimagi/server:${ZIMAGI_ENVIRONMENT}` image.
   6.  Finally, it executes the `docker run` command with all constructed arguments and the specified Zimagi image and command.

**External Interfaces**
   The `zimagi.sh` script interacts heavily with the Docker daemon to manage and run containers. It uses the `docker run` command to launch Zimagi services, leveraging Docker's networking and volume capabilities. It also interacts with the host system's environment variables to configure the Docker containers.
