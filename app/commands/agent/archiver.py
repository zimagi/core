from datetime import datetime
from systems.commands.index import Agent
from utility.data import Collection
from utility.filesystem import save_file


class Archiver(Agent("archiver")):
    processes = ("record_scaling_event",)

    def record_scaling_event(self):
        save_file(f"{settings.DATA_DIR}/scaling-event", datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
        for package in self.listen("worker:scaling", state_key="core_archiver"):
            message = Collection(**package.message)
            self.save_instance(
                self._scaling_event,
                None,
                fields={
                    "created": package.time,
                    "command": message.command,
                    "worker_type": message.worker_type,
                    "worker_max_count": message.worker_max_count,
                    "worker_count": message.worker_count,
                    "task_count": message.task_count,
                    "workers_created": message.workers_created,
                },
            )
