from cmath import log
import hmac
import time
import requests
import hashlib
import json


def get_signature(query, secret_key):
    signature = hmac.new(bytes(secret_key, 'latin-1'), msg=bytes(query,
                         'latin-1'), digestmod=hashlib.sha256).hexdigest()
    print(signature)
    return signature


def get_trading_depth(pair):
    response = requests.get(
        'https://www.mexc.com/open/api/v2/market/depth?symbol='+pair+'&depth=500')
    # print(str(response.json()))
    lowest_sell = float(response.json()['data']['asks'][0]['price'])
    highest_buy = float(response.json()['data']['bids'][0]['price'])
    return [lowest_sell, highest_buy]


def get_time_stamp():
    response = requests.get('https://api.mexc.com/api/v3/time')
    result = response.json()
    return result["serverTime"]


def order(pair, side, price, size, api_key, secret_key):
    timestamp = get_time_stamp()
    newPair = pair.replace('_', '')
    query = "symbol="+newPair+"&side="+side.upper() + \
        "&type=LIMIT&quantity=" + \
            str(size)+"&price="+str(price) + \
        "&recvWindow=5000&timestamp="+str(timestamp)

    sign = get_signature(query, secret_key)
    header = {"X-MEXC-APIKEY": api_key, "Content-Type": 'application/json'}

    req = query+"&signature="+sign
    # print(req)
    response = requests.post(url="https://api.mexc.com/api/v3/order",
                             headers=header, data=req)
    print(response.json())
    return response.json()



def orderBatch(data, api_key, private_key, acton, priority, self):
    count = 0
    no = 0
    if acton == "add_bulk_order":
        for item in json.loads(data):
            no += 1
            if(no % 20 == 0):
                time.sleep(1.2)
            try:
                res = order(item['symbol'], item['type'], item['price'],
                            item['amount'], api_key, private_key)
                if 'orderId' in res:
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
                if 'orderId' in res:
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

