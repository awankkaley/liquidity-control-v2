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
    if response["statusCode"] == 200:
        return {
            "success": True,
            "order_id": response["body"]["id"],
            "type": response["body"]["side"],
            "price": response["body"]["price"],
            "amount": response["body"]["amount"],
            "created_at": time.time(),
        }
    else:
        return {
            "success": False,
            "errorMessage": response["body"]["errorMessage"],
        }

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

def price(pair):
    response = call("", "", False, "GET", "/trading-pairs/" + pair + "/ticker")
    last_price = float(response["body"]["price"])
    return last_price

def cancel(pair, order_id, type, api_key, private_key):
    print("cancel")
    response = call(api_key, private_key, True, "DELETE", "/orders/" + order_id)
    return response


def orders(api_key, secret_key):
    response = call(api_key, secret_key, True, "GET", "/orders")
    return response["body"]


def cancel_all(api_key, secret_key):
    orders_data = orders(api_key, secret_key)
    for order in orders_data:
        cancel("", order["id"], "", api_key, secret_key)


# print(
#     cancel_all(
#         "1-182ac4e6-fe01-4a64-a77c-c315fcce5-des8c494ea8351681ac061990565",
#         "3CHcr+xpC9cdsWi5K+CLDWwhlHjpe02GXR+OjQ6IuSA83z68IEKbAGYjXB0i9Kb1Nvccgy+AbiXti05E5Tu/+A==",
#     )
# )
# print(
#     orders(
#         "1-182ac4e6-fe01-4a64-a77c-c315fcce5-des8c494ea8351681ac061990565",
#         "3CHcr+xpC9cdsWi5K+CLDWwhlHjpe02GXR+OjQ6IuSA83z68IEKbAGYjXB0i9Kb1Nvccgy+AbiXti05E5Tu/+A==",
#     )
# )
