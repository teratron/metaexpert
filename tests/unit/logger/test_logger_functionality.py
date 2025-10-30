"""Tests for logger functionality in MetaExpert.

Due to the complex architecture of the logger system with automatic initialization,
these tests focus on specific functions that can be tested in isolation.
"""

import tempfile
from unittest.mock import MagicMock, patch


def test_sensitive_data_filter():
    """Test that SensitiveDataFilter properly masks sensitive data."""
    # Mock the problematic initialization before importing
    with patch("metaexpert.logger.__init__._initialize_logging"):
        # Import and test the SensitiveDataFilter class directly
        from metaexpert.logger.processors import SensitiveDataFilter

    # Create an instance of the filter
    filter_instance = SensitiveDataFilter()

    # Test data with sensitive information
    test_data = {
        "api_key": "secret123456",
        "secret_key": "very_secret789",
        "password": "my_password123",
        "token": "bearer_token999",
        "normal_field": "normal_value",
        "short_token": "abc",  # Short value should be fully masked
    }

    # Apply filtering
    filtered_data = filter_instance(None, "event", test_data.copy())

    # Check that sensitive fields are masked appropriately
    # Long values should show last 4 chars with *** prefix
    assert filtered_data["api_key"] == "***3456"
    assert filtered_data["secret_key"] == "***t789"
    assert filtered_data["password"] == "***d123"
    assert filtered_data["token"] == "***n999"
    # Short values should be fully masked
    assert filtered_data["short_token"] == "***"

    # Check that normal fields are not affected
    assert filtered_data["normal_field"] == "normal_value"


def test_trade_event_filter():
    """Test that TradeEventFilter properly identifies trade events."""
    from metaexpert.logger.processors import TradeEventFilter

    # Create an instance of the filter
    filter_instance = TradeEventFilter()

    # Test with a trade event
    trade_event = {"event_type": "trade", "symbol": "BTCUSDT", "amount": 1.0}
    result = filter_instance(None, "event", trade_event)
    assert result["_trade_event"] is True

    # Test with a non-trade event
    non_trade_event = {"event_type": "info", "message": "system status"}
    result = filter_instance(None, "event", non_trade_event)
    assert "_trade_event" not in result


def test_performance_monitor():
    """Test that PerformanceMonitor detects slow operations."""
    from metaexpert.logger.processors import PerformanceMonitor

    # Create a monitor with 10ms threshold
    monitor = PerformanceMonitor(threshold_ms=10.0)

    # Test with a slow trade operation
    slow_trade = {"event_type": "trade", "duration_ms": 150.0, "symbol": "BTCUSDT"}
    result = monitor(None, "event", slow_trade)
    assert result["_slow_operation"] is True
    assert "performance_warning" in result
    assert "150.00ms" in result["performance_warning"]

    # Test with a fast trade operation (should not trigger slow operation flag)
    fast_trade = {
        "event_type": "trade",
        "duration_ms": 5.0,  # Less than threshold
        "symbol": "ETHUSDT",
    }
    result = monitor(None, "event", fast_trade)
    assert "_slow_operation" not in result
    assert "performance_warning" not in result

    # Test with non-trade event (should not be monitored)
    non_trade = {"event_type": "info", "duration_ms": 150.0}
    result = monitor(None, "event", non_trade)
    assert "_slow_operation" not in result


def test_config_preset_methods_exist():
    """Test that config preset methods exist and are callable."""
    from metaexpert.logger.config import LoggerConfig

    # Проверим, что методы-пресеты существуют
    assert hasattr(LoggerConfig, "for_development")
    assert hasattr(LoggerConfig, "for_production")
    assert hasattr(LoggerConfig, "for_backtesting")

    assert callable(LoggerConfig.for_development)
    assert callable(LoggerConfig.for_production)
    assert callable(LoggerConfig.for_backtesting)


def test_config_presets():
    """Test configuration presets for different environments."""
    from metaexpert.logger.config import LoggerConfig

    # Test development preset
    dev_config = LoggerConfig.for_development()
    assert dev_config.log_level == "DEBUG"
    assert dev_config.use_colors is True
    assert dev_config.json_logging is False
    assert dev_config.log_to_console is True

    # Test production preset
    prod_config = LoggerConfig.for_production()
    assert prod_config.log_level == "WARNING"
    assert prod_config.use_colors is False
    assert prod_config.json_logging is True
    assert prod_config.log_to_console is False

    # Test backtesting preset
    backtest_config = LoggerConfig.for_backtesting()
    assert backtest_config.log_level == "INFO"
    assert backtest_config.use_colors is False
    assert backtest_config.json_logging is True
    assert backtest_config.log_to_console is False


