Quick Start
===========

This guide provides a rapid introduction to using the Zimagi platform.

1.  **Verify Installation**

    After following the :doc:`installation` steps, ensure your Zimagi environment is running correctly:

    .. code-block:: bash

        zimagi info

    This command should output basic information about your Zimagi server and installed modules.

2.  **Explore Available Commands**

    Zimagi offers a wide range of commands. To see a list of top-level commands:

    .. code-block:: bash

        zimagi --help

    To get help on a specific command, for example, `module`:

    .. code-block:: bash

        zimagi module --help

3.  **Manage Modules**

    Modules are fundamental building blocks in Zimagi. You can create a new module from a template:

    .. code-block:: bash

        zimagi module create my-new-module --template standard

    This creates a new module named `my-new-module` using the `standard` template.

4.  **Interact with AI Agents**

    Zimagi integrates AI capabilities. You can ask the platform questions:

    .. code-block:: bash

        zimagi ai ask "What is the capital of France?"

    You can also engage in a chat session:

    .. code-block:: bash

        zimagi chat listen my-chat-channel

    In another terminal, send a message:

    .. code-block:: bash

        zimagi chat send my-chat-channel "Hello, Zimagi!"

5.  **Data Management**

    Manage configuration settings:

    .. code-block:: bash

        zimagi config save my-setting --value "my_value" --type string

    Retrieve your setting:

    .. code-block:: bash

        zimagi config get my-setting

6.  **Task Scheduling**

    Schedule a simple task to run periodically:

    .. code-block:: bash

        zimagi schedule save my-daily-task --command "platform info" --interval "days=1"

    This schedules the `platform info` command to run every day.

For more detailed usage, refer to the :doc:`usage/index` section.
