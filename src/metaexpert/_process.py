# -*- coding: utf-8 -*-

import inspect
from pathlib import Path

from logger import Logger, get_logger
from metaexpert._event import Event


class Process:
    def __init__(self, name: str) -> None:
        """Initialize the process.

        Args:
            name (str): Name of the library.
        """
        self.logger: Logger = get_logger(name)
        self.module: object | None = None
        self.filename: str | None = None

    def init_process(self) -> None:
        """Initialize the process.

        This method is called to set up the process and register callbacks.
        It inspects the current module to find functions decorated with
        specific event decorators and registers them as callbacks for the
        corresponding events.
        """
        frame = inspect.stack()[len(inspect.stack()) - 1]
        module = inspect.getmodule(frame[0])

        if module:
            self.module = module
            self.filename = Path(frame[1]).stem

            for attr in dir(module):
                # All objects of the module.
                obj: object | None = module.__dict__.get(attr)

                # Only module functions.
                # All the functions of the module with decorators or without shortcuts.
                if obj and callable(obj) and not isinstance(obj, type):
                    # List of hierarchy of objects, functions, decorators or closes.
                    qualif: list[str] = obj.__qualname__.split(".")

                    if len(qualif) > 1:
                        event = Event.get_event_from(qualif[1])

                        if event:
                            if len(event.value["callback"]) < event.value["number"]:
                                event.value["callback"].append(getattr(module, attr))
                            else:
                                self.logger.warning(
                                    "Too many callbacks for %s: %d",
                                    qualif[1], event.value["number"] + 1
                                )

    def run_process(self, event: Event) -> None:
        """Run the process.

        Args:
            event (Event): Event to be executed.
        """
        if event in Event:
            for callback in event.value["callback"]:
                callback()
                self.logger.debug("Launch task for %s()", event.value["name"])
        else:
            self.logger.warning("Process %s not found", event.value["name"])
