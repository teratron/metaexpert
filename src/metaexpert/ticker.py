import asyncio
import json
import time
from datetime import datetime

import matplotlib.pyplot as plt
from websocket import WebSocketApp, WebSocket


class Chart:
    def __init__(self) -> None:
        self.x_data: list = []
        self.y_data: list = []
        self.fig = plt.figure()
        self.axe = self.fig.add_subplot(111)
        self.fig.show()

    def update(self, x, y) -> None:
        self.x_data.append(x)
        self.y_data.append(y)
        self.axe.plot(self.x_data, self.y_data, color='blue', label='ETHUSDT')
        self.fig.canvas.draw()
        plt.pause(0.1)

    def stop(self) -> None:
        plt.close(self.fig)


chart = Chart()


def on_open(ws: WebSocket) -> None:
    print("WebSocket connection opened")


def on_close(ws: WebSocket, arg: str, _: str) -> None:
    print("WebSocket connection closed")
    chart.stop()


def on_error(ws: WebSocket, error: Exception) -> None:
    print(f"WebSocket error: {error}")


def on_message(ws: WebSocket, message: str) -> None:
    # print(f"Received message: {message}")
    try:
        data = json.loads(message)['data']
        # print(f"Parsed message: {data}")
        event_time = time.localtime(data['E'] // 1000)
        hour = event_time.tm_hour
        minute = event_time.tm_min
        second = event_time.tm_sec

        print(f"{hour}:{minute}:{second} - {data['c']}")
        # print(f"Time: {ms_to_datetime(data['E'])}  Symbol: {data['s']}")

        chart.update(f"{hour}:{minute}:{second}", float(data['c']))

    except json.JSONDecodeError as e:
        print(f"Failed to parse message: {e}")


def ms_to_datetime(ms: int) -> str:
    """
    Преобразует миллисекунды в формат даты.

    Args:
        ms: время в миллисекундах

    Returns:
        строка с датой в формате 'YYYY-MM-DD HH:MM:SS'
    """
    return datetime.fromtimestamp(ms / 1000).strftime('%Y-%m-%d %H:%M:%S')


def ms_to_datetime_ms(ms: int) -> str:
    """
    Преобразует миллисекунды в формат даты с миллисекундами.

    Args:
        ms: время в миллисекундах

    Returns:
        строка с датой в формате 'YYYY-MM-DD HH:MM:SS.mmm'
    """
    return datetime.fromtimestamp(ms / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


async def main():
    url = "wss://stream.binance.com:9443/stream?streams=ethusdt@miniTicker"
    client = WebSocketApp(
        url=url,
        on_open=on_open,
        on_close=on_close,
        on_error=on_error,
        on_message=on_message
    )
    client.run_forever()


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    # asyncio.set_event_loop(asyncio.new_event_loop())
    # asyncio.run(main())
