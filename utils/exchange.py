
from time import sleep
from utils.lbank import get_trading_depth as depth, orderBatch as orders
from utils.bitmartdata import get_trading_depth as depth2, orderBatch as orders2
from utils.indodax import get_trading_depth as depth3, orderBatch as orders3
from utils.mexc import get_trading_depth as depth4, orderBatch as orders4
from utils.flybit import get_trading_depth as depth5, orderBatch as orders5
from utils.getio import get_trading_depth as depth6, orderBatch as orders6


def get_trading_depth(pair, exchange):
    sleep(0.3)
    if exchange == "1":
        return depth(pair=pair)
    if exchange == "2":
        return depth2(pair=pair)
    if exchange == "3":
        return depth3(pair=pair)
    if exchange == "4":
        return depth4(pair=pair)
    if exchange == "5":
        return depth5(pair=pair)
    if exchange == "6":
        return depth6(pair=pair)


def exchangeOrder(data, api_key, private_key, acton, exchange, priority, memo, self):
    if exchange == "1":
        return orders(data, api_key, private_key, acton, priority, self)
    if exchange == "2":
        return orders2(data, api_key, private_key, acton, priority, memo, self)
    if exchange == "3":
        return orders3(data, api_key, private_key, acton, priority, self)
    if exchange == "4":
        return orders4(data, api_key, private_key, acton, priority, self)
    if exchange == "5":
        return orders5(data, api_key, private_key, acton, priority, self)
    if exchange == "6":
        return orders6(data, api_key, private_key, acton, priority, self)