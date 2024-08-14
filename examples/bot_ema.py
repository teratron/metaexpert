import time
import numpy
from expert import Expert


def main() -> None:
    bot = Expert("BTCUSDT",)

    close = numpy.random.randn(100)

    ema = talib.MA(close, timeperiod=3, matype=talib.MA_Type.EMA)
    print(ema)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Elapsed time: {time.time() - start}")
