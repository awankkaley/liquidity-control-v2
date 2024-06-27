import base64, hashlib, hmac, json, requests, time


def call(
    api_jey, secret_key, need_auth, method, path, body_json=None, recv_window=None
):
    method = method.upper()
    if need_auth:
        timestamp = str(int(time.time() * 1000))
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
    response = call(
        api_key, secret_key, True, "POST", "/orders", post_orders_req_body, 200
    )
    return response


def orderBatch(data, api_key, private_key, acton, priority, self):
    count = 0
    no = 0
    if acton == "add_bulk_order":
        for item in json.loads(data):
            no += 1
            if no % 40 == 0:
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
                    self.f.write("Order " + str(no) + ": Sukses")
                    print("Order " + str(no) + ": Sukses")
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
                            self.f.write("Order Buy: " + status)
                            self.f.write("\n")
                            print("Order Buy: " + status)
                        else:
                            self.os["text"] = str(status)
                            self.f.write("Order Sell: " + status)
                            self.f.write("\n")
                            print("Order Sell: " + status)
                    else:
                        if no == 1:
                            self.os["text"] = str(status)
                            self.f.write("Order Sell: " + status)
                            self.f.write("\n")
                            print("Order Sell: " + status)
                        else:
                            self.ob["text"] = str(status)
                            self.f.write("Order Buy: " + status)
                            self.f.write("\n")
                            print("Order Buy: " + status)
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


def cancel(id, api_key, secret_key):
    response = call(api_key, secret_key, True, "DELETE", "/orders/" + id)
    return response

# post_orders_req_body = {
#     "side": "buy",
#     "type": "limit",
#     "amount": 1,
#     "price": 10000,
#     "tradingPairName": "BTC-KRW",
# }


# print(call(True, 'GET', '/orders'))
# print(call(True, 'GET', '/orders?includePast=true'))
# print(call(True, 'GET', '/trades?limit=1'))
# print(call(False, 'GET', '/trading-pairs/BTC-KRW/book?level=1'))
