import json
import sys
import threading
from utils.exchange import get_trading_depth, orderBatch
from utils.math_utils import random_float


def start(delay, min_price_difference, min_usdt, max_usdt, max_limit_price, min_limit_price, market, quantity_decimals,price_decimals,api_key,private_key,exchange,priority ):
    threading.Timer(delay, start, (delay, min_price_difference, min_usdt, max_usdt, max_limit_price, min_limit_price, market, quantity_decimals,price_decimals,api_key,private_key,exchange,priority)).start()
    print("\n---DATA----")
    trading_depth = get_trading_depth(market,exchange)
    lowest_sell = trading_depth[0]
    highest_buy = trading_depth[1]
    print("Lowest : "+str(lowest_sell))
    print("Highest : "+str(highest_buy))
    price_difference = round(lowest_sell - highest_buy, price_decimals)
    print('Current Price Difference: ' + str(price_difference))
    if min_price_difference <= price_difference and highest_buy <= max_limit_price and lowest_sell >= min_limit_price:
        random_quantity = random_float(min_usdt, max_usdt, quantity_decimals)
        print('BuySell Quantity: ' + str(random_quantity) + ' USDT')
        random_price = random_float(highest_buy, lowest_sell, price_decimals)
        token_per_order = round(float(random_quantity / random_price), int(quantity_decimals))
        print('BuySell Quantity Token: ' + str(token_per_order))
        print('BuySell Price: ' + str(random_price) + ' USDT')
        list = []
        if priority == 1:
            list.append({"symbol":market, "type":'sell', "price":random_price, "amount":random_quantity, "custom_id":''})
            list.append({"symbol":market, "type":'buy', "price":random_price, "amount":random_quantity, "custom_id":''})
        if priority == 2:
            list.append({"symbol":market, "type":'buy', "price":random_price, "amount":random_quantity, "custom_id":''})
            list.append({"symbol":market, "type":'sell', "price":random_price, "amount":random_quantity, "custom_id":''})
        data = json.dumps(list)
        orderBatch(data=data,api_key=api_key,private_key=private_key,acton="create_volume",exchange=exchange)



print('----START CREATE VOLUME BOT----')
# input
try:
    with open('credential.txt') as f:
        lines = f.readlines()
        exchange = lines[0].replace("\n", "")
        api_key = lines[1].replace("\n", "")
        private_key = lines[2].replace("\n", "")
        market = lines[3].replace("\n", "")
        price_decimals = lines[4].replace("\n", "")
        quantity_decimals = lines[5].replace("\n", "")
except:
    print('Credential Not Found, Please set your credential first')
    sys.exit()


min_usdt = input("Please enter random min quantity (USDT) : ")
print('Order Min Quantity : ' + min_usdt + ' USDT / order')
max_usdt = input("Please enter random max quantity (USDT) : ")
print('Order Max Quantity : ' + max_usdt + ' USDT / order')
min_price_difference = input("Please enter min difference to run volume bots (USDT) maximum "+price_decimals+" decimals: ")
print('Min Price Difference : ' + min_price_difference + ' USDT')
delay = input("Please enter delay in seconds (Ex: 5.5) : ")
print('Delay : ' + delay + ' seconds')
max_limit_price = input("Please enter maximum price to run volume bots (USDT): ")
print('Order Max Price : ' + max_limit_price + ' USDT')
min_limit_price = input("Please enter minimum price to run volume bots (USDT): ")
print('Order Min Price : ' + min_limit_price + ' USDT')
while True:
    try:
        priority = int(input("Please select priority (1.Sell First, 2.Buy First): "))
        priority_title = "Buy First"
        if(priority == 1):
            priority_title = "Sell First"
            print('Priority : ' + str(priority_title))
    except ValueError:
        print("enter a valid value (number)")
        continue
    else:
        if priority not in [1,2]:
            print("invalid key")
            continue
        else:
            break


start(float(delay), float(min_price_difference), float(min_usdt), float(max_usdt), float(max_limit_price), float(min_limit_price), market, int(quantity_decimals), int(price_decimals), str(api_key), str(private_key), str(exchange), int(priority))
input("--------END-----------\n")
