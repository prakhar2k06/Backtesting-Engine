from collections import deque
from core.event import Event

class EventQueue:
    def __init__(self):
        self._queue = deque()
    
    def push_event(self, event: Event) -> None:
        self._queue.append(event)
    
    def pop_event(self) -> Event:
        if not self.is_empty():
            raise IndexError("EventQueue is empty")
        
        return self._queue.popleft()

    def is_empty(self) -> bool:
        return len(self._queue) == 0


