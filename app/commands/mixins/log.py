import datetime
import threading

from django.conf import settings
from django.utils import timezone
from systems.commands.index import CommandMixin


class LogMixin(CommandMixin("log")):
    log_lock = threading.Lock()

    def log_init(self, options=None, task=None, log_key=None, worker=None):
        if options is None:
            options = {}

        if self.log_result:
            with self.log_lock:
                if log_key is None or log_key == "<none>":
                    self.log_entry = self._log.create(None, {"command": self.get_full_name()})
                else:
                    self.log_entry = self._log.retrieve(log_key)

                self.log_entry.user = self.active_user
                self.log_entry.config = options
                self.log_entry.status = self._log.model.STATUS_RUNNING
                if task:
                    self.log_entry.worker = worker
                    self.log_entry.task_id = task.request.id

                self.log_entry.save()

        return self.log_entry.name if self.log_result else "<none>"

    def log_message(self, data, log=True):
        def _create_log_message(command, data, _log):
            if getattr(command, "log_entry", None) and _log:
                command.log_entry.messages.create(data=data)

            if command.exec_parent:
                _create_log_message(command.exec_parent, data, True)

        if self.log_result:
            with self.log_lock:
                _create_log_message(self, data, log)

    def log_status(self, status, check_log_result=False, schedule=None):
        if not check_log_result or self.log_result:
            with self.log_lock:
                if getattr(self, "log_entry", None):
                    if schedule:
                        self.log_entry.schedule_id = schedule

                    self.log_entry.set_status(status)
                    self.log_entry.save()

    def get_status(self):
        return self.log_entry.status if self.log_result else None

    def clean_logs(self, log_days=None, message_days=None):
        current_time = timezone.now()

        if log_days is None:
            log_days = settings.LOG_RETENTION_DAYS
        if message_days is None:
            message_days = settings.LOG_MESSAGE_RETENTION_DAYS

        log_cutoff_time = current_time - datetime.timedelta(days=log_days)
        log_message_cutoff_time = current_time - datetime.timedelta(days=message_days)

        self._log_message.filter(log__updated__lte=log_message_cutoff_time).delete()
        self._log.filter(updated__lte=log_cutoff_time).delete()
