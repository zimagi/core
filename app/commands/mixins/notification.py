import logging
import re

from django.conf import settings
from kombu.exceptions import OperationalError
from settings.tasks import send_notification
from systems.commands.index import CommandMixin
from utility.data import ensure_list

logger = logging.getLogger(__name__)


class NotificationMixin(CommandMixin("notification")):
    def normalize_notify_command(self, command):
        return re.sub(r"\s+", ":", command)

    def collect_notify_groups(self, group_names):
        groups = []
        for name in group_names:
            group = self._group.retrieve(name)
            if not group:
                group = self.group_provider.store(name, {})
            groups.append(group)
        return groups

    def load_notification_users(self, success):
        self.notification_users = {}

        def load_groups(groups):
            for group in ensure_list(groups):
                for user in self._user.filter(groups__name=group):
                    if user.email:
                        self.notification_users[user.name] = user.email

        if self.active_user and self.active_user.email:
            self.notification_users[self.active_user.name] = self.active_user.email

        command = re.sub(r"\s+", ":", self.get_full_name())
        notification = self._notification.retrieve(command)

        if notification:
            notification_groups = list(notification.groups.values_list("group__name", flat=True))
            if notification_groups:
                load_groups(notification_groups)

        groups = self.command_notify
        if groups:
            load_groups(groups)

        if not success:
            if notification:
                notification_failure_groups = list(notification.failure_groups.values_list("group__name", flat=True))
                if notification_failure_groups:
                    load_groups(notification_failure_groups)

            groups = self.command_notify_failure
            if groups:
                load_groups(groups)

        return list(self.notification_users.values())

    def format_notification_subject(self, success):
        status = "SUCCESS" if success else "FAILED"
        return f"{settings.EMAIL_SUBJECT_PREFIX} {status}: {self.get_full_name()}"

    def format_notification_body(self):
        option_lines = []
        for key, val in self.options.export().items():
            option_lines.append(f"> {key}: {val}")

        return "Command: {}\n\nOptions:\n\n{}\n\nMessages:\n\n{}\n\nMore Information:\n\n{}".format(
            self.get_full_name(),
            "\n".join(option_lines),
            "\n".join(self.notification_messages),
            f"zimagi log get {self.log_entry.get_id()}",
        )

    def send_notifications(self, success):
        def send_mail(recipient):
            try:
                logger.debug(f"Sending '{subject}' notification in the background")
                send_notification.delay(recipient, subject, body)
            except OperationalError as e:
                logger.debug(f"Sending '{subject}' notification now: {e}")
                send_notification(recipient, subject, body)

        if self.log_result and settings.CELERY_BROKER_URL:
            recipients = self.load_notification_users(success)
            subject = self.format_notification_subject(success)
            body = self.format_notification_body()

            self.run_list(recipients, send_mail)