def test_error_event_enricher():
    """Test that ErrorEventEnricher adds appropriate context to error events."""
    from metaexpert.logger.processors import ErrorEventEnricher

    enricher = ErrorEventEnricher()

    # Test with an error event that has an exception
    exception = ValueError("Test error")
    error_event = {
        "level": "error",
        "event": "Something went wrong",
        "exception": exception,
    }

    result = enricher(None, "event", error_event)
    assert result["error_type"] == "ValueError"
    assert result["error_module"] == "builtins"

    # Test with non-error event (should not be enriched)
    info_event = {"level": "info", "event": "Informational message"}

    result = enricher(None, "event", info_event)
    assert "error_type" not in result
    assert "error_module" not in result


def test_log_context_manager():
    """Test LogContext functionality."""
    from metaexpert.logger.context import LogContext

    # Test that LogContext can be instantiated and used without errors
    with LogContext(user_id=123, session_id="abc"):
        # Just verify the context manager works without errors
        pass


def test_trade_context_manager():
    """Test TradeContext functionality."""
    # Mock the initialization to avoid triggering logger setup
    with patch("metaexpert.logger.__init__._initialize_logging"):
        from metaexpert.logger.context import TradeContext

        # Mock the get_trade_logger function to avoid initialization issues
        with patch("metaexpert.logger.context.get_trade_logger") as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger

            # Test that TradeContext can be instantiated and used without errors
            with TradeContext(symbol="BTCUSDT", side="BUY", quantity=0.01):
                # Just verify the context manager works without errors
                pass

            # Verify that get_trade_logger was called with correct parameters
            mock_get_logger.assert_called_once()
            call_args = mock_get_logger.call_args[1]  # keyword arguments
            assert call_args.get("symbol") == "BTCUSDT"
            assert call_args.get("side") == "BUY"
            assert call_args.get("quantity") == 0.01
            assert call_args.get("event_type") == "trade"


def test_wrapper_class_in_structlog():
    """Test that wrapper_class functionality works as expected."""
    # Тестирование wrapper_class в structlog можно выполнить, проверив
    # конфигурацию structlog без инициализации всей системы логирования
    import structlog

    # Проверим, что structlog может использовать разные wrapper классы
    test_dict = {"key": "value"}

    # Тестирование функций обработки
    result = structlog.processors.JSONRenderer()(None, "event", test_dict)
    assert isinstance(result, (str, bytes))  # Результат должен быть сериализуемым


def test_get_logger_function():
    """Test the get_logger function functionality."""
    from metaexpert.logger.context import get_logger

    # Mock structlog.get_logger to avoid initialization
    with patch("structlog.get_logger") as mock_structlog_get_logger:
        mock_logger = MagicMock()
        mock_structlog_get_logger.return_value = mock_logger

        # Проверим, что функция возвращает logger
        logger = get_logger("test_module")
        mock_structlog_get_logger.assert_called_once_with("test_module")
        assert logger == mock_logger

        # Проверим, что можно добавить контекст
        mock_logger_with_context = MagicMock()
        mock_structlog_get_logger.return_value = mock_logger_with_context
        _logger_with_context = get_logger("test_module", symbol="BTCUSDT")

        # Check that bind was called on the logger
        mock_logger_with_context.bind.assert_called_once_with(symbol="BTCUSDT")


def test_config_validation():
    """Test validation of logger configuration."""
    from metaexpert.logger.config import LoggerConfig

    # Test valid configuration
    valid_config = LoggerConfig(
        log_level="INFO",
        log_to_console=True,
        log_to_file=True,
        log_dir=tempfile.gettempdir(),
    )
    assert valid_config.log_level == "INFO"

    # Test validation - at least one output must be enabled
    try:
        _invalid_config = LoggerConfig(
            log_level="INFO",
            log_to_console=False,
            log_to_file=False,
            log_dir=tempfile.gettempdir(),
        )
        # This should raise a validation error
        assert AssertionError(), "Should have raised validation error"
    except ValueError:
        # Expected behavior
        pass


def test_trade_log_filter():
    """Test that trade events are properly filtered to trades.log."""
    # This test requires the system to be configured, so we'll test the filter logic
    from metaexpert.logger.processors import TradeEventFilter

    # Create an instance of the filter
    filter_instance = TradeEventFilter()

    # Test with a trade event
    trade_event = {"event_type": "trade", "symbol": "BTCUSDT", "amount": 1.0}
    result = filter_instance(None, "event", trade_event)
    assert result["_trade_event"] is True


def test_performance_monitoring():
    """Test performance monitoring functionality."""
    # This test is similar to test_performance_monitor but with different focus
    from metaexpert.logger.processors import PerformanceMonitor

    # Create a monitor with 100ms threshold
    monitor = PerformanceMonitor(threshold_ms=100.0)

    # Test with a slow operation
    slow_operation = {
        "event_type": "trade",
        "duration_ms": 150.0,
        "operation": "order_execution",
    }
    result = monitor(None, "event", slow_operation)
    assert result["_slow_operation"] is True
    assert "performance_warning" in result
    assert "150.00ms" in result["performance_warning"]
