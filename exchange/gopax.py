import base64, hashlib, hmac, json, requests, time
from datetime import datetime


def server_time():
    response = requests.get("https://api.gopax.co.kr/time").json()
    return response["serverTime"]


def call(
    api_jey, secret_key, need_auth, method, path, body_json=None, recv_window=None
):
    method = method.upper()
    if need_auth:
        timestamp = str(server_time())
        include_querystring = method == "GET" and path.startswith("/orders?")
        p = path if include_querystring else path.split("?")[0]
        msg = "t" + timestamp + method + p
        msg += (str(recv_window) if recv_window else "") + (
            json.dumps(body_json) if body_json else ""
        )
        raw_secret = base64.b64decode(secret_key)
        raw_signature = hmac.new(
            raw_secret, str(msg).encode("utf-8"), hashlib.sha512
        ).digest()
        signature = base64.b64encode(raw_signature)
        headers = {"api-key": api_jey, "timestamp": timestamp, "signature": signature}
        if recv_window:
            headers["receive-window"] = str(recv_window)
    else:
        headers = {}
    req_func = {"GET": requests.get, "POST": requests.post, "DELETE": requests.delete}[
        method
    ]
    resp = req_func(
        url="https://api.gopax.co.kr" + path, headers=headers, json=body_json
    )
    return {
        "statusCode": resp.status_code,
        "body": resp.json(),
        "header": dict(resp.headers),
    }


def order(pair, side, price, size, api_key, secret_key):
    post_orders_req_body = {
        "side": side,
        "type": "limit",
        "amount": size,
        "price": price,
        "tradingPairName": pair,
    }
    response = call(api_key, secret_key, True, "POST", "/orders", post_orders_req_body)
    return response


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
                if "id" in res["body"]:
                    count += 1
                    self.f.write("\n")
                    self.f.write(
                        "Order "
                        + str(no)
                        + ": Success, ID: "
                        + str(res["body"]["id"])
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
                        + str(res["body"]["id"])
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
                if "id" in res["body"]:
                    status = "Success"
                    if priority == 2:
                        if no == 1:
                            self.ob["text"] = str(status)
                            self.f.write(
                                "Order Buy: "
                                + status
                                + "ID: "
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
                                + str(res["body"]["id"])
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
    response = call("", "", False, "GET", "/trading-pairs/" + pair + "/book")
    lowest_sell = float(response["body"]["ask"][0][1])
    highest_buy = float(response["body"]["bid"][0][1])
    return [lowest_sell, highest_buy]


def get_avail_by_asset(data, asset_value):
    for entry in data:
        if entry["asset"] == asset_value:
            return entry["avail"]
    return None  # If no entry with the specified asset is found


def balance(pair, api_key, secret_key):
    tokenA = pair.split("-")[0]
    tokenB = pair.split("-")[1]

    response = call(api_key, secret_key, True, "GET", "/balances")

    balance = response["body"]
    tokenA = get_avail_by_asset(balance, tokenA)
    tokenB = get_avail_by_asset(balance, tokenB)

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


def price(pair):
    response = call("", "", False, "GET", "/trading-pairs/" + pair + "/ticker")
    last_price = float(response["body"]["price"])
    return last_price


def get_price(pair, self):
    try:
        res = price(pair)
        self.current_price["text"] = res
    except Exception as e:
        # print(str(e))
        self.current_price["text"] = "Failed"


def cancel(id, api_key, secret_key):
    response = call(api_key, secret_key, True, "DELETE", "/orders/" + id)
    return response


def orders(api_key, secret_key):
    response = call(api_key, secret_key, True, "GET", "/orders")
    return response["body"]


def cancel_all(api_key, secret_key):
    orders_data = orders(api_key, secret_key)
    for order in orders_data:
        cancel(order["id"], api_key, secret_key)


