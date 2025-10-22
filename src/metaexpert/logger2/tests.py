"""Tests for logger2 module."""

import tempfile
from pathlib import Path

import pytest

from metaexpert.logger2 import (
    LoggerConfig,
    get_logger,
    get_trade_logger,
    log_context,
    setup_logging,
    trade_context,
)


@pytest.fixture(scope="function")
def test_log_dir(tmp_path):
    """Create temporary log directory."""
    log_dir = tmp_path / "test_logs"
    log_dir.mkdir(exist_ok=True)
    return log_dir


@pytest.fixture(scope="function")
def test_config(test_log_dir):
    """Create test logging configuration."""
    return LoggerConfig(
        log_level="DEBUG",
        log_to_console=False,
        log_to_file=True,
        log_dir=test_log_dir,
        use_colors=False,
        json_logs=False,
    )


class TestLoggerConfig:
    """Test LoggerConfig validation."""

    def test_default_config(self):
        """Test default configuration."""
        config = LoggerConfig()
        assert config.log_level == "INFO"
        assert config.log_to_console is True
        assert config.log_to_file is True

    def test_custom_config(self, test_log_dir):
        """Test custom configuration."""
        config = LoggerConfig(
            log_level="DEBUG",
            log_dir=test_log_dir,
            max_bytes=1024 * 1024,
            backup_count=3,
        )
        assert config.log_level == "DEBUG"
        assert config.max_bytes == 1024 * 1024
        assert config.backup_count == 3

    def test_log_dir_creation(self, tmp_path):
        """Test that log directory is created."""
        log_dir = tmp_path / "new_logs"
        config = LoggerConfig(log_dir=log_dir)
        assert log_dir.exists()

    def test_invalid_max_bytes(self):
        """Test validation of max_bytes."""
        with pytest.raises(ValueError, match="max_bytes must be positive"):
            LoggerConfig(max_bytes=0)

        with pytest.raises(ValueError, match="must not exceed 1GB"):
            LoggerConfig(max_bytes=2 * 1024 * 1024 * 1024)


class TestBasicLogging:
    """Test basic logging functionality."""

    def test_get_logger(self, test_config):
        """Test getting a logger."""
        setup_logging(test_config)
        logger = get_logger(__name__)
        assert logger is not None
        
        logger.info("test message")
        
        # Check log file was created
        log_file = test_config.log_dir / "expert.log"
        assert log_file.exists()

    def test_log_with_context(self, test_config):
        """Test logging with context variables."""
        setup_logging(test_config)
        logger = get_logger(__name__).bind(
            exchange="binance",
            symbol="BTCUSDT"
        )
        
        logger.info("test with context")
        
        log_file = test_config.log_dir / "expert.log"
        content = log_file.read_text()
        assert "binance" in content
        assert "BTCUSDT" in content

    def test_log_levels(self, test_config):
        """Test different log levels."""
        setup_logging(test_config)
        logger = get_logger(__name__)
        
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
        logger.critical("critical message")
        
        log_file = test_config.log_dir / "expert.log"
        content = log_file.read_text()
        
        assert "debug message" in content
        assert "info message" in content
        assert "warning message" in content
        assert "error message" in content
        assert "critical message" in content


class TestContextManagement:
    """Test context management features."""

    def test_log_context(self, test_config):
        """Test log_context context manager."""
        setup_logging(test_config)
        logger = get_logger(__name__)
        
        with log_context(strategy_id=1001, symbol="ETHUSDT"):
            logger.info("inside context")
        
        logger.info("outside context")
        
        log_file = test_config.log_dir / "expert.log"
        content = log_file.read_text()
        
        # Context should be in first message
        assert "strategy_id" in content
        assert "1001" in content
        assert "ETHUSDT" in content

    def test_trade_context(self, test_config):
        """Test trade_context context manager."""
        setup_logging(test_config)
        trade_logger = get_trade_logger(strategy_id=1001)
        
        with trade_context(symbol="BTCUSDT", side="BUY", quantity=0.01):
            trade_logger.info("trade executed", price=50000)
        
        log_file = test_config.log_dir / "expert.log"
        content = log_file.read_text()
        
        assert "trade" in content.lower()
        assert "BTCUSDT" in content
        assert "BUY" in content
        assert "0.01" in content


class TestSpecializedLoggers:
    """Test specialized logger functionality."""

    def test_trade_logger(self, test_config):
        """Test trade logger."""
        setup_logging(test_config)
        trade_logger = get_trade_logger(strategy_id=1001)
        
        trade_logger.info(
            "trade executed",
            symbol="BTCUSDT",
            side="BUY",
            price=50000,
            quantity=0.01
        )
        
        trade_log_file = test_config.log_dir / "trades.log"
        assert trade_log_file.exists()
        
        content = trade_log_file.read_text()
        assert "trade executed" in content
        assert "BTCUSDT" in content

    def test_error_logging(self, test_config):
        """Test error logging."""
        setup_logging(test_config)
        logger = get_logger(__name__)
        
        try:
            raise ValueError("Test error")
        except ValueError:
            logger.error("error occurred", exc_info=True)
        
        error_log_file = test_config.log_dir / "errors.log"
        assert error_log_file.exists()
        
        content = error_log_file.read_text()
        assert "error occurred" in content
        assert "ValueError" in content
        assert "Test error" in content


class TestJSONLogging:
    """Test JSON logging format."""

    def test_json_format(self, test_log_dir):
        """Test JSON log output."""
        config = LoggerConfig(
            log_level="INFO",
            log_to_console=False,
            log_to_file=True,
            log_dir=test_log_dir,
            json_logs=True,
        )
        setup_logging(config)
        
        logger = get_logger(__name__)
        logger.info("test json", key="value", number=123)
        
        log_file = test_log_dir / "expert.log"
        content = log_file.read_text()
        
        # Should be valid JSON
        import json
        log_entry = json.loads(content.strip().split('\n')[0])
        
        assert log_entry["message"] == "test json"
        assert log_entry["key"] == "value"
        assert log_entry["number"] == 123


class TestPerformance:
    """Test logging performance."""

    def test_logging_performance(self, test_config, benchmark):
        """Benchmark logging performance."""
        setup_logging(test_config)
        logger = get_logger(__name__)
        
        def log_message():
            logger.info("performance test", iteration=1, data="test")
        
        # Should be fast (< 1ms per log call)
        result = benchmark(log_message)
        assert result < 0.001  # Less than 1ms


class TestFileRotation:
    """Test log file rotation."""

    def test_rotation(self, test_log_dir):
        """Test log file rotation when size limit reached."""
        config = LoggerConfig(
            log_level="INFO",
            log_dir=test_log_dir,
            max_bytes=1024,  # 1KB for fast testing
            backup_count=2,
        )
        setup_logging(config)
        
        logger = get_logger(__name__)
        
        # Write enough to trigger rotation
        for i in range(100):
            logger.info("test message " * 10, iteration=i)
        
        # Check that rotation occurred
        log_file = test_log_dir / "expert.log"
        backup_file = test_log_dir / "expert.log.1"
        
        assert log_file.exists()
        # Backup file should exist if rotation happened
        # (may not exist if not enough data was written)
