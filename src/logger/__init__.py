"""Logger module.

This module provides logging functionality for the trading bot,
including console and file logging with rotation.

Logging levels:

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

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from dotenv_vault import load_dotenv

from src.config import (
    LOG_BACKUP_COUNT,
    LOG_CONFIG,
    LOG_FORMAT,
    LOG_LEVEL,
    LOG_MAX_SIZE,
    LOG_FILE,
    LOG_NAME
)

# Load environment variables
load_dotenv()


def setup_logger(name: str | None = None, level: str | None = None) -> logging.Logger:
    """Set up and configure the logger.

    Args:
        name (str, optional): Logger name. Defaults to None.
        level (str, optional): Logging level. Defaults to None.

    Returns:
        logging.Logger: Configured logger instance.
    """

    # Set default logger name if not provided
    if name is None:
        name = LOG_NAME

    # Create logger instance
    logger = logging.getLogger(name)

    # Check if log config file exists
    if os.path.isfile(LOG_CONFIG):
        import json
        from logging.config import dictConfig

        try:
            # Load config from JSON file
            with open(LOG_CONFIG) as file:
                config = json.load(file)

            dictConfig(config)

            return logger
        except FileNotFoundError as e:
            print(f"Error loading logging configuration file: {e}")

    # Get log level from environment or config
    if level is None:
        level = os.getenv("LOG_LEVEL", LOG_LEVEL)

    # Create logs directory if it doesn't exist
    log_dir: Path = Path(str.join("..", "logs"))
    log_dir.mkdir(exist_ok=True)

    # Configure logger
    logger.setLevel(getattr(logging, level))

    # Clear existing handlers to avoid duplicate logs
    if logger.handlers:
        logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)

    # Create console handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        log_dir / LOG_FILE,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    """Get the logger instance.

    Args:
        name (str, optional): Logger name. Defaults to None.

    Returns:
        logging.Logger: Logger instance.
    """

    return logging.getLogger(name)

# from logging import getLogger
#
# # https://youtu.be/USNrWe_3WJg?si=FYctGEXxVoiyYBva&t=517
# # https://www.youtube.com/live/LKYOtXNqiBc?si=Tic9KshrkOzAS13f&t=350
#
#
# # Load config
# if os.path.isfile(LOG_CONFIG):
#     import json
#     from logging.config import dictConfig
#
#     with open(LOG_CONFIG) as file:
#         config = json.load(file)
#     dictConfig(config)
# else:
#     import sys
#     from logging import basicConfig, FileHandler, StreamHandler, WARNING, INFO
#
#     log_format = "[%(asctime)s] %(levelname)s: %(name)s: %(message)s"
#
#     stream_handler = StreamHandler(stream=sys.stdout)
#     stream_handler.setLevel(INFO)
#
#     file_handler = FileHandler(filename=LOG_FILE, encoding="utf-8")
#     file_handler.setLevel(WARNING)
#
#     basicConfig(format=log_format, handlers=[stream_handler, file_handler])
#
#     stream_handler.close()
#     file_handler.close()
#
# _logger = getLogger(__name__)
