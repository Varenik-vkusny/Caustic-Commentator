from collections import deque

class NarrativeState:
    def __init__(self, max_history=5):
        self.history = deque(maxlen=max_history)
        self.last_narration = ""

    def add_event(self, description):
        self.history.append(description)
        self.last_narration = description

    def get_context(self):
        """Returns a summarized string of recent events."""
        return " -> ".join(list(self.history))
