"""Small, bounded memory for the simulated companion brain.

This is local in-process memory, not a learned model or persistent database.
"""
from collections import deque
from dataclasses import dataclass
from time import time


@dataclass(frozen=True)
class MemoryEvent:
    timestamp: float
    kind: str
    detail: str


class EpisodicMemory:
    """Keep recent events and expose a compact summary for decision-making."""

    def __init__(self, capacity: int = 100) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._events: deque[MemoryEvent] = deque(maxlen=capacity)

    def remember(self, kind: str, detail: str) -> None:
        self._events.append(MemoryEvent(time(), kind, detail))

    def recent(self, limit: int = 10) -> tuple[MemoryEvent, ...]:
        if limit < 0:
            raise ValueError("limit must be non-negative")
        return tuple(self._events)[-limit:] if limit else ()

    def count(self, kind: str | None = None) -> int:
        if kind is None:
            return len(self._events)
        return sum(event.kind == kind for event in self._events)
