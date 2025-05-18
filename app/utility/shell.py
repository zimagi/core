import logging
import os
import subprocess

from utility.data import flatten

logger = logging.getLogger(__name__)


class ShellError(Exception):
    pass


class Shell:
    @classmethod
    def exec(cls, command_args, input=None, display=True, line_prefix="", env=None, cwd=None, callback=None, sudo=False):
        if not env:
            env = {}

        shell_env = os.environ.copy()
        for variable, value in env.items():
            shell_env[variable] = value

        if sudo:
            command_args = ["sudo", *command_args]

        try:
            process = subprocess.Popen(
                flatten(command_args),
                bufsize=0,
                env=shell_env,
                cwd=cwd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as e:
            logger.debug("Process {} failed with error: {}".format(" ".join(command_args), e))
            return False

        if input:
            if isinstance(input, (list, tuple)):
                input = "\n".join(input) + "\n"
            else:
                input = input + "\n"

            process.stdin.write(input.encode("utf-8"))
        try:
            if callback and callable(callback):
                callback(process, line_prefix, display=display)

            process.wait()
        finally:
            logger.debug("Terminating shell command {} with status {}".format(" ".join(command_args), process.returncode))
            process.terminate()

        return process.returncode == 0

    @classmethod
    def capture(cls, command_args, input=None, line_prefix="", env=None, cwd=None):
        if not env:
            env = {}

        output = []

        def process(process, line_prefix, display):
            for line in process.stdout:
                line = line.decode("utf-8").strip("\n")
                output.append(f"{line_prefix}{line}")

        cls.exec(command_args, input=input, display=False, env=env, cwd=cwd, callback=process)
        return "\n".join(output).strip()
