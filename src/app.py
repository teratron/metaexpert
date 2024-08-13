"""Expert Application
"""
import json
import pprint

from _logger import getLogger
from flask import Flask, render_template, request, flash, redirect, jsonify
from binance.spot import Spot

_logger = getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def index():
    spot = Spot()
    infos = spot.exchange_info()
    symbols = infos["symbols"]

    props = {
        "title": "Home",
        "infos": infos,
        "symbols": symbols
    }
    return render_template("view.home.tmpl", **props)


@app.route("/about")
def about():
    title = "About"
    return render_template("view.about.tmpl", title=title)


@app.route("/hello")
def hello():
    """{
    timezone: "UTC",
    serverTime: 1633012903441,
    rateLimits: [
            {
              "interval": "MINUTE",
              "intervalNum": 1,
              "limit": 6000,
              "rateLimitType": "REQUEST_WEIGHT"
            },
            ...
        ]
    exchangeFilters: [],
    symbols: [
            {
              "allowTrailingStop": true,
              "allowedSelfTradePreventionModes": [
                "EXPIRE_TAKER",
                "EXPIRE_MAKER",
                "EXPIRE_BOTH"
              ],
              "baseAsset": "ETH",
              "baseAssetPrecision": 8,
              "baseCommissionPrecision": 8,
              "cancelReplaceAllowed": true,
              "defaultSelfTradePreventionMode": "EXPIRE_MAKER",
              "permissions": [],
              "quoteAsset": "BTC",
              "quoteAssetPrecision": 8,
              "quoteCommissionPrecision": 8,
              "quoteOrderQtyMarketAllowed": true,
              "quotePrecision": 8,
              "status": "TRADING",
              "symbol": "ETHBTC",
              "filters": [
                {
                  "filterType": "PRICE_FILTER",
                  "maxPrice": "922327.00000000",
                  "minPrice": "0.00001000",
                  "tickSize": "0.00001000"
                },
                {
                  "filterType": "LOT_SIZE",
                  "maxQty": "100000.00000000",
                  "minQty": "0.00010000",
                  "stepSize": "0.00010000"
                },
                {
                  "filterType": "ICEBERG_PARTS",
                  "limit": 10
                },
                {
                  "filterType": "MARKET_LOT_SIZE",
                  "maxQty": "2077.27362125",
                  "minQty": "0.00000000",
                  "stepSize": "0.00000000"
                },
                {
                  "filterType": "TRAILING_DELTA",
                  "maxTrailingAboveDelta": 2000,
                  "maxTrailingBelowDelta": 2000,
                  "minTrailingAboveDelta": 10,
                  "minTrailingBelowDelta": 10
                },
                {
                  "askMultiplierDown": "0.2",
                  "askMultiplierUp": "5",
                  "avgPriceMins": 5,
                  "bidMultiplierDown": "0.2",
                  "bidMultiplierUp": "5",
                  "filterType": "PERCENT_PRICE_BY_SIDE"
                },
                {
                  "applyMaxToMarket": false,
                  "applyMinToMarket": true,
                  "avgPriceMins": 5,
                  "filterType": "NOTIONAL",
                  "maxNotional": "9000000.00000000",
                  "minNotional": "0.00010000"
                },
                {
                  "filterType": "MAX_NUM_ORDERS",
                  "maxNumOrders": 200
                },
                {
                  "filterType": "MAX_NUM_ALGO_ORDERS",
                  "maxNumAlgoOrders": 5
                }
              ],
              "icebergAllowed": true,
              "isMarginTradingAllowed": true,
              "isSpotTradingAllowed": true,
              "ocoAllowed": true,
              "orderTypes": [
                "LIMIT",
                "LIMIT_MAKER",
                "MARKET",
                "STOP_LOSS",
                "STOP_LOSS_LIMIT",
                "TAKE_PROFIT",
                "TAKE_PROFIT_LIMIT"
              ],
              "otoAllowed": true,
              "permissionSets": [
                [
                  "SPOT",
                  "MARGIN",
                  "TRD_GRP_004",
                  "TRD_GRP_005",
                  "TRD_GRP_006",
                  ...
                  "TRD_GRP_054"
                ]
              ]
            },
            ...
        ]
    }
    """
    spot = Spot()
    infos = spot.exchange_info()

    return jsonify(infos)


@app.errorhandler(404)
def not_found(error):
    title = "404"
    return render_template('view.error.tmpl', title=title, error=error), 404


if __name__ == "__main__":
    _logger.info("start app")

    app.run(port=5001, debug=True)

    _logger.info("finish app")
