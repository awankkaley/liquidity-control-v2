
from utils.lbank import get_trading_depth as depth, orderBatch as orders

def get_trading_depth(pair,exchange):
    if exchange == "1":
        return depth(pair=pair)

def orderBatch(data, api_key, private_key, acton, exchange,priority):
    if exchange == "1":
        return orders(data, api_key, private_key, acton,priority)