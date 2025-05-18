from systems.commands.index import Agent


class Archiver(Agent("archiver")):
    processes = ("record_scaling_event",)

    def record_scaling_event(self):
        for package in self.listen("worker:scaling", state_key="core_archiver"):
            message = package.message
            self.save_instance(
                self._scaling_event,
                None,
                fields={
                    "created": package.time,
                    "log_id": message.log_key,
                    "worker_max_count": message.worker_max_count,
                    "worker_count": message.worker_count,
                    "task_count": message.task_count,
                    "workers_created": message.workers_created,
                },
            )
