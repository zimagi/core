import logging

from systems.cell.actor import Actor
from systems.cell.communication import CommunicationProcessor
from systems.cell.error import ErrorHandler
from systems.cell.memory import MemoryManager
from systems.cell.state import StateManager
from systems.commands.index import BaseCommand

logger = logging.getLogger(__name__)


class Cell(BaseCommand("cell")):

    @property
    def agent_channel(self):
        channel = super().agent_channel
        if not channel:
            channel = f"agent:{self.get_cell_id()}"
        return channel

    def get_cell_id(self):
        return ":".join(self.get_full_name().split(" ")[1:])

    def get_state_key(self):
        return f"cell:state:{self.get_cell_id()}"

    def get_sensor_key(self):
        return self.agent_user

    def get_error_handler(self):
        return ErrorHandler(self)

    def get_communication_processor(self):
        return CommunicationProcessor(self, self.agent_user, self.get_sensor_key())

    def get_state_manager(self):
        return StateManager(
            self,
            self.get_state_key(),
            {
                "goal": self.agent_goal,
                "rules": self.agent_rules,
                "persona": self.agent_persona,
                "tools": self.agent_tools,
            },
        )

    def get_memory_manager(self, **kwargs):
        return MemoryManager(self, self.agent_user, **kwargs)

    def get_actor(self, **kwargs):
        return Actor(self, **kwargs)

    def exec(self):
        # Initialize cycle
        try:
            self._initialize_cycle(
                self.agent_sensor,
                prompts={
                    "system": self.agent_system_template,
                    "request": self.agent_request_template,
                    "tools": self.agent_tools_template,
                },
            )
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(self.agent_channel, error)
            raise

        # Execute cycle
        try:
            for event in self.communication.listen(self.agent_sensor_filters, self.agent_message_fields):
                response = self.profile(self.process_sensory_event, event)
                self.communication.send(self.agent_channel, event, response, self.agent_channel_field_map)
                self.finalize_event_response(event, response)
                self.data("Completed", response)

        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(self.agent_channel, error)
            raise

        # Finalize cycle
        try:
            self._finalize_cycle()
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(self.agent_channel, error)
            raise

    def _initialize_cycle(self, sensor_name, prompts, **kwargs):
        self.error_handler = self.get_error_handler()
        self.manager.load_templates()

        if self.agent_user:
            self._user.set_active_user(self.get_instance(self._user, self.agent_user, required=True))

        self.actor = self.get_actor(prompts=prompts, **kwargs)
        self.communication = self.get_communication_processor()
        self.communication.set_sensor(sensor_name)

        self.initialize_cycle()

    def initialize_cycle(self):
        """Override in subclasses to extend cell cycle initialization"""
        pass

    def process_sensory_event(self, event):
        return self.actor.respond(
            event, self.agent_memory_sequence, self.agent_memory_search_field, self.agent_message_field_labels
        )

    def finalize_event_response(self, event, response):
        self.actor.memorize()

    def _finalize_cycle(self):
        self.actor.refine_state()
        self.finalize_cycle()

    def finalize_cycle(self):
        """Override in subclasses to extend cell cycle finalization"""
        pass
