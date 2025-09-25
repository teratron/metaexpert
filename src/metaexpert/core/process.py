import asyncio
import inspect
from asyncio import Task
from enum import Enum
from logging import Logger
from threading import Thread
from types import ModuleType
from typing import Self

from metaexpert.config import APP_NAME
from metaexpert.logger import get_logger
from metaexpert.websocket import WebSocketClient

from ._event_handler import EventHandler

logger: Logger = get_logger(APP_NAME)


class Process(Enum):
    """Event types for the trading system.

    Each event type has a maximum number of callbacks defined by the 'max_callbacks' field.
    """

    ON_INIT = {
        "name": "on_init",
        "max_callbacks": 1,
        "callback": [],
        "is_async": False,
        # "status": None,  # InitStatus.INIT_SUCCEEDED
        "is_done": False,
    }
    ON_DEINIT = {
        "name": "on_deinit",
        "max_callbacks": 1,
        "callback": [],
        "is_async": False
    }
    ON_TICK = {
        "name": "on_tick",
        "max_callbacks": 1,
        "callback": [],
        "is_async": True
    }
    ON_BAR = {
        "name": "on_bar",
        "max_callbacks": 5,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_TIMER = {
        "name": "on_timer",
        "max_callbacks": 5,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_TRANSACTION = {
        "name": "on_transaction",
        "max_callbacks": 1,
        "callback": [],
        "is_async": True
    }
    ON_BOOK = {
        "name": "on_book",
        "max_callbacks": 1,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_ORDER = {
        "name": "on_order",
        "max_callbacks": 1,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_POSITION = {
        "name": "on_position",
        "max_callbacks": 1,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_ERROR = {
        "name": "on_error",
        "max_callbacks": 1,
        "callback": [],
        "is_async": False
    }
    ON_ACCOUNT = {
        "name": "on_account",
        "max_callbacks": 1,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_BACKTEST_INIT = {
        "name": "on_backtest_init",
        "max_callbacks": 1,
        "callback": [],
        "is_async": False
    }
    ON_BACKTEST_DEINIT = {
        "name": "on_backtest_deinit",
        "max_callbacks": 1,
        "callback": [],
        "is_async": False
    }
    ON_BACKTEST = {
        "name": "on_backtest",
        "max_callbacks": 1,
        "callback": [],
        "instance": [],
        "is_async": True
    }
    ON_BACKTEST_PASS = {
        "name": "on_backtest_pass",
        "max_callbacks": 1,
        "callback": [],
        "is_async": False
    }

    def __new__(cls, value: dict):
        """Create a new enum member with a copy of the provided value."""
        obj = object.__new__(cls)
        # Create a copy of the dictionary and ensure mutable lists are independent
        obj._value_ = {k: v if not isinstance(v, list) else [] for k, v in value.items()}
        return obj

    @classmethod
    def init(cls) -> ModuleType | None:
        """Initialize the process.

        This method is called to set up the process and register callbacks.
        It inspects the current module to find functions decorated with
        specific event decorators and registers them as callbacks for the
        corresponding events.
        """
        frame = inspect.stack()[len(inspect.stack()) - 1]
        module: ModuleType | None = inspect.getmodule(frame[0])
        if module is None:
            return None

        for attr in dir(module):
            # All objects of the module.
            obj: object | None = module.__dict__.get(attr)

            # All the functions of the module with decorators or without shortcuts.
            if obj and callable(obj) and not isinstance(obj, type):
                # List of hierarchy of objects, functions, decorators or closes.
                qualname_parts: list[str] = getattr(obj, "__qualname__", "").split(".")
                if len(qualname_parts) > 1:
                    cls._push_callback(qualname_parts[1], (module, attr))

        return module

    @classmethod
    def _get_process_from(cls, name: str) -> Self | None:
        """Get a process by its name.

        This method searches for a process in the enumeration by its name.

        Args:
            name (str): The name of the process to search for.

        Returns:
            Self | None: The process if found, otherwise None.
        """
        for item in cls:
            if item.value.get("name") == name.lower():
                return item

        return None

    @classmethod
    def _push_callback(cls, name: str, args: tuple[ModuleType, str]) -> None:
        """Push a callback to the process.

        This method registers a callback function for a specific event.
        It checks if the event exists and if the number of callbacks does not exceed the limit.
        If the event does not exist or the number of callbacks exceeds the limit, it logs a warning.

        Args:
            name (str): The name of the event to register the callback for.
            args (tuple[ModuleType, str]): A tuple containing the module and the function name to register as a callback.
        """
        event = cls._get_process_from(name)
        if event is None:
            return

        callback = event.value.get("callback")
        if not isinstance(callback, list):
            return

        max_callbacks = event.value.get("max_callbacks")
        if not isinstance(max_callbacks, int):
            return

        if len(callback) < max_callbacks:
            callback.append(getattr(*args))
            logger.debug(
                "Registering callback for '%s:%s()'",
                event.value.get("name"), args[1]
            )
        else:
            logger.warning(
                "Too many callbacks for '%s': %d",
                name, max_callbacks + 1
            )

    def push_instance(self, instance: EventHandler) -> None:
        """Push an instance to the process.

        This method adds an instance to the process's list of instances.
        It is used to register instances that need to be notified when the event occurs.
        """
        if not isinstance(self.value.get("instance"), list):
            logger.error("Instances for '%s' are not a list", self.value.get("name"))
            return

        self.value["instance"].append(instance)
        logger.debug("Instance added for '%s'", self.value.get("name"))

    def pop_instance(self) -> EventHandler | None:
        """Pop an instance from the process.

        This method removes the last instance from the process's list of instances.
        It is used to unregister instances that no longer need to be notified when the event occurs.
        """
        if not isinstance(self.value.get("instance"), list):
            logger.error("Instances for '%s' are not a list", self.value.get("name"))
            return None

        if self.value["instance"]:
            instance = self.value["instance"].pop()
            logger.debug("Instance removed for '%s': %s", self.value.get("name"), instance)
            return instance

        return None

    def check_instance(self) -> bool:
        """Check if there are any instances registered for the process.

        This method checks if the process has any instances registered.
        It returns True if there are instances, otherwise False.
        """
        if not isinstance(self.value.get("instance"), list):
            logger.error("Instances for '%s' are not a list", self.value.get("name"))
            return False

        has_instances = bool(self.value["instance"])
        logger.debug("Process '%s' has instances: %s", self.value.get("name"), has_instances)
        return has_instances

    def run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        If the process is marked as asynchronous, it runs the callbacks using asyncio.
        """
        if self.value.get("is_async"):
            asyncio.run(self._run_async())
        else:
            self._run()

    def _run(self) -> None:
        """Run the process.

        This method executes the registered callbacks for the event.
        """
        callback = self.value.get("callback")
        if not isinstance(callback, list):
            logger.error("Callbacks for '%s' are not a list", self.value.get("name"))
            return

        for func in callback:
            func()
            logger.debug("Launch task for '%s'", self.value.get("name"))

        if "is_done" in self.value and not self.value.get("is_done"):
            self.value["is_done"] = True
            logger.debug("Process '%s' is done", self.value.get("name"))

    async def _run_async(self) -> None:
        """Run the process asynchronously.

        This method executes the registered callbacks for the event asynchronously.
        """
        callback = self.value.get("callback")
        if not isinstance(callback, list):
            logger.error("Callbacks for '%s' are not a list", self.value.get("name"))
            return

        logger.debug("Launch task for '%s(s)'", self.value.get("name"))
        tasks = self._get_tasks() or []
        await asyncio.gather(*tasks)

    def _get_tasks(self) -> list[Task] | None:
        """Get the tasks for the process.

        This method retrieves the registered callbacks for the event and creates asyncio tasks for them.
        It returns a list of asyncio tasks or None if there are no valid callbacks.
        """
        callback = self.value.get("callback")
        if not isinstance(callback, list):
            logger.error("Callbacks for '%s' are not a list", self.value.get("name"))
            return None

        tasks: list[Task] = []
        for func in callback:
            if func and callable(func) and inspect.iscoroutinefunction(func):
                tasks.append(asyncio.create_task(func()))

        return tasks

    @classmethod
    def processing(cls, ws_url: str) -> bool:
        """Process the events for the trading system.

        This method initializes the process and starts running the tasks.
        It checks if the process is already initialized and if not, it starts a new thread to run the tasks.
        It returns True if the process was successfully initialized, otherwise False.
        """
        # if not cls.ON_INIT.value.get("is_done"):
        #     return False

        Thread(
            target=WebSocketClient,
            args=(ws_url,),
            daemon=True
        ).start()

        Thread(target=cls._run_tasks, daemon=True).start()

        return True

    @classmethod
    def _run_tasks(cls) -> None:
        """Run the tasks for the process.

        This method gathers all tasks for the processes that are marked as asynchronous.
        It runs the tasks in an asyncio event loop.
        """
        asyncio.run(cls._gather_tasks())

    @classmethod
    async def _gather_tasks(cls) -> None:
        """Gather all tasks for the processes.

        This method collects all tasks for the processes that are marked as asynchronous.
        It iterates through the processes and gathers their tasks into a single list.
        If any process fails to gather tasks, it logs an error message.
        """
        tasks: list[Task] = []
        for item in cls:
            if item.value.get("is_async"):
                task = item._get_tasks()
                if isinstance(task, list):
                    tasks.extend(task)
                else:
                    logger.error("Failed to gather tasks for '%s'", item.value.get("name"))
                    return

        await asyncio.gather(*tuple(tasks))
