Из последних сделанных изменений этого кода:
```python
'''Это заглушка/шаблон клиентского скрипта'''
import os
from dotenv import load_dotenv
from metaexpert import MetaExpert  # предполагаемая внешняя библиотека

# Load environment variables from .env file
load_dotenv()

# Initialize MetaExpert with enhanced configuration
expert = MetaExpert(
    # --- Обязательные параметры ---
    exchange="binance",             # Биржа: 'binance', 'bybit', 'okx', 'bitget', 'kucoin'
    
    # --- Ключи API (обязательны для live-режима) ---
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET"),
    api_passphrase=os.getenv("API_PASSPHRASE"),  # Только для OKX, KuCoin
    
    # --- Параметры подключения ---
	subaccount=os.getenv("SUBACCOUNT"),  # Для Bybit multi-accounts, optional
    base_url=os.getenv("BASE_URL"),      # Опционально, для кастомных URL
    testnet=False,                       # True для testnet окружения
	proxy={
        "http": os.getenv("PROXY_HTTP"),
        "https": os.getenv("PROXY_HTTPS")
    },

    # --- Режим торговли и рынка ---
    market_type="futures",          # 'spot', 'futures', 'options' (проверка 'options')
    contract_type="linear",         # Только если market_type=futures: 'linear' (USDT-M) | 'inverse' (COIN-M), на Bybit/OKX называется "USDT-M" / "COIN-M". Можно сделать алиасы внутри движка
    settlement_currency="USDT",     # Валюта расчета: 'USDT' (linear), 'BTC'/'ETH' (inverse)
    margin_mode="isolated",         # 'isolated' или 'cross' (только для futures/margin)
    position_mode="hedge",          # 'hedge' (двусторонние) или 'oneway' (односторонние позиции, проверка) (Binance futures)

	# --- Настройки риск-менеджмента ---
    max_drawdown_pct=0.2,           # Максимальная просадка от пикового эквити (0.2 = 20%)
    daily_loss_limit=1000,          # Дневной лимит убытков в USDT, в settlement_currency (например, USDT для linear, BTC для inverse)

    # --- Настройки логирования ---
    log_level="INFO",               # 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    log_file="expert.log",          # Файл для логов
	trade_log_file="trades.log",    # Файл для логов торговых операций
	error_log_file="errors.log",    # Файл для логов для ошибок (особенно если log_level=INFO, а ошибки хочется отдельно).
    log_to_console=True,            # Вывод логов в консоль
    
    # --- Дополнительные параметры ---
	rate_limit=1200,                # Ограничение RPS, макс. запросов в минуту (зависит от биржи)
    enable_metrics=True,            # Сбор метрик производительности
	persist_state=True,             # Сохраняет: открытые ордера, позиции, счетчики. Осторожно при смене стратегии!
    state_file="expert_state.json"  # Файл для сохранения состояния
)

@expert.on_init(
    # --- Метаданные стратегии ---
    strategy_name="EMA Cross",      # Название эксперта
    strategy_id=12345,              # ID эксперта
    comment="ema_expert",           # Комментарий к ордерам (32 символов для Binance, до 36 для Bybit)
	
    # --- Основные параметры торговли ---
    symbols=["BTCUSDT", "ETHUSDT"], # Список символа/символов (str | list[str])
    timeframe="1h",                 # Таймфрейм: '1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'
    lookback_bars=100,              # Количество баров истории для анализа (зависит от timeframe)
	warmup_bars=50,                 # Пропустить первые N баров для инициализации индикаторов
	warmup_mode="skip",             # или "no_trade" — не открывать сделки, но генерировать on_bar
    
    # --- Настройки риск-менеджмента ---
    leverage=10,                    # Плечо по умолчанию (1-125 для BTC, зависит от биржи, для маржинальной торговли, ignored для spot)
	
    # --- Параметры управления капиталом ---
    initial_capital=10000,          # Начальный капитал в settlement_currency
    size_type="risk_based",         # 'fixed_base', 'fixed_quote', 'percent_equity', 'risk_based'
	size_value=1.5,                 # Размер позиции, значение зависит от size_type: fixed_base: 0.01 BTC | fixed_quote: 1000 USDT | percent_equity: 10.0% | risk_based: 1.5%
	max_position_size_quote=50000.0,# Макс. размер позиции в валюте котировки (USDT)

    # --- Параметры входа в рынок ---
    stop_loss_pct=2.0,              # Stop-Loss в % от цены входа
    take_profit_pct=4.0,            # Take-Profit в % от цены входа
	max_spread_pct=0.1,             # Максимальный спред для входа в %
    
    # --- Управление позициями (портфелем) ---
    max_open_positions=3,           # Макс. количество открытых позиций
    max_positions_per_symbol=1,     # Макс. позиций на один символ
    
	# --- Фильтры и условия входа ---
    trade_hours=[9, 10, 11, 15, 16],# Торговать только в эти часы UTC в UTC, по умолчанию None - круглосуточно
    allowed_days=[1,2,3,4,5],       # Дни недели (1=пн, 7=вс), по умолчанию None - каждый день
    min_volume=1000000,             # Мин. объем в settlement_currency
    volatility_filter=True,         # Фильтр по волатильности
    trend_filter=True,              # Фильтр по тренду
)
def init() -> None:
    """Initialization function called once when the expert advisor starts."""
    pass

@expert.on_deinit
def deinit(reason: str) -> None:
    """Deinitialization function called when the expert advisor stops.
    
    Args:
        reason: The reason for deinitialization
    """
    print(f"The reason for deinitialization: {reason}")

@expert.on_tick
def tick(rates) -> None:
    """Called on each tick (price update) from the market.

    Args:
        rates: Current market rates information
    """
    pass

@expert.on_bar(
    pyramid_levels=3,               # Уровни пирамидинга (наращивания)
    pyramid_factor=0.5,             # Множитель размера для пирамидинга
)
def bar(rates) -> None:
    """Called when a new 1-hour bar (candle) is formed.
    This is where the main EMA trading logic is implemented.

    Args:
        rates: Bar data containing OHLCV information
    """
    pass

@expert.on_timer(
	interval=1                     # seconds, type float
)
def timer() -> None:
    """Called every 1 second to perform time-based operations.
    Useful for operations that need to run periodically regardless of market activity.
    """
    pass

@expert.on_order
def order(order) -> None:
    """Called when order status changes.
    
    Args:
        order: Order object with status update
    """
    print(f"Order update: {order.symbol} {order.side} {order.status}")

@expert.on_position(
	trailing_stop_pct=1.0,          # Trailing Stop в %
	trailing_activation_pct=2.0,    # Активация trailing stop после прибыли в %
    breakeven_pct=1.5,              # Перевод в безубыток при прибыли в %
)
def position(pos) -> None:
    """Called when position status changes.
    
    Args:
        position: Position object with current state
    """
	print(f"Position update: {pos.symbol} PnL: {pos.pnl:.2f}")

@expert.on_transaction
def transaction(request, result) -> None:
    """Called when a transaction is completed.

    Args:
        request: The transaction request details
        result: The result of the transaction
    """
    pass

@expert.on_book
def book(orderbook) -> None:
    """Функция генерируется только при изненении состояния стакана цен.
    """
	# orderbook.symbol, orderbook.bids, orderbook.asks
    pass

@expert.on_error
def error(err) -> None:
	# Обработка ошибок биржи / сети
	# Можно добавить логику: переподключение, алерт в телеграм и т.д.
	print(f"Error: {err}")

@expert.on_account
def account(acc) -> None:
	# Обновления баланса
	print(f"Account balance: {acc.balance:.6f} {acc.currency}")

def main() -> None:
    """Main entry point for the expert advisor.
    
    Starts the trading bot with the configured settings.
    """
    expert.run(
	    # --- Режим работы эксперта ---
		mode="paper",                   # 'paper' (симуляция) или 'live' (реальная торговля)
		
		# --- Бэктестинг ---
        backtest_start="2024-01-01",    # Начало периода бэктеста
		backtest_end="2025-08-31",      # Конец периода бэктеста
    )

if __name__ == "__main__":
    main()
```
нужно сделать шаблон файла, который будет копироваться каждый раз, когда пользователь библиотекой MetaExpert будет вызывать команду: `new` или `create`.
Основные требования все события/хуки заглушки, везде, где нужно, комментарии для разъяснения, докстринги.
