import json
import threading
from utils.lbank import get_trading_depth, orderBatch
from utils.math_utils import random_float
import utils.const as const


def start(delay, min_price_difference, min_usdt, max_usdt, max_limit_price, min_limit_price):
    threading.Timer(delay, start, (delay, min_price_difference, min_usdt, max_usdt, max_limit_price, min_limit_price)).start()
    trading_depth = get_trading_depth()
    lowest_sell = trading_depth[0]
    highest_buy = trading_depth[1]
    print("Lowest : "+str(lowest_sell))
    print("Highest : "+str(highest_buy))
    price_difference = round(lowest_sell - highest_buy, const.price_decimals)
    print('Current Price Difference: ' + str(price_difference))
    if min_price_difference <= price_difference and highest_buy <= max_limit_price and lowest_sell >= min_limit_price:
        random_quantity = random_float(min_usdt, max_usdt, const.quantity_decimals)
        print('BuySell Quantity: ' + str(random_quantity) + ' USDT')
        random_price = random_float(highest_buy, lowest_sell, const.price_decimals)
        print('BuySell Price: ' + str(random_price) + ' USDT')
        list = []
        list.append({"symbol":const.market, "type":'sell', "price":random_price, "amount":random_quantity, "custom_id":''})
        list.append({"symbol":const.market, "type":'buy', "price":random_price, "amount":random_quantity, "custom_id":''})
        data = json.dumps(list)
        orderBatch(data=data)



print('START CREATE VOLUME BOT FOR ' + const.market)
min_usdt = input("Please enter random min quantity (USDT) : ")
print('Order Min Quantity : ' + min_usdt + ' USDT / order')
max_usdt = input("Please enter random max quantity (USDT) : ")
print('Order Max Quantity : ' + max_usdt + ' USDT / order')
min_price_difference = input("Please enter min difference to run volume bots (USDT) maximum 4 decimals (Ex. 0.0001) : ")
print('Min Price Difference : ' + min_price_difference + ' USDT')
delay = input("Please enter delay in seconds (Ex: 5.5) : ")
print('Delay : ' + delay + ' seconds')
max_limit_price = input("Please enter maximum price to run volume bots (USDT): ")
print('Order Max Price : ' + max_limit_price + ' USDT')
min_limit_price = input("Please enter minimum price to run volume bots (USDT): ")
print('Order Min Price : ' + min_limit_price + ' USDT')


start(float(delay), float(min_price_difference), float(min_usdt), float(max_usdt), float(max_limit_price), float(min_limit_price))

# TIDAK ADA INTERVAL DI LBANK