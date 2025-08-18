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

    def save_user_message(self, chat_name, message, user=None, role="user"):
        if not user:
            user = self.active_user.name

        self.get_memory_manager().set_sequence(chat_name).add({"role": role, "content": message, "sender": user}).save()
