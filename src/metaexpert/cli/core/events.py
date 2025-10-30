"""Event bus for CLI applications."""

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any

from metaexpert.logger import get_logger


class EventType(str, Enum):
    """CLI event types."""

    COMMAND_START = "command:start"
    COMMAND_END = "command:end"
    COMMAND_ERROR = "command:error"
    PROCESS_START = "process:start"
    PROCESS_STOP = "process:stop"
    CONFIG_CHANGED = "config:changed"


@dataclass
class Event:
    """CLI event."""

    type: EventType
    data: dict[str, Any]


class EventBus:
    """Central event bus for CLI."""

    def __init__(self):
        self._subscribers: dict[EventType, list[Callable]] = {}
        self.logger = get_logger(__name__)

    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        """
        Subscribe to event.

        Args:
            event_type: Type of event to subscribe to
            handler: Callable to execute when event is published
        """
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

        self.logger.debug(
            f"Subscribed handler to event: {event_type}",
            event_type=event_type,
            handler=handler.__name__,
        )

    def publish(self, event: Event) -> None:
        """
        Publish event.

        Args:
            event: Event to publish
        """
        handlers = self._subscribers.get(event.type, [])

        self.logger.debug(
            f"Publishing event: {event.type}",
            event_type=event.type,
            handler_count=len(handlers),
        )

        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                self.logger.error(
                    f"Event handler failed: {e}",
                    event_type=event.type,
                    handler=handler.__name__,
                    error=str(e),
                )


# Global event bus instance
_event_bus = EventBus()


def get_event_bus() -> EventBus:
    """Get the global event bus instance."""
    return _event_bus
