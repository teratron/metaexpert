import logging
import os
import pytest
from metaexpert.logger import configure_logging, get_logger

def test_configure_logging_console(capsys):
    """Test that logging is configured to output to console."""
    config = {
        "default_level": "INFO",
        "handlers": {"console": {"type": "console"}},
    }
    configure_logging(config)

    logger = get_logger("test_console")
    logger.info("This is a console test.")

    captured = capsys.readouterr()
    assert "This is a console test." in captured.out

def test_configure_logging_file(tmp_path, monkeypatch):
    """Test that logging is configured to output to a file."""
    log_dir = tmp_path / "logs"
    log_file = log_dir / "test.log"

    config = {
        "default_level": "DEBUG",
        "handlers": {"file": {"type": "file", "filename": "test.log"}},
    }
    # Override the default LOG_DIRECTORY for this test
    from metaexpert.logger import config as logger_config
    monkeypatch.setattr(logger_config, 'LOG_DIRECTORY', str(log_dir))

    configure_logging(config)

    logger = get_logger("test_file")
    logger.debug("This is a file test.")

    # Close handlers to ensure logs are flushed
    logging.shutdown()

    assert log_file.exists()
    assert "This is a file test." in log_file.read_text()

def test_configure_logging_structured(capsys):
    """Test structured (JSON) logging configuration."""
    import json

    config = {
        "default_level": "WARNING",
        "structured_logging": True,
        "handlers": {"console": {"type": "console"}},
    }
    configure_logging(config)

    logger = get_logger("test_structured")
    logger.warning("This is a structured test.")

    captured = capsys.readouterr()
    log_json = json.loads(captured.out)

    assert log_json["level"] == "WARNING"
    assert log_json["message"] == "This is a structured test."
    assert log_json["logger"] == "test_structured"

def test_configure_logging_async(tmp_path, monkeypatch):
    """Test asynchronous logging configuration."""
    log_dir = tmp_path / "logs"
    log_file = log_dir / "test_async.log"

    config = {
        "default_level": "INFO",
        "async_logging": True,
        "handlers": {"file": {"type": "file", "filename": "test_async.log"}},
    }
    from metaexpert.logger import config as logger_config
    monkeypatch.setattr(logger_config, 'LOG_DIRECTORY', str(log_dir))

    configure_logging(config)

    logger = get_logger("test_async")
    logger.info("This is an async test.")

    # Shutdown logging and wait for async handler to flush
    logging.shutdown()

    assert log_file.exists()
    assert "This is an async test." in log_file.read_text()

def test_get_logger():
    """Test the get_logger function."""
    logger1 = get_logger("my_test_logger")
    logger2 = get_logger("my_test_logger")
    assert logger1 is logger2
    assert logger1.name == "my_test_logger"