import logging
import yaml
import time

from django.core.management.base import CommandError
from systems.manage.task import CommandAborted
from systems.commands import exec
from utility import display

logger = logging.getLogger(__name__)


class WebhookCommand(exec.ExecCommand):

    def set_options(self, options, primary=False):
        self.options.clear()
        for key, value in options.items():
            self.options.add(key, value)

    def get_response_type(self):
        return "text/plain"

    def handle_api(self, options):
        self._register_signal_handlers()

        logger.debug(f"Running API webhook: {self.get_full_name()}\n\n{yaml.dump(options)}")

        try:
            return self._webhook_exec_wrapper()
        except Exception as e:
            logger.warning(f"Command transport exception: {e}")
            raise e
        finally:
            self.export_profiler_data()

    def _webhook_exec_wrapper(self):
        self.start_time = time.time()

        success = True
        log_key = self._exec_init(signals=False)

        try:
            return self._exec_api_handler(log_key)

        except Exception as e:
            success = False

            if not isinstance(e, (CommandError, CommandAborted)):
                self.error(e, terminate=False, traceback=display.format_exception_info(), system=True)
        finally:
            try:
                self.log_status(success, True)
                self.send_notifications(success)

            except Exception as e:
                self.error(e, terminate=False, traceback=display.format_exception_info(), system=True)

            finally:
                self.shutdown()
                self.set_status(success)
                self.publish_exit()
                self.manager.delete_task_status(log_key)
                self.manager.cleanup(log_key)
                self.flush()

    def _exec_local_handler(self, log_key, primary=True):
        raise NotImplementedError("Method _exec_local_handler not supported for webhook commands")

    def _exec_api_handler(self, log_key):
        profiler_name = "exec.webhook.api"
        try:
            self.start_profiler(profiler_name)
            return self.exec()
        finally:
            self.stop_profiler(profiler_name)
