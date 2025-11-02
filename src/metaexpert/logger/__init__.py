"""MetaExpert logging system."""

import logging

#from metaexpert.config import LOG_LEVEL_TYPE
from metaexpert.logger.config import LoggerConfig


class MetaLogger(LoggerConfig):

    def create(
        self
        #log_name: str,
        # log_level: LOG_LEVEL_TYPE,
        # log_file: str,
        # log_trade_file: str,
        # log_error_file: str,
        # log_to_file: bool,
        # log_to_console: bool,
        # json_logging: bool,
    ) -> logging.Logger:
        """Create a new MetaLogger instance."""

        # Setup logging with the new config. This affects global state.
        #setup_logging(config)
        print(self.log_level)
        return logging.getLogger(self.log_name)


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name."""
    return logging.getLogger(name)
