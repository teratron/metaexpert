import inspect
import platform
from enum import Enum, unique
from functools import update_wrapper
from pathlib import Path
from typing import Any, Callable, Coroutine, TypeVar, cast, Iterable

from logger import Logger, get_logger

F = TypeVar("F", bound=Callable[..., Any])


def setup_method(f: F) -> F:
    def wrapper_func(self, *args: Any, **kwargs: Any) -> Any:
        return f(self, *args, **kwargs)

    return cast(F, update_wrapper(wrapper_func, f))


@unique
class InitStatus(Enum):
    """Initialization status codes."""
    INIT_UNKNOWN = 0
    INIT_SUCCEEDED = 1
    INIT_FAILED = 2
    INIT_PARAMETERS_INCORRECT = 3


class Process:
    __events: set[str] = {
        "on_init", "on_deinit", "on_trade", "on_transaction", "on_tick", "on_bar", "on_timer", "on_book"
    }
    symbol: str | set[str] | None
    timeframe: str | set[str] | None
    shift: int = 0
    magic: int = 0
    name: str = ""

    def __init__(self, name) -> None:
        self.logger: Logger = get_logger(name)

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    def run(self) -> None:
        try:
            # Initialize and run the trading bot
            self._run_event("on_init")
            self.logger.info("Expert initialized successfully")

            # self._run_event(self.__events)
            # while True:
            #     pass
        except KeyboardInterrupt:
            self.logger.info("Expert stopped by user")
        except (ConnectionError, TimeoutError) as e:
            self.logger.exception("An error occurred: %s", e)
        finally:
            self._run_event("on_deinit")
            self.logger.info("Expert shutdown complete")

    def _get_name_module(self, path: str) -> str:
        frame = inspect.stack()[len(inspect.stack()) - 1]
        name = frame[1]

        match platform.system():
            case "Windows":
                name = name.split("\\")[-1]
            case "Linux" | "Darwin":
                name = name.split("/")[-1]

        return name.split(".")[0]

    def _run_event(self, decorator: str | Iterable[str]) -> None:
        frame = inspect.stack()[len(inspect.stack()) - 1]
        # [print(i) for i in inspect.stack()]
        # print(len(inspect.stack()))
        # print(inspect.stack()[3])
        #[print(i) for i in inspect.stack()[3]]
        module = inspect.getmodule(frame[0])
        # print(frame[1].split("\\")[-1].split(".")[0])

        # Получение имени файла
        self.name = Path(frame[1]).stem
        self.logger.debug("Processing file: %s", self.name)

        if module:
            for attr in dir(module):
                # All objects of the module.
                obj: Any | None = module.__dict__.get(attr)
                # print(attr, obj)

                # Only module functions.
                # All the functions of the module with decorators or without shortcuts.
                if obj and callable(obj) and not isinstance(obj, type):
                    # List of hierarchy of objects, functions, decorators or closes.
                    qualif: list[str] = obj.__qualname__.split(".")

                    if len(qualif) > 1:
                        if qualif[0] == __class__.__name__ or qualif[0] == self.__class__.__name__:
                            if (isinstance(decorator, Iterable) and any(qualif[1] == item for item in decorator)) or (
                                    isinstance(decorator, str) and qualif[1] == decorator):
                                # asyncio.run(getattr(module, attr)())
                                getattr(module, attr)()
                                self.logger.debug("Launch task for @%s:%s()", qualif[1], attr)
                        elif any(qualif[0] == item for item in ["on_process"]):
                            getattr(module, attr)()
                            self.logger.debug("Launch task for %s()", attr)

    @setup_method
    def on_process(self) -> None:
        print("*** expert.on_process ***")

    def on_init(
            self,
            symbol: str | None = None,
            timeframe: str | None = None,
            *,
            shift: int = 0,
            magic: int = 0,
            name: str | None = None
    ) -> Callable:
        """Decorator for initialization event handling.

        Args:
            symbol (str | None): Symbol of the trading pair.
            timeframe (str | None): Time frame for the trading data.
            shift (int, optional): A shift relative to the current bar on which the expert is traded. Defaults to 0.
            magic (int, optional): Magic number. Used to identify the expert. Defaults to 0.
            name (str | None): The name of the expert.
            
        Returns:
            Callable: Decorated function that handles the initialization event.
        """
        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], InitStatus]) -> Callable:  # InitStatus:
            def inner(*args, **kwargs) -> None:
                self.symbol = symbol
                self.timeframe = timeframe
                self.shift = shift
                self.magic = magic
                self.name = name

                # self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)

                func(*args, **kwargs)

            return inner  # InitStatus.INIT_SUCCEEDED

        return outer

    def on_deinit(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_trade(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    def on_transaction(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    # def on_tick(self, func: Callable[[], None]) -> Callable[[], Coroutine[Any, Any, None]]:
    def on_tick(self, func: Callable) -> Callable:
        def inner(*args, **kwargs) -> None:
            # task = asyncio.create_task(func())
            # task
            func(*args, **kwargs)
            # await self.__tick()
            # task = asyncio.create_task(self.__tick())
            # await task
            # i = 3
            # while i > 0:
            #     func()
            #     print(self, " ", i)
            #     i -= 1
            # return func()

        return inner

    # Call: TypeAlias = Callable[[list[Any], dict[str, Any]], None]

    def on_bar(self, time_frame: str = "1h") -> Callable:
        def outer(
                func: Callable[[tuple[Any, ...], dict[str, Any]], None],
        ) -> Callable[[tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, None]]:
            def inner(*args, **kwargs) -> None:
                func(*args, **kwargs)
                print(time_frame)

            return inner

            # async def async_inner(*args, **kwargs) -> None:
            #     await func(*args, **kwargs)
            #     print(time_frame)
            #
            # return async_inner

        return outer

    def on_timer(self, interval: int = 1000) -> Callable:
        """Decorator for timer-based event handling.

        Args:
            interval (int, optional): Time interval in milliseconds. Defaults to 1000.

        Returns:
            Callable: Decorated function that executes at specified intervals.
        """

        def outer(func: Callable) -> Callable:
            def inner() -> None:
                func()
                print(interval)

            return inner

        return outer

    def on_book(self, func: Callable) -> Callable:
        def inner() -> None:
            func()

        return inner

    async def __tick(self):
        print("__tick")

    # @property
    # def magic(self) -> int:
    #     return self._magic
    #
    # @magic.setter
    # def magic(self, value: int) -> None:
    #     self._magic = value
    #
    # @property
    # def comment(self) -> str:
    #     return self.__comment
    #
    # @comment.setter
    # def comment(self, value: str) -> None:
    #     self.__comment = value + f"Magic number: {self._magic}"
