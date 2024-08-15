import time
import numpy
import talib
from src._expert import Expert


# @expert.on_init
# @expert.on_deinit
# @expert.on_trade
# @expert.on_tick
# @expert.on_minute
# @expert.on_bar(time_frame="1h")


def main() -> None:
    bot = Expert("BTCUSDT", "1h", shift=0, period=3)

    bot.trade(lots=0.0001, stop_loss=0.0001, take_profit=0.0001, trailing_stop=0.0001)
    bot.positions = 2
    bot.slippage = 10.0


    close = numpy.random.randn(100)
    ema = talib.MA(close, timeperiod=3, matype=talib.MA_Type.EMA)
    print(ema)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Elapsed time: {time.time() - start}")
