import copy
import logging
import sys

from datetime import datetime
from celery import beat, current_app, exceptions, schedules
from django.conf import settings
from django.db.models import Case, F, IntegerField, Q, When
from django.db.models.functions import Cast
from django_celery_beat.clockedschedule import clocked
from django_celery_beat.schedulers import DatabaseScheduler, ModelEntry
from django_celery_beat.utils import aware_now

from data.schedule.models import ScheduledTask, ScheduledTaskChanges, TaskCrontab, TaskDatetime, TaskInterval
from utility.filesystem import save_file

logger = logging.getLogger(__name__)


class ScheduleEntry(ModelEntry):
    model_schedules = (
        (schedules.schedule, TaskInterval, "interval"),
        (schedules.crontab, TaskCrontab, "crontab"),
        (clocked, TaskDatetime, "clocked"),
    )

    @classmethod
    def from_entry(cls, name, app=None, **entry):
        obj, created = ScheduledTask._default_manager.update_or_create(
            name=name,
            defaults=cls._unpack_fields(**entry),
        )
        return cls(obj, app=app)

    @classmethod
    def _unpack_fields(cls, schedule, args=None, kwargs=None, relative=None, options=None, **entry):
        entry_schedules = {model_field: None for _, _, model_field in cls.model_schedules}
        model_schedule, model_field = cls.to_model_schedule(schedule)
        entry_schedules[model_field] = model_schedule
        entry.update(entry_schedules, args=args or [], kwargs=kwargs or {}, **cls._unpack_options(**options or {}))
        return entry

    @classmethod
    def _unpack_options(
        cls, queue=None, exchange=None, routing_key=None, priority=None, headers=None, expire_seconds=None, **kwargs
    ):
        return {
            "queue": queue,
            "exchange": exchange,
            "routing_key": routing_key,
            "priority": priority,
            "headers": headers or {},
            "expire_seconds": expire_seconds,
        }

    def __init__(self, model, app=None):
        self.app = app or current_app._get_current_object()
        self.name = model.name
        self.task = model.task
        try:
            self.schedule = model.schedule
        except model.DoesNotExist:
            logger.error(
                "Disabling schedule %s that was removed from database",
                self.name,
            )
            self._disable(model)

        self.args = model.args
        self.kwargs = model.kwargs

        self.options = {}
        for option in ["queue", "exchange", "routing_key", "priority"]:
            value = getattr(model, option)
            if value is not None:
                self.options[option] = value

        if getattr(model, "expires_", None):
            self.options["expires"] = getattr(model, "expires_")

        self.options["headers"] = model.headers or {}
        self.options["periodic_task_name"] = model.name

        self.total_run_count = model.total_run_count
        self.model = model

        if not model.last_run_at:
            model.last_run_at = self._default_now()

        self.last_run_at = model.last_run_at


class CeleryScheduler(DatabaseScheduler):
    Entry = ScheduleEntry
    Model = ScheduledTask
    Changes = ScheduledTaskChanges

    def install_default_entries(self, data):
        self.update_from_dict({})
        save_file(f"{settings.DATA_DIR}/scheduler", datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    def apply_async(self, entry, producer=None, advance=True, **kwargs):
        entry = self.reserve(entry) if advance else entry
        task = self.app.tasks.get(entry.task)

        options = copy.deepcopy(entry.options)
        options["queue"] = entry.kwargs.get("worker_type", "default")
        options["priority"] = entry.kwargs.get("task_priority", settings.WORKER_DEFAULT_TASK_PRIORITY)
        try:
            entry_args = beat._evaluate_entry_args(entry.args)
            entry_kwargs = beat._evaluate_entry_kwargs(entry.kwargs)
            if task:
                return task.apply_async(entry_args, entry_kwargs, producer=producer, **options)
            else:
                return self.send_task(entry.task, entry_args, entry_kwargs, producer=producer, **options)
        except Exception as exc:
            exceptions.reraise(
                beat.SchedulingError,
                beat.SchedulingError(f"Couldn't apply scheduled task {entry.name}: {exc}"),
                sys.exc_info()[2],
            )
        finally:
            self._tasks_since_sync += 1
            if self.should_sync():
                self._do_sync()

    def _get_crontab_exclude_query(self):
        server_time = aware_now()
        server_hour = server_time.hour

        hours_to_include = [(server_hour + offset) % 24 for offset in range(-2, 3)]
        hours_to_include += [4]  # celery's default cleanup task

        numeric_hour_pattern = r"^\d+$"
        numeric_hour_tasks = TaskCrontab.objects.filter(hour__regex=numeric_hour_pattern)

        annotated_tasks = numeric_hour_tasks.annotate(
            hour_int=Cast("hour", IntegerField()),
            server_hour=Case(
                *[
                    When(timezone=timezone_name, then=(F("hour_int") + self._get_timezone_offset(timezone_name) + 24) % 24)
                    for timezone_name in self._get_unique_timezone_names()
                ],
                default=F("hour_int"),
            ),
        )

        excluded_hour_task_ids = annotated_tasks.exclude(server_hour__in=hours_to_include).values_list("id", flat=True)
        exclude_query = Q(crontab__isnull=False) & Q(crontab__id__in=excluded_hour_task_ids)
        return exclude_query

    def _get_unique_timezone_names(self):
        return TaskCrontab.objects.values_list("timezone", flat=True).distinct()
