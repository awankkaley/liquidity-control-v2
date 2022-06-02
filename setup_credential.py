
api_key = input("Please input API Key : ")
print('api key inserted')

private_key = input("Please input Private Key : ")
print('Private Key inserted')

market = input("Please input Market Pair (ex lbank : doge_usdt) : ")
print('Market Pair : ' + market)
while True:
        try:
                price_decimals = int(input("Please input Price Decimal: "))
                print('Price Decimal : ' + str(price_decimals))
        except ValueError:
                print("enter a valid value (number)")
                continue
        else:
                break

while True:
        try:
                quantity_decimals = int(input("Please input Qty Decimal: "))
                print('Qty Decimal : ' + str(quantity_decimals))
        except ValueError:
                print("enter a valid value (number)")
                continue
        else:
                break

with open('credential.txt', 'w') as f:
        f.write(api_key)
        f.write("\n")
        f.write(private_key)
        f.write("\n")
        f.write(market)
        f.write("\n")
        f.write(str(price_decimals))
        f.write("\n")
        f.write(str(quantity_decimals))        