# import numpy
# import talib
import os

from metaexpert import MetaExpert

expert = MetaExpert(
    stock="binance",
    api_key=os.getenv("BINANCE_API_KEY"),
    api_secret=os.getenv("BINANCE_API_SECRET"),
    base_url=os.getenv("BINANCE_BASE_URL"),
    # instrument="spot",
    instrument="futures",
    contract="coin_m",
    mode="paper",
)

expert.balance()


@expert.on_init("BTCUSDT", "1h", shift=0, magic=12345, name="EMA Expert")
def init() -> None:
    print("*** on_init ***")


# @expert.on_init("BTCUSDT", "1h", shift=0, magic=12345, name="EMA Expert")
# def init2() -> None:
#     print("*** on_init 2 ***")

@expert.on_deinit
def deinit(reason) -> None:
    print("*** on_deinit ***", reason)


@expert.on_tick
def tick() -> None:
    print("*** on_tick ***")


@expert.on_bar("1h")
def bar(rate) -> None:
    print("*** on_bar ***")
    # close = numpy.random.randn(20)
    # ema_slow = talib.MA(close, timeperiod=7, matype=talib.MA_Type.EMA)
    # ema_fast = talib.EMA(close, timeperiod=3)
    # print(ema_slow)
    # print(ema_fast)
    # ema_slow.dtype(numpy.float64)
    # ema_fast.dtype(numpy.float64)
    # ema_cross = numpy.cross(ema_slow, ema_fast)
    # print(ema_cross)
    print(rate)


@expert.on_timer(1000)
def timer() -> None:
    print("*** on_timer 1000 ***")


@expert.on_timer(3000)
def timer2() -> None:
    print("*** on_timer 3000 ***")


@expert.on_trade
def trade() -> None:
    print("*** on_trade ***")


@expert.on_transaction
def transaction(request, result) -> None:
    print("*** on_transaction ***")


@expert.on_book
def book(symbol) -> None:
    print("*** on_book ***")


def main() -> None:
    expert.run()


if __name__ == "__main__":
    main()
