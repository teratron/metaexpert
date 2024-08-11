import pandas
from lightweight_charts import Chart
from _logger import getLogger

logger = getLogger()

if __name__ == "__main__":
    logger.info("start chart")
    chart = Chart()

    # Columns: time | open | high | low | close | volume
    df = pandas.read_csv("data/ohlcv.csv")
    chart.set(df)

    chart.show(block=True)
