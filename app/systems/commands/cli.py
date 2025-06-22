import cProfile
import functools
import os
import sys
import time

import django
from django.conf import settings
from django.core import management
from django.core.management import call_command
from django.core.management.base import CommandError, CommandParser
from django.core.management.commands import migrate
from django.db import connection
from systems.models.overrides import *  # noqa: F401, F403
from utility.display import format_exception_info
from utility.mutex import MutexError, check_mutex
from utility.terminal import TerminalMixin

django_allowed_commands = ["check", "shell", "dbshell", "inspectdb", "showmigrations", "makemigrations", "migrate"]


class CLI(TerminalMixin):
    def __init__(self, argv=None):
        super().__init__()
        self.argv = argv if argv else []

    def handle_error(self, error):
        if not isinstance(error, CommandError) and error.args:
            self.print("** " + self.error_color(error.args[0]), sys.stderr)
        else:
            self.print("** " + self.error_color(error), sys.stderr)

        try:
            debug = settings.MANAGER.runtime.debug()
        except AttributeError:
            debug = True

        if debug:
            self.print(
                "> " + self.traceback_color("\n".join([item.strip() for item in format_exception_info()])),
                stream=sys.stderr,
            )

    def exclusive_wrapper(self, exec_method, lock_id):
        def wrapper(*args, **kwargs):
            tries = 0
            while True:
                try:
                    with check_mutex(lock_id):
                        if tries == 0:
                            return exec_method(*args, **kwargs)
                        return

                except MutexError as error:
                    pass

                time.sleep(0.1)
                tries += 1

        functools.update_wrapper(wrapper, exec_method)
        return wrapper

    def initialize(self):
        parser = CommandParser(add_help=False, allow_abbrev=False)
        parser.add_argument("args", nargs="*")
        namespace, extra = parser.parse_known_args(self.argv[1:])
        args = namespace.args

        if not args:
            args = ["help"]

        if "--debug" in extra:
            settings.MANAGER.runtime.debug(True)

        if "--no-color" in extra:
            settings.MANAGER.runtime.color(False)

        return args

    def execute(self):
        try:
            os.environ["ZIMAGI_ARGS"] = " ".join(self.argv[1:])

            django.setup()

            if settings.INIT_PROFILE or settings.COMMAND_PROFILE:
                settings.MANAGER.runtime.parallel(False)

            if settings.COMMAND_PROFILE:
                command_profiler = cProfile.Profile()

            if settings.INIT_PROFILE:
                init_profiler = cProfile.Profile()
                init_profiler.enable()

            try:
                args = self.initialize()

                if args[0] in django_allowed_commands:
                    command = management.load_command_class("django.core", args[0])
                else:
                    command = settings.MANAGER.index.find_command(args)

                if settings.INIT_PROFILE:
                    init_profiler.disable()

                if settings.COMMAND_PROFILE:
                    command_profiler.enable()

                if isinstance(command, migrate.Command):
                    command.run_from_argv = self.exclusive_wrapper(command.run_from_argv, "system_migrate")

                command.run_from_argv(self.argv)
                self.exit(0)

            except KeyboardInterrupt:
                self.print("> " + self.error_color("User aborted"), stream=sys.stderr)
            except Exception as error:
                self.handle_error(error)

            self.exit(1)

        except Exception as error:
            self.handle_error(error)
        finally:
            connection.close()

            if settings.INIT_PROFILE:
                init_profiler.dump_stats(self.get_profiler_path("init"))

            if settings.COMMAND_PROFILE:
                command_profiler.disable()
                command_profiler.dump_stats(self.get_profiler_path("command"))

    def install(self):
        try:
            django.setup()

            from systems.commands import action

            command = action.primary("install", interpolate=False)

            settings.MANAGER.install_scripts(command, True)
            settings.MANAGER.install_requirements(command, True)
            self.exit(0)

        except KeyboardInterrupt:
            self.print("> " + self.error_color("User aborted"), stream=sys.stderr)
        except Exception as error:
            self.handle_error(error)

        self.exit(1)

    def get_profiler_path(self, name):
        return os.path.join(settings.MANAGER.profiler_path, f"{name}.profile")


def execute(argv):
    CLI(argv).execute()


def install():
    CLI().install()
