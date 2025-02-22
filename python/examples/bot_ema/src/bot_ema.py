import time
#import numpy
#import talib
from python.expert.src.expert import Expert

expert = Expert("BTCUSDT", "1h", shift=0, period=3)


def on_process() -> None:
    print("*** on_process ***")


@expert.on_init
def init() -> None:
    print("*** on_init ***")


@expert.on_deinit
def deinit() -> None:
    print("*** on_deinit ***")


@expert.on_trade
def trade() -> None:
    print("*** on_trade ***")


@expert.on_tick
def tick() -> None:
    print("*** on_tick ***")


@expert.on_bar("1h")
def bar() -> None:
    print("*** on_bar ***")


@expert.on_timer(1042)
def timer() -> None:
    print("*** on_timer ***")


def main() -> None:
    expert.trade(lots=0.0001, stop_loss=0.0001, take_profit=0.0001, trailing_stop=0.0001)
    expert.positions = 2
    expert.slippage = 10

    expert.run()

    # close = numpy.random.randn(20)
    # ema_slow = talib.MA(close, timeperiod=7, matype=talib.MA_Type.EMA)
    # ema_fast = talib.EMA(close, timeperiod=3)
    # print(ema_slow)
    # print(ema_fast)
    # ema_slow.dtype(numpy.float64)
    # ema_fast.dtype(numpy.float64)
    # ema_cross = numpy.cross(ema_slow, ema_fast)
    # print(ema_cross)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Elapsed time: {time.time() - start}")
