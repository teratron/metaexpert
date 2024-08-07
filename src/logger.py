from logging import getLogger, basicConfig, FileHandler, StreamHandler, DEBUG, ERROR, WARNING

# Logging
# DEBUG < INFO < WARNING < ERROR < CRITICAL
logger = getLogger(__name__)
format_log = "%(asctime)s %(levelname)s: %(name)s: %(message)s"

# File
file_handler = FileHandler("data.log", encoding="utf-8")
file_handler.setLevel(WARNING)

# Stream
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)

basicConfig(level=DEBUG, format=format_log, handlers=[file_handler, stream_handler])

logger.info("start app")
logger.debug("test debug")
logger.warning("test warning")
logger.error("test error")
logger.critical("test critical")
logger.info("finish app")

file_handler.close()
stream_handler.close()
