import inspect
from pathlib import Path
from typing import Any, Callable

from logger import Logger, get_logger
from metaexpert._event import Event


class Process(Event):
    __events: set[str] = {
        "on_init", "on_deinit", "on_trade", "on_transaction", "on_tick", "on_bar", "on_timer", "on_book"
    }
    symbol: str | set[str] | None
    timeframe: str | set[str] | None

    # shift: int
    # magic: int
    # filename: str | None

    def __init__(self, name: str) -> None:
        super().__init__()
        self.logger: Logger = get_logger(name)
        # self.event: Event = Event()

        # self.fill()

    def _run(self, event: str | set[str], count: int = 1) -> None:
        frame = inspect.stack()[len(inspect.stack()) - 1]
        module = inspect.getmodule(frame[0])

        # Obtaining a file name
        self.filename = Path(frame[1]).stem
        self.logger.debug("Processing file: %s", self.filename)

        if module:
            num: int = 0
            dec: set[str] = {event} if isinstance(event, str) else event

            for attr in dir(module):
                # All objects of the module.
                obj: object | None = module.__dict__.get(attr)

                # Only module functions.
                # All the functions of the module with decorators or without shortcuts.
                if obj and callable(obj) and not isinstance(obj, type):
                    # List of hierarchy of objects, functions, decorators or closes.
                    qualif: list[str] = obj.__qualname__.split(".")

                    if len(qualif) > 1:
                        if qualif[0] == __class__.__name__ or qualif[0] == self.__class__.__name__:
                            if any(qualif[1] == item for item in dec) and num < count:
                                num += 1
                                # asyncio.run(getattr(module, attr)())
                                getattr(module, attr)()
                                self.logger.debug("Launch task for @%s:%s()", qualif[1], attr)
                        elif any(qualif[0] == item for item in dec):
                            getattr(module, attr)()
                            self.logger.debug("Launch task for %s()", attr)

    def on_init(
            self,
            symbol: str | set[str] | None = None,
            timeframe: str | set[str] | None = None,
            *,
            shift: int = 0,
            magic: int = 0,
            name: str | None = None
    ) -> Callable:
        """Decorator for initialization event handling.

        Args:
            symbol (str | None): Symbol of the trading pair.
            timeframe (str | None): Time frame for the trading data.
            shift (int): A shift relative to the current bar on which the expert is traded. Defaults to 0.
            magic (int): Magic number. Used to identify the expert. Defaults to 0.
            name (str | None): The name of the expert.
            
        Returns:
            Callable: Decorated function that handles the initialization event.
        """

        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], Callable]) -> Callable:  # InitStatus:
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
        ) -> Callable[[tuple[Any, ...], dict[str, Any]], None]:
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
