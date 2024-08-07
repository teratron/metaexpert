"""Logging

NOTSET < DEBUG < INFO < WARNING < ERROR < CRITICAL

- DEBUG - самая подробная информация, нужна только разработчику и только для отладки,
          например значения переменных,
          какие данные получены и т.д.
- INFO - информационные сообщения, как подтверждение работы, например запуск сервиса.
- WARNING - еще не ошибка, но уже надо посмотреть - мало места на диске, мало памяти,
            много созданных объектов и т.д.
- ERROR - приложение еще работает и может работать, но что-то пошло не так.
- CRITICAL - приложение не может работать дальше.
"""
import os
from logging import getLogger
from dotenv_vault import load_dotenv

# Dotenv
global log_config, log_file
if load_dotenv():
    log_config = os.getenv("LOG_CONFIG", "logger.json")
    log_file = os.getenv("LOG_FILE", "data.log")

# Load config
if os.path.isfile(log_config):
    import json
    from logging.config import dictConfig

    with open(log_config) as file:
        config = json.load(file)

    dictConfig(config)
else:
    import sys
    from logging import basicConfig, FileHandler, StreamHandler, DEBUG, WARNING

    log_format = "%(asctime)s %(levelname)s: %(name)s: %(message)s"

    # Console
    stream_handler = StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(DEBUG)

    # File
    file_handler = FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(WARNING)

    basicConfig(level=DEBUG, format=log_format, handlers=[stream_handler, file_handler])

    stream_handler.close()
    file_handler.close()

logger = getLogger(__name__)
