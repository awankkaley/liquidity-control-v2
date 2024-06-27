from cmath import log
import hmac
import requests
import hashlib
import time
import json
from datetime import datetime
import jwt

now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def get_signature(access_key_client, secret_key_client):
    payload = {
        "accessKey": access_key_client,
        "nonce": now
    }
    token = jwt.encode(payload, secret_key_client, algorithm="HS256")
    return token


def get_trading_depth(pair):
    response = requests.get(
        'https://openapi.flybit.com/v1/orderbook?MARKET='+pair)
    lowest_sell = float(response.json()['S'][0]['OC_PRICE'])
    highest_buy = float(response.json()['B'][0]['OC_PRICE'])
    return [lowest_sell, highest_buy]


def order(pair, side, price, size, api_key, secret_key):

    sign = get_signature(api_key, secret_key)
    header = {"Authorization": "Bearer "+sign,
              "Content-Type": 'application/json'}

    par = {}
    if(side == "buy"):
        par["SIDE"] = "B"
    else:
        par["SIDE"] = "S"

    par["MARKET"] = pair
    par["CALL_TYPE"] = "N"
    par["PRICE"] = str(price)
    par["AMOUNT"] = str(size)

    response = requests.post(url="https://openapi.flybit.com/v1/orders",
                             headers=header, data=json.dumps(par))
    print(response.json())
    return response.json()


def orderBatch(data, api_key, private_key, acton, priority, self):
    count = 0
    no = 0
    if acton == "add_bulk_order":
        for item in json.loads(data):
            no += 1
            if(no % 40 == 0):
                time.sleep(1.2)
            try:
                res = order(item['symbol'], item['type'], item['price'],
                            item['amount'], api_key, private_key)
                if 'ORDER_ID' in res:
                    count += 1
                    self.f.write("\n")
                    self.f.write("Order "+str(no)+": Sukses")
                    print("Order "+str(no)+": Sukses")
                else:
                    self.f.write("\n")
                    self.f.write("Order "+str(no)+": Failed -" +
                                 str(res))
                    print("Order "+str(no)+": Failed -"+str(res))
            except e:
                print(str(e))
                self.f.write("\n")
                self.f.write("Order "+str(no)+": Request Failed")
                print("Order "+str(no)+": Request Failed")
        self.success['text'] = str(count)
        self.result['text'] = "Process Completed, please check log"
        self.f.close()
    if acton == "create_volume":
        for item in json.loads(data):
            status = "Failed"
            no += 1
            try:
                res = order(item['symbol'], item['type'], item['price'],
                            item['amount'], api_key, private_key)
                if 'ORDER_ID' in res:
                    status = "Success"
                    if priority == 2:
                        if(no == 1):
                            self.ob['text'] = str(status)
                            self.f.write("Order Buy: "+status)
                            self.f.write("\n")
                            print("Order Buy: "+status)
                        else:
                            self.os['text'] = str(status)
                            self.f.write("Order Sell: "+status)
                            self.f.write("\n")
                            print("Order Sell: "+status)
                    else:
                        if(no == 1):
                            self.os['text'] = str(status)
                            self.f.write("Order Sell: "+status)
                            self.f.write("\n")
                            print("Order Sell: "+status)
                        else:
                            self.ob['text'] = str(status)
                            self.f.write("Order Buy: "+status)
                            self.f.write("\n")
                            print("Order Buy: "+status)
                else:
                    if priority == 2:
                        if(no == 1):
                            self.ob['text'] = str(
                                status+"-"+str(res))
                            self.f.write("Order Buy: "+status +
                                         "-"+str(res))
                            self.f.write("\n")
                            print("Order Buy: "+status +
                                  "-"+str(res))
                        else:
                            self.os['text'] = str(
                                status+"-"+str(res))
                            self.f.write("Order Sell: "+status +
                                         "-"+str(res))
                            self.f.write("\n")
                            print("Order Sell: "+status +
                                  "-"+str(res))
                    else:
                        if(no == 1):
                            self.os['text'] = str(
                                status+"-"+str(res))
                            self.f.write("Order Sell: "+status +
                                         "-"+str(res))
                            self.f.write("\n")
                            print("Order Sell: "+status +
                                  "-"+str(res))
                        else:
                            self.ob['text'] = str(
                                status+"-"+str(res))
                            self.f.write("Order Buy: "+status +
                                         "-"+str(res))
                            self.f.write("\n")
                            print("Order Buy: "+status +
                                  "-"+str(res))
            except Exception as e:
                print("------ERRROOOORRRR------- : "+str(e))
                if priority == 2:
                    if(no == 1):
                        self.ob['text'] = str(status+"- Request Failed")
                        self.f.write("Order Buy: "+status+"-Request Failed")
                        self.f.write("\n")
                        print("Order Buy: "+status+"- Request Failed")
                    else:
                        self.os['text'] = str(status+"- Request Failed")
                        self.f.write("Order Sell: "+status+"- Request Failed")
                        self.f.write("\n")
                        print("Order Sell: "+status+"- Request Failed")
                else:
                    if(no == 1):
                        self.os['text'] = str(status+"-Request Failed")
                        self.f.write("Order Sell: "+status+"-Request Failed")
                        self.f.write("\n")
                        print("Order Sell: "+status+"-Request Failed")
                    else:
                        self.ob['text'] = str(status+"-Request Failed")
                        self.f.write("Order Buy: "+status+"-Request Failed")
                        self.f.write("\n")
                        print("Order Buy: "+status+"-Request Failed")


# order("USDT-LIFE", "buy", 0.06064, 17, "MjAyMy0wNi0yN1QxNTozMTowMFotNjVjOTNlZDAtYzBjMS00NGZhLThjNmUtZjU4YTcyNDU2YWMzMjc2MTE5",
#       "$2a$10$/8hcLGBnSrBSLATI47IHXeEMaVKo3IR2UyXYmrPeDOk1oIf5JPHr")
