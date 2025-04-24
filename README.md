# MetaExpert

[![PyPI version](https://badge.fury.io/py/metaexpert.svg)](https://badge.fury.io/py/metaexpert)
<!--[![Build Status](https://travis-ci.com/teratron/metaexpert.svg?branch=master)](https://travis-ci.com/teratron/metaexpert)-->
[![Documentation Status](https://readthedocs.org/projects/metaexpert/badge/?version=latest)](https://metaexpert.readthedocs.io/en/latest/?badge=latest)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## Description

## Visuals

## Installation

```shell
pip install metaexpert
```

```shell
poetry add metaexpert
```

```shell
uv add metaexpert
```

If you have already added **MetaExpert**, you can update to the latest version by using:

```shell
pip install --upgrade metaexpert
```

```shell
poetry update metaexpert
```

```shell
uv sync --upgrade-package metaexpert
```

## Usage

```python

```

usage:

	main.py [-h] [--type {spot,futures,options,margin}] [--contract {usd_m,coin_m}] [--mode {backtest,paper,live}] [--exchange {binance,bybit}] [--pair PAIR] [--timeframe TIMEFRAME] [--size SIZE]
						 [--stop-loss STOP_LOSS] [--take-profit TAKE_PROFIT] [--trailing-stop TRAILING_STOP] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]

	main.py [-h] [--type={spot,futures,options,margin}] [--contract={usd_m,coin_m}] [--mode={backtest,paper,live}] [--exchange={binance,bybit}] [--pair=PAIR] [--timeframe=TIMEFRAME] [--size=SIZE]
						 [--stop-loss=STOP_LOSS] [--take-profit=TAKE_PROFIT] [--trailing-stop=TRAILING_STOP] [--log-level={DEBUG,INFO,WARNING,ERROR,CRITICAL}]

Expert Trading Bot

options:

  -h, --help            show this help message and exit
  
  --type {spot,futures,options,margin}
  --type={spot,futures,options,margin}
                        Trading type: spot, futures, options, or margin
  
  --contract {usd_m,coin_m}
  --contract={usd_m,coin_m}
                        Contract type for futures trading: USDⓈ-M (usd_m) or COIN-M (coin_m)
  
  --mode {backtest,paper,live}
  --mode={backtest,paper,live}
                        Trading mode: backtest, paper, or live
  
  --exchange {binance,bybit}
  --exchange={binance,bybit}
                        Stock exchange to use (e.g., binance, bybit)
  
  --pair PAIR, --symbol PAIR
  --pair=PAIR, --symbol=PAIR
                        Trading pair (e.g., BTCUSDT)
  
  --timeframe TIMEFRAME, --tf TIMEFRAME
  --timeframe=TIMEFRAME, --tf=TIMEFRAME
                        Trading timeframe
  
  --size SIZE, --lots SIZE
  --size=SIZE, --lots=SIZE
                        Maximum position size as a fraction of available balance
  
  --stop-loss STOP_LOSS, --sl STOP_LOSS
  --stop-loss=STOP_LOSS, --sl=STOP_LOSS
                        Stop loss percentage
  
  --take-profit TAKE_PROFIT, --tp TAKE_PROFIT
  --take-profit=TAKE_PROFIT, --tp=TAKE_PROFIT
                        Take profit percentage
  
  --trailing-stop TRAILING_STOP, --ts TRAILING_STOP
  --trailing-stop=TRAILING_STOP, --ts=TRAILING_STOP
                        Trailing stop percentage
  
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
  --log-level={DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Logging level

## Documentation

## Examples

You can find examples in the [example's directory](examples):

- [EMA Expert](examples/exapert_ema.py)
-
-

## Support

## Roadmap

## Contributing

## Authors and acknowledgment

## License

[MIT License](LICENSE).

## Project status

_Project at the initial stage._

See the latest [commits](https://github.com/teratron/metaexpert/commits/master).

---
