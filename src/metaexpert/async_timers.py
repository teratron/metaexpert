import asyncio
import time


class AsyncTimer:
    def __init__(self, name, interval):
        self.name = name
        self.interval = interval
        self.is_running = False
        self.start_time = None
        self.elapsed_time = 0

    async def start(self):
        self.is_running = True
        self.start_time = time.time()
        print(f"Таймер {self.name} запущен.")

        while self.is_running:
            await asyncio.sleep(self.interval)
            self.elapsed_time += self.interval
            print(f"Таймер {self.name}: прошло {self.elapsed_time:.1f} секунд")

    def stop(self):
        if self.is_running:
            self.is_running = False
            print(
                f"Таймер {self.name} остановлен. Общее время: {self.elapsed_time:.1f} секунд"
            )


async def main():
    # Создаем два таймера с разными интервалами
    timer1 = AsyncTimer("#1", 1.0)  # интервал 1 секунда
    timer2 = AsyncTimer("#2", 2.5)  # интервал 2.5 секунды

    # Запускаем оба таймера одновременно
    task1 = asyncio.create_task(timer1.start())
    task2 = asyncio.create_task(timer2.start())

    # Даем таймерам поработать 10 секунд
    # await asyncio.sleep(10)

    # Останавливаем таймеры
    timer1.stop()
    timer2.stop()

    # Ждем завершения задач
    await asyncio.gather(task1, task2)

    print("Программа завершена.")


if __name__ == "__main__":
    # Запускаем асинхронную функцию main
    asyncio.run(main())
