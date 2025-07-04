from django.conf import settings
from utility.terminal import TerminalMixin

from zimagi.command import client, schema

from .commands.action import ActionCommand
from .commands.help import HelpCommand
from .commands.router import RouterCommand
from .commands.test import TestCommand
from .commands.version import VersionCommand
from .commands.chat import ChatCommand
from .errors import CommandNotFoundError


class CommandIndex(TerminalMixin):

    def __init__(self):
        self.command_client = client.Client(
            protocol=("http" if settings.COMMAND_HOST == "localhost" else "https"),
            host=settings.COMMAND_HOST,
            port=settings.COMMAND_PORT,
            user=settings.API_USER,
            token=settings.API_USER_TOKEN,
            encryption_key=settings.API_USER_KEY,
            init_commands=False,
            message_callback=self.handle_command_message,
        )

    def get_action(self, command):
        if command.name == "version":
            return VersionCommand(self, command)
        elif command.name == "test":
            return TestCommand(self, command)
        else:
            return ActionCommand(self, command)

    def find(self, args):
        command = self.command_client.schema

        if args[0] == "help":
            return HelpCommand(self, command)
        elif args[0] == "chat":
            return ChatCommand(self, command)

        for name in args:
            if isinstance(command, (schema.Root, schema.Router)):
                try:
                    command = command[name]
                except KeyError:
                    command_name = f"{command.name} {name}" if isinstance(command, schema.Router) else name
                    raise CommandNotFoundError(f"Command '{command_name}' not found")
            else:
                break

        if isinstance(command, schema.Router):
            return RouterCommand(self, command)
        elif isinstance(command, schema.Action):
            self.command = self.get_action(command)
            return self.command
        else:
            raise CommandNotFoundError(f"Command '{command.name} {name}' not found")

    def handle_command_message(self, message):
        self.command.handle_message(message)
