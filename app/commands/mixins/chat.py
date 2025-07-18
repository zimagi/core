from systems.cell.memory import MemoryManager
from systems.commands.index import CommandMixin


class ChatMixin(CommandMixin("chat")):

    def get_memory_manager(self, search_limit=None, search_min_score=None):
        return MemoryManager(
            self,
            self.active_user,
            search_limit=search_limit,
            search_min_score=search_min_score,
        )

    def save_user_message(self, chat_name, message, time=None, user=None, role="user"):
        user = user if user else self.active_user.name
        time = time if time else self.time.now
        (
            self.get_memory_manager()
            .set_chat(chat_name)
            .add({"role": role, "content": message, "sender": user, "created": self.time.to_datetime(time)})
            .save()
        )
