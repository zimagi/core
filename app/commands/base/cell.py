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

    def get_state_manager(self, actor):
        return StateManager(
            self,
            actor,
            self.get_state_key(),
            {
                "goal": self.agent_goal,
                "rules": self.agent_rules,
                "tools": self.agent_tools,
            },
        )

    def get_memory_manager(self, actor):
        return MemoryManager(
            self,
            actor,
            self.agent_user,
            self.agent_chat_key,
            text_splitter=self.agent_message_splitter_provider,
            encoder_model=self.agent_embedding_model_provider,
            encoder_model_options=self.agent_embedding_model_options,
            search_limit=1000,
            search_min_score=0.3,
        )

    def get_actor(self, prompts):
        return Actor(
            self,
            language_model=self.agent_primary_model_provider,
            language_model_options=self.agent_primary_model_options,
            prompts=prompts,
            output_token_percent=0.35,
        )

    def event_processor(self):
        # Initialize cycle
        try:
            self._initialize_cycle(
                self.agent_sensor,
                {
                    "system": self.command.agent_system_template,
                    "tools": self.command.agent_tools_template,
                    "request": self.command.agent_template,
                },
            )
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(self.agent_channel, error)
            raise

        # Execute cycle
        try:
            for event in self.communication.listen(
                self.agent_sensor_filters, self.agent_message_fields, self.agent_sensor_id_field
            ):
                response = self.profile(self.process_sensory_event, event)
                self.communication.send(self.agent_channel, event, response.export())
                self.finalize_event_response(event, response)
        except Exception as error:
            self.error_handler.handle(error)
            raise

        # Finalize cycle
        try:
            self._finalize_cycle()
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(self.agent_channel, error)
            raise

    def assistant(self):
        chat_channel = "chat:message"

        # Initialize cycle
        try:
            self._initialize_cycle(
                chat_channel,
                {
                    "system": self.command.agent_system_template,
                    "assistant": self.command.agent_assistant_template,
                },
            )
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(chat_channel, error)
            raise

        # Execute cycle
        try:
            for event in self.communication.listen(
                {"mentions_me": "message"},
                ["user", "name", "message"],
            ):
                response = self.profile(self.process_chat_message, event)
                self.communication.send(chat_channel, event, response.export())
                self.finalize_event_response(event, response)
        except Exception as error:
            self.error_handler.handle(error)
            raise

        # Finalize cycle
        try:
            self._finalize_cycle()
        except Exception as error:
            self.error_handler.handle(error)
            self.communication.send_error(chat_channel, error)
            raise

    def _initialize_cycle(self, sensor_name, prompts):
        self.manager.load_templates()

        if self.agent_user:
            self._user.set_active_user(self.get_instance(self._user, self.agent_user, required=True))

        self.error_handler = self.get_error_handler()

        self.actor = self.get_actor(prompts)
        self.communication = self.get_communication_processor()
        self.communication.set_sensor(sensor_name)

        self.initialize_cycle()

    def initialize_cycle(self):
        """Override in subclasses to extend cell cycle initialization"""
        pass

    def process_sensory_event(self, event):
        return self.actor.respond(event.message, self.agent_memory_search_field, self.agent_message_field_labels)

    def process_chat_message(self, event):
        return self.actor.assist(
            event.message,
            "message",
            {
                "user": "Zimagi Username",
                "name": "Chat Name",
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
