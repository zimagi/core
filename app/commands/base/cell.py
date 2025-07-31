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
    def processes(self):
        sensor_name = self.spec["options"].get("agent_sensor", None)
        if not sensor_name:
            return ("assistant",)
        if sensor_name == "chat:message":
            return ("event_processor",)
        else:
            return ("event_processor", "assistant")

    def get_state_key(self):
        return f"cell:state:{self.agent_user}:{".".join(self.get_full_name().split(" ")[1:])}"

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
                "tools": self.agent_tools,
            },
        )

    def get_memory_manager(self, **kwargs):
        return MemoryManager(self, self.agent_user, **kwargs)

    def get_actor(self, **kwargs):
        return Actor(self, **kwargs)

    def event_processor(self):
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

    def assistant(self):
        self.notice("Starting cell assistant ...")

        chat_channel = "chat:message"

        # Initialize cycle
        try:
            self._initialize_cycle(
                chat_channel,
                prompts={
                    "system": self.agent_system_template,
                    "assistant": self.agent_assistant_template,
                },
                search_limit=self.agent_assistant_search_limit,
                search_min_score=self.agent_assistant_search_min_score,
            )
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(chat_channel, error)
            raise

        # Execute cycle
        try:
            for event in self.communication.listen(
                {"mentions_me": "message"},
                ["user", "name", "message", "time"],
            ):
                response = self.profile(self.process_chat_message, event)
                self.communication.send(
                    chat_channel,
                    event,
                    response,
                    {
                        "user": "user",
                        "name": "message__name",
                        "message": "response__message",
                        "time": "time",
                    },
                )
                self.finalize_event_response(event, response)

        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(chat_channel, error)
            raise

        # Finalize cycle
        try:
            self._finalize_cycle()
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(chat_channel, error)
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
            event, self.agent_chat_key, self.agent_memory_search_field, self.agent_message_field_labels
        )

    def process_chat_message(self, event):
        return self.actor.assist(
            event,
            self.agent_chat_key,
            "message",
            {
                "user": "Zimagi Username",
                "name": "Chat Name",
                "time": "Message Time Received",
                "message": "User Message",
            },
        )

    def finalize_event_response(self, event, response):
        self.actor.memorize()

    def _finalize_cycle(self):
        self.actor.refine_state()
        self.finalize_cycle()

    def finalize_cycle(self):
        """Override in subclasses to extend cell cycle finalization"""
        pass
