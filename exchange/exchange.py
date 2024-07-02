from time import sleep
from exchange.lbank import get_trading_depth as depth, orderBatch as orders
from exchange.bitmartdata import get_trading_depth as depth2, orderBatch as orders2
from exchange.indodax import (
    get_trading_depth as depth3,
    order as orders3,
    balance as balance3,
    price as price3,
    cancel as cancel3,
)  # "btc_idr"
from exchange.mexc import get_trading_depth as depth4, orderBatch as orders4
from exchange.flybit import get_trading_depth as depth5, orderBatch as orders5
from exchange.getio import get_trading_depth as depth6, orderBatch as orders6
from exchange.gopax import (
    get_trading_depth as depth7,
    order as orders7,
    balance as balance7,
    price as price7,
    cancel as cancel7,
)  # "BTC-KRW"


def get_trading_depth(pair, exchange):
    sleep(0.3)
    if exchange == "3":
        return depth3(pair=pair)
    if exchange == "7":
        return depth7(pair=pair)


def exchangeOrder(pair, side, price, size, api_key, secret_key, exchange, memo=None):
    if exchange == "3":
        return orders3(pair, side, price, size, api_key, secret_key)
    if exchange == "7":
        return orders7(pair, side, price, size, api_key, secret_key)


def balance(pair, api_key, private_key, exchange):
    if exchange == "3":
        return balance3(pair, api_key, private_key)
    if exchange == "7":
        return balance7(pair, api_key, private_key)


def price(pair, exchange):
    if exchange == "3":
        return price3(pair)
    if exchange == "7":
        return price7(pair)


def cancel(pair, order_id, type, api_key, private_key, exchange):
    if exchange == "3":
        return cancel3(pair, order_id, type, api_key, private_key)
    if exchange == "7":
        return cancel7(pair, order_id, type, api_key, private_key)