"""

"""

from logging import getLogger, basicConfig, FileHandler, StreamHandler, DEBUG, ERROR

# Logging
# DEBUG < INFO < WARNING < ERROR < CRITICAL
logger = getLogger()
format_log = "%(asctime)s %(levelname)s: %(name)s: %(message)s"
file_handler = FileHandler("data.log")
file_handler.setLevel(ERROR)
console_handler = StreamHandler()
console_handler.setLevel(DEBUG)
basicConfig(level=DEBUG, format=format_log, handlers=[file_handler, console_handler])

if __name__ == "__main__":
    logger.info("start app")
    logger.debug("test debug")
    logger.warning("test warning")
    logger.error("test error")
    logger.critical("test critical")
    logger.info("finish app")
