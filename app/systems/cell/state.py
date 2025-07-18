import copy
import logging
import threading

from utility.data import dump_json

logger = logging.getLogger(__name__)


class StateManager:
    lock = threading.Lock()

    def __init__(self, command, state_key, default_state):
        self.command = command
        self.state_key = state_key
        self.default_state = default_state
        self._state = {}
        self.load()

    def load(self):
        self._state = self.command.get_state(
            self.state_key,
            self.default_state,
        )
        logger.debug(f"Loaded agent state: {self._state}")
        return self._state

    def save(self, state):
        self._state = state
        self.command.set_state(self.state_key, self._state)
        logger.debug(f"Agent state saved: {self._state}")
        return self._state

    def __iter__(self):
        with self.lock:
            return iter(self._state)

    def __len__(self):
        return len(self._state)

    def __contains__(self, name):
        return name in self._state

    def __setitem__(self, name, value):
        with self.lock:
            self._state[name] = value
            self.save(self._state)

    def __setattr__(self, name, value):
        self.__setitem__(name, value)

    def set(self, name, value):
        self.__setitem__(name, value)

    def __delitem__(self, name):
        with self.lock:
            del self._state[name]
            self.save(self._state)

    def __delattr__(self, name):
        self.__delitem__(name)

    def delete(self, name):
        self.__delitem__(name)

    def clear(self):
        with self.lock:
            self._state.clear()
            self.save(self._state)

    def items(self):
        with self.lock:
            return self._state.items()

    def __getitem__(self, name):
        if name not in self._state:
            return None
        return self._state[name]

    def __getattr__(self, name):
        return self.__getitem__(name)

    def get(self, name, default=None):
        if name not in self._state:
            return default
        return self._state[name]

    def export(self):
        return copy.deepcopy(self._state)

    def __str__(self):
        return dump_json(self._state, indent=2)

    def __repr__(self):
        return self.__str__()
