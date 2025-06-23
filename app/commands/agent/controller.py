from datetime import datetime
from django.conf import settings
from services.celery import app
from systems.commands.index import Agent
from utility.filesystem import save_file


class Controller(Agent("controller")):
    def exec(self):
        self.manager.reset()

        for agent in self.manager.collect_agents():
            worker = self.get_provider(
                "worker",
                settings.WORKER_PROVIDER,
                app,
                worker_type=agent.spec.get("worker_type", "default"),
                command_name=" ".join(agent.command),
                command_options=agent.spec.get("options", {}),
            )
            if self._check_agent_schedule(agent.spec):
                config_name = self.manager._get_agent_scale_config(agent.command)
                agent_count = self.get_config(config_name, 0)
                worker.scale_agents(agent_count)
            else:
                worker.scale_agents(0)

        save_file(f"{settings.DATA_DIR}/controller", datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
