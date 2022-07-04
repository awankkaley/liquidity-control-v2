
import hashlib
import hmac
import json
import time

import requests


BASE_URL = "https://indodax.com"
# secretKey = "907fb24c24633e0501ea6f2ce39dafd396ab00335299de5cf803508078b6768a106bf2d9305a72ff"
# apiKey = "QF6RJTKZ-ESDUVZO3-SBCH4OWS-RJKKFBEW-X72LOPYX"


def orderBatch(data, api_key, private_key, acton, priority, self):
    count = 0
    no = 0
    if acton == "add_bulk_order":
        for item in json.loads(data):
            no += 1
            if(no % 10 == 0):
                time.sleep(6)
            try:
                res = order(item['symbol'], item['type'], item['price'],
                            item['amount'], api_key, private_key)
                print(res['success'])
                if res['success'] == 1:
                    count += 1
                    self.f.write("\n")
                    self.f.write("Order "+str(no)+": Sukses")
                    print("Order "+str(no)+": Sukses")
                else:
                    self.f.write("\n")
                    self.f.write("Order "+str(no)+": Failed -" +
                                 str(res))
                    print("Order "+str(no)+": Failed -"+str(res))
            except:
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
                if res['success'] == 1:
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


def get_trading_depth(pair):
    pair = pair.replace('_', '')
    response = requests.get(
        BASE_URL+"/api/depth/"+pair)
    lowest_sell = float(response.json()['sell'][0][0])
    highest_buy = float(response.json()['buy'][0][0])
    print(lowest_sell)
    print(highest_buy)
    return [lowest_sell, highest_buy]

# get_trading_depth("doge_idr")


def get_time_stamp():
    response = requests.get(BASE_URL+"/api/server_time")
    result = response.json()
    return result["server_time"]


def generateSignature(params, secretKey):
    par = []
    for k in sorted(params.keys()):
        par.append(k + '=' + str(params[k]))
    par = '&'.join(par)
    print(par)
    sign = hmac.new(secretKey, par.encode("utf8"), hashlib.sha512).hexdigest()
    return sign


def order(pair, side, price, size, api_key, secret_key):
    timestamp = get_time_stamp()
    method = "trade"
    type = side
    price = price
    pair = pair
    idr = size*price

    par = {}
    if(side == "buy"):
        par["idr"] = idr
    else:
        cde = pair.split("_")[0]
        par[cde] = size
    par["method"] = method
    par["pair"] = pair
    par["price"] = price
    par["timestamp"] = timestamp
    par["type"] = type

    sign = generateSignature(par, bytes(secret_key, 'utf-8'))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL+"/tapi", headers=header, data=par)

    print(response.json())
    return response.json()


def open_order(secretKey, api_key):
    timestamp = get_time_stamp()
    method2 = "openOrders"
    par = {}
    par["method"] = method2
    par["timestamp"] = timestamp
    sign = generateSignature(par, bytes(secretKey, 'utf-8'))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL+"/tapi", headers=header, data=par)

    print(response.json())


# open_order(
#     api_key="QF6RJTKZ-ESDUVZO3-SBCH4OWS-RJKKFBEW-X72LOPYX",
#     secretKey="907fb24c24633e0501ea6f2ce39dafd396ab00335299de5cf803508078b6768a106bf2d9305a72ff"
# )


def cancel_order(secretKey, api_key, id):
    timestamp = get_time_stamp()
    method = "cancelOrder"
    pair = "doge_idr"
    type = "sell"

    par = {}
    par["method"] = method
    par["order_id"] = id
    par["pair"] = pair
    par["timestamp"] = timestamp
    par["type"] = type

    sign = generateSignature(par, bytes(secretKey, 'utf-8'))
    header = {"Key": api_key, "Sign": sign}
    response = requests.post(url=BASE_URL+"/tapi", headers=header, data=par)

    print(response.json())


# cancel_order(
#     api_key="QF6RJTKZ-ESDUVZO3-SBCH4OWS-RJKKFBEW-X72LOPYX",
#     secretKey="907fb24c24633e0501ea6f2ce39dafd396ab00335299de5cf803508078b6768a106bf2d9305a72ff",
#     id="54562936"
# )
