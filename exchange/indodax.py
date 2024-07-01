from collections import OrderedDict
import hashlib
import hmac
import json
import time
from urllib import response
from datetime import datetime
import requests


BASE_URL = "https://indodax.com"


def orderBatch(data, api_key, private_key, acton, priority, self):
    count = 0
    no = 0
    if acton == "add_bulk_order":
        for item in json.loads(data):
            no += 1
            if no % 10 == 0:
                time.sleep(1.2)
            try:
                res = order(
                    item["symbol"],
                    item["type"],
                    item["price"],
                    item["amount"],
                    api_key,
                    private_key,
                )
                if res["success"] == 1:
                    count += 1
                    self.f.write("\n")
                    self.f.write(
                        "Order "
                        + str(no)
                        + ": Success, ID: "
                        + str(res["return"]["order_id"])
                        + " Price: "
                        + str(item["price"])
                        + " Amount: "
                        + str(item["amount"])
                        + " Type: "
                        + str(item["type"])
                        + " Time: "
                        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    )
                    print(
                        "Order "
                        + str(no)
                        + ": Success, ID: "
                        + str(res["return"]["order_id"])
                        + " Price: "
                        + str(item["price"])
                        + " Amount: "
                        + str(item["amount"])
                        + " Type: "
                        + str(item["type"])
                        + " Time: "
                        + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    )
                else:
                    self.f.write("\n")
                    self.f.write("Order " + str(no) + ": Failed -" + str(res))
                    print("Order " + str(no) + ": Failed -" + str(res))
            except e:
                print(str(e))
                self.f.write("\n")
                self.f.write("Order " + str(no) + ": Request Failed")
                print("Order " + str(no) + ": Request Failed")
        self.success["text"] = str(count)
        self.result["text"] = "Process Completed, please check log"
        self.f.close()
    if acton == "create_volume":
        for item in json.loads(data):
            status = "Failed"
            no += 1
            try:
                res = order(
                    item["symbol"],
                    item["type"],
                    item["price"],
                    item["amount"],
                    api_key,
                    private_key,
                )
                if res["success"] == 1:
                    status = "Success"
                    if priority == 2:
                        if no == 1:
                            self.ob["text"] = str(status)
                            self.f.write(
                                "Order Buy: "
                                + status
                                + "ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                            self.f.write("\n")
                            print(
                                "Order Buy: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                        else:
                            self.os["text"] = str(status)
                            self.f.write(
                                "Order Sell: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                            self.f.write("\n")
                            print(
                                "Order Sell: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                    else:
                        if no == 1:
                            self.os["text"] = str(status)
                            self.f.write(
                                "Order Sell: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                            self.f.write("\n")
                            print(
                                "Order Sell: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                        else:
                            self.ob["text"] = str(status)
                            self.f.write(
                                "Order Buy: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                            self.f.write("\n")
                            print(
                                "Order Buy: "
                                + status
                                + " ID: "
                                + str(res["return"]["order_id"])
                                + " Price: "
                                + str(item["price"])
                                + " Amount: "
                                + str(item["amount"])
                                + " Time: "
                                + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            )
                else:
                    if priority == 2:
                        if no == 1:
                            self.ob["text"] = str(status + "-" + str(res))
                            self.f.write("Order Buy: " + status + "-" + str(res))
                            self.f.write("\n")
                            print("Order Buy: " + status + "-" + str(res))
                        else:
                            self.os["text"] = str(status + "-" + str(res))
                            self.f.write("Order Sell: " + status + "-" + str(res))
                            self.f.write("\n")
                            print("Order Sell: " + status + "-" + str(res))
                    else:
                        if no == 1:
                            self.os["text"] = str(status + "-" + str(res))
                            self.f.write("Order Sell: " + status + "-" + str(res))
                            self.f.write("\n")
                            print("Order Sell: " + status + "-" + str(res))
                        else:
                            self.ob["text"] = str(status + "-" + str(res))
                            self.f.write("Order Buy: " + status + "-" + str(res))
                            self.f.write("\n")
                            print("Order Buy: " + status + "-" + str(res))
            except Exception as e:
                print("------ERRROOOORRRR------- : " + str(e))
                if priority == 2:
                    if no == 1:
                        self.ob["text"] = str(status + "- Request Failed")
                        self.f.write("Order Buy: " + status + "-Request Failed")
                        self.f.write("\n")
                        print("Order Buy: " + status + "- Request Failed")
                    else:
                        self.os["text"] = str(status + "- Request Failed")
                        self.f.write("Order Sell: " + status + "- Request Failed")
                        self.f.write("\n")
                        print("Order Sell: " + status + "- Request Failed")
                else:
                    if no == 1:
                        self.os["text"] = str(status + "-Request Failed")
                        self.f.write("Order Sell: " + status + "-Request Failed")
                        self.f.write("\n")
                        print("Order Sell: " + status + "-Request Failed")
                    else:
                        self.ob["text"] = str(status + "-Request Failed")
                        self.f.write("Order Buy: " + status + "-Request Failed")
                        self.f.write("\n")
                        print("Order Buy: " + status + "-Request Failed")


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
    return response.json()


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


def get_balance(pair, api_key, secret_key, self):
    try:
        res = balance(pair, api_key, secret_key)
        self.tokenA["text"] = res[0]
        self.tokenB["text"] = res[1]
    except Exception as e:
        print(str(e))
        self.tokenA["text"] = "Failed"
        self.tokenB["text"] = "Failed"


def get_price(pair, self):
    try:
        res = price(pair)
        self.current_price["text"] = res
    except Exception as e:
        print(str(e))
        self.current_price["text"] = "Failed"


def cancel_all(pair, api_key, secret_key):
    orders = get_orders(pair, api_key, secret_key)
    for order in orders["return"]["orders"]:
        cancel(pair, order["order_id"], order["type"], api_key, secret_key)


# print(
#     cancel_all(
#         "algo_idr",
#         "51EU7SEP-1Z5PG8E1-5CAYHVSP-LUYRXVBI-PLXAXQCR",
#         "284c491c7f609599550413e4ebd19b106069c8cc8a44952d07f9003c16c1276714fd67e69838e533",
#     )
# )

# print(
#     get_orders(
#         "algo_idr",
#         "51EU7SEP-1Z5PG8E1-5CAYHVSP-LUYRXVBI-PLXAXQCR",
#         "284c491c7f609599550413e4ebd19b106069c8cc8a44952d07f9003c16c1276714fd67e69838e533",
#     )
# )

# print(
#     cancel(
#         "algo_idr",
#         "28511526",
#         "buy",
#         "51EU7SEP-1Z5PG8E1-5CAYHVSP-LUYRXVBI-PLXAXQCR",
#         "284c491c7f609599550413e4ebd19b106069c8cc8a44952d07f9003c16c1276714fd67e69838e533",
#     )
# )


# print(
#     balance(
#         "algo_idr",
#         "51EU7SEP-1Z5PG8E1-5CAYHVSP-LUYRXVBI-PLXAXQCR",
#         "284c491c7f609599550413e4ebd19b106069c8cc8a44952d07f9003c16c1276714fd67e69838e533",
#     )
# )
