import inspect
from enum import Enum, unique
from functools import update_wrapper
from typing import Any, Callable, Coroutine, TypeVar, cast

from logger import Logger, getLogger

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
    __events: list[str] = ["on_deinit", "on_trade", "on_transaction", "on_tick", "on_bar", "on_timer", "on_book"]
    # "on_init",
    symbol: str | None
    time_frame: str | None
    shift: int
    magic: int
    name: str

    def __init__(self, name) -> None:
        # self,
        # symbol: str | set[str] | None,
        # time_frame: str | set[str] | None = None,
        # *,
        # shift: int = 0,
        # period: int = 1,
        # magic: int = 0,
        # title: str = "",
        # prefix: str = "_",
        # ** props: dict[str, Any]
        self.logger: Logger = getLogger(__name__)
        # self.run()
        # self._run_event("on_init")

    def __str__(self) -> str:
        return f"{type(self).__name__} {self.name}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name!r}>"

    def run(self) -> None:
        self._run_event("on_init")
        # self._run_event(self.__events)

    def _run_event(self, decorator: str | list[str]) -> None:
        frame = inspect.stack()[len(inspect.stack()) - 1]
        # [print(i) for i in inspect.stack()]
        # print(len(inspect.stack()))
        # print(inspect.stack()[3])
        # [print(i) for i in inspect.stack()[3]]
        module = inspect.getmodule(frame[0])
        # print(module.__dict__)

        if module:
            for attr in dir(module):
                # Все объекты модуля.
                obj: Any | None = module.__dict__.get(attr)
                # print(attr, obj)

                # Только функции модуля
                if obj and callable(obj) and not isinstance(obj, type):
                    # Все функции модуля с декораторами или замыканиями или без них.
                    # Список иерархии объектов, функций, декораторов или замыканий.
                    qualif: list[str] = obj.__qualname__.split(".")
                    # print(qualif)

                    if len(qualif) > 1:
                        if qualif[0] == __class__.__name__ or qualif[0] == self.__class__.__name__:
                            if (isinstance(decorator, list) and any(qualif[1] == item for item in decorator)) or (
                                    isinstance(decorator, str) and qualif[1] == decorator):
                                # asyncio.run(getattr(mod, attr)())
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
            time_frame: str | None = None,
            *,
            shift: int = 0,
            magic: int = 0,
            name: str | None = None
    ) -> Callable:
        """Decorator for initialization event handling.

        Args:
            symbol (str | None): Symbol of the trading pair.
            time_frame (str | None): Time frame for the trading data.
            shift (int, optional): Shift value. Defaults to 0.
            magic (int, optional): Magic number. Defaults to 0.
            name (str | None): Name of the process.
            
        Returns:
            Callable: Decorated function that handles the initialization event.
            
        :param symbol: Инструмент с которым работает эксперт.
        :type symbol: `str` or `None`
        :param time_frame: Таймфрейм, по которому осуществляется торговля эксперт.
        :type time_frame: `str` or `set[str]` or `None`
        :param shift: Сдвиг относительно текущего бара, бар на котором осуществляется торговля эксперта.
        :type shift: `int`
        :param period: Период (интервал) баров на котором осуществляется торговля и/или прорисовка эксперта.
        :type period: `int`
        :param magic: Магический номер. Используется для идентификации эксперта.
        :type magic: `int`
        :param name: Название процесса.
        :type name: `str` or `None`
        :return: Декорированная функция, обрабатывающая событие инициализации.
        :rtype: Callable
        """

        def outer(func: Callable[[tuple[Any, ...], dict[str, Any]], InitStatus]) -> Callable:  # InitStatus:
            def inner(*args, **kwargs) -> None:
                self.symbol = symbol
                self.time_frame = time_frame
                self.shift = shift
                self.magic = magic
                self.name = name

                self.logger.info("Pair: %s, Timeframe: %s", args.pair, args.timeframe)

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
