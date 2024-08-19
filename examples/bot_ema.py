import time
# import numpy
# import talib
from expert import Expert

expert = Expert("BTCUSDT", "1h", shift=0, period=3)


# @expert.on_init
# def init() -> None:
#     print("*** on_init ***")
#
#
# @expert.on_deinit
# def deinit() -> None:
#     print("*** on_deinit ***")
#
#
# @expert.on_trade
# def trade() -> None:
#     print("*** on_trade ***")
#
#
# @expert.on_tick
# def tick() -> None:
#     print("*** on_tick ***")
#
#
# @expert.on_bar(time_frame="1h")
# def bar() -> None:
#     print("*** on_bar ***")


@expert.on_timer(interval=1000)
def timer() -> None:
    print("*** on_timer ***")


def main() -> None:
    # expert.trade(lots=0.0001, stop_loss=0.0001, take_profit=0.0001, trailing_stop=0.0001)
    # expert.positions = 2
    # expert.slippage = 10.0

    expert.run()
    # print(__name__)
    # print(__file__)

    # close = numpy.random.randn(100)
    # ema = talib.MA(close, timeperiod=3, matype=talib.MA_Type.EMA)
    # print(ema)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Elapsed time: {time.time() - start}")
