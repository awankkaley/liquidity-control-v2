from collections import OrderedDict
import hashlib
import hmac
import json
import time
from urllib import response
from datetime import datetime
import requests


BASE_URL = "https://indodax.com"


def get_trading_depth(pair):
    pair = pair.replace("_", "")
    response = requests.get(BASE_URL + "/api/depth/" + pair)
    lowest_sell = float(response.json()["sell"][0][0])
    highest_buy = float(response.json()["buy"][0][0])
    return [lowest_sell, highest_buy]


def price(pair):
    pair = pair.replace("_", "")
    response = requests.get(BASE_URL + "/api/ticker/" + pair)
    last_price = float(response.json()["ticker"]["last"])
    return last_price


def get_time_stamp():
    response = requests.get(BASE_URL + "/api/server_time")
    result = response.json()
    return result["server_time"]


def generateSignature(params, secretKey):
    par = []
    for k in sorted(params.keys()):
        par.append(k + "=" + str(params[k]))
    par = "&".join(par)
    sign = hmac.new(secretKey, par.encode("utf8"), hashlib.sha512).hexdigest()
    return sign


def order(pair, side, price, size, api_key, secret_key):
    timestamp = get_time_stamp()
    method = "trade"
    type = side
    price = price
    pair = pair
    idr = size * price

    par = {}
    if side == "buy":
        par["idr"] = idr
    else:
        cde = pair.split("_")[0]
        par[cde] = size
    par["method"] = method
    par["pair"] = pair
    par["price"] = price
    par["timestamp"] = timestamp
    par["type"] = type
    sorted_par = {}
    param = sorted(par.items())
    for i in param:
        sorted_par[i[0]] = i[1]

    sign = generateSignature(sorted_par, bytes(secret_key, "utf-8"))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL + "/tapi", headers=header, data=sorted_par)
    response = response.json()
    if response["success"] == 1:
        return {
            "success": True,
            "order_id": response["return"]["order_id"],
            "type": type,
            "price": price,
            "amount": size,
            "created_at": datetime.now(),
        }
    else:
        return {
            "success": False,
            "errorMessage": response["error"],
        }


def get_orders(pair, api_key, secret_key):
    timestamp = get_time_stamp()
    method = "openOrders"

    par = {}
    par["method"] = method
    par["pair"] = pair
    par["timestamp"] = timestamp

    sorted_par = {}
    param = sorted(par.items())
    for i in param:
        sorted_par[i[0]] = i[1]

    sign = generateSignature(sorted_par, bytes(secret_key, "utf-8"))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL + "/tapi", headers=header, data=sorted_par)
    return response.json()


def cancel(pair, order_id, type, api_key, secret_key):
    timestamp = get_time_stamp()
    method = "cancelOrder"

    par = {}
    par["method"] = method
    par["pair"] = pair
    par["order_id"] = order_id
    par["type"] = type
    par["timestamp"] = timestamp

    sorted_par = {}
    param = sorted(par.items())
    for i in param:
        sorted_par[i[0]] = i[1]

    sign = generateSignature(sorted_par, bytes(secret_key, "utf-8"))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL + "/tapi", headers=header, data=sorted_par)
    return response.json()


def balance(pair, api_key, secret_key):
    tokenA = pair.split("_")[0]
    tokenB = pair.split("_")[1]
    timestamp = get_time_stamp()
    method = "getInfo"

    par = {}
    par["method"] = method
    par["timestamp"] = timestamp

    sorted_par = {}
    param = sorted(par.items())
    for i in param:
        sorted_par[i[0]] = i[1]

    sign = generateSignature(sorted_par, bytes(secret_key, "utf-8"))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL + "/tapi", headers=header, data=sorted_par)
    response = response.json()
    balance = response["return"]["balance"]
    tokenA = balance[tokenA]
    tokenB = balance[tokenB]
    return [tokenA, tokenB]


def cancel_all(pair, api_key, secret_key):
    orders = get_orders(pair, api_key, secret_key)
    for order in orders["return"]["orders"]:
        cancel(pair, order["order_id"], order["type"], api_key, secret_key)


# print(
#     cancel_all(
#         "algo_idr",
#         "GQGVC7DI-V7FCWG6O-IRFKWIEY-HUXT6SQQ-P1482IJZ",
#         "9521c1dbf6cb4b91597e669ca7d7bbf7a433eda4cece45bb3d015b6d1ce62376936b08ef751edb0a",
#     )
# )

# print(
#     get_orders(
#         "algo_idr",
#         "GQGVC7DI-V7FCWG6O-IRFKWIEY-HUXT6SQQ-P1482IJZ",
#         "9521c1dbf6cb4b91597e669ca7d7bbf7a433eda4cece45bb3d015b6d1ce62376936b08ef751edb0a",
#     )
# )

# print(
#     cancel(
#         "algo_idr",
#         "28511526",
#         "buy",
#         "GQGVC7DI-V7FCWG6O-IRFKWIEY-HUXT6SQQ-P1482IJZ",
#         "9521c1dbf6cb4b91597e669ca7d7bbf7a433eda4cece45bb3d015b6d1ce62376936b08ef751edb0a",
#     )
# )


# print(
#     balance(
#         "algo_idr",
#         "GQGVC7DI-V7FCWG6O-IRFKWIEY-HUXT6SQQ-P1482IJZ",
#         "284c491c7f609599550413e4ebd19b19521c1dbf6cb4b91597e669ca7d7bbf7a433eda4cece45bb3d015b6d1ce62376936b08ef751edb0a06069c8cc8a44952d07f9003c16c1276714fd67e69838e533",
#     )
# )
