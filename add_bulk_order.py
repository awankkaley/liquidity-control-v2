import json
import sys
from utils.lbank import orderBatch
import utils.const as const



print('STARTING ADD BULK ORDER ON ' + const.pairing)

# input
amount = input("Please input budget (USDT) amount : ")
print('Budget : ' + amount + ' USDT')
order_type = input("Please enter order type (buy/sell) : ")
if order_type != 'buy' and order_type != 'sell':
    print('Wrong value')
    sys.exit()
print('Order Type : ' + order_type)
order_start_price = input("Please enter order start price : ")
print('Order Start Price : ' + order_start_price)
trailing_percentage = input("Please enter trailing percentage : ")
print('Trailing Percentage : ' + trailing_percentage + '%')
order_quantity = input("Please enter order quantity : ")
print('Order Quantity : ' + order_quantity)

# output
usdt_per_order = float(amount) / int(order_quantity)
print('usdt_per_order: ' + str(usdt_per_order))
distance_percentage_per_order = float(
    trailing_percentage) / int(order_quantity)
print('distance_percentage_per_order: ' + str(distance_percentage_per_order))

direction_amplifier = -1 if (order_type == 'buy') else 1

list = []

for index in range(int(order_quantity)):
    current_percentage = float(
        index * distance_percentage_per_order * direction_amplifier)
    price = float(order_start_price) + \
        float(order_start_price) * current_percentage / 100
    price = round(price, int(const.price_decimals))
    print('Price : ' + str(price))
    token_per_order = round(
        float(usdt_per_order / price), int(const.quantity_decimals))
    print('token_per_order: ' + str(token_per_order))
    list.append({"symbol": const.pairing, "type": order_type,
                "price": price, "amount": token_per_order, "custom_id": ''})

data = json.dumps(list)
orderBatch(data=data)

