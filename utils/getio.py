from cmath import log
import hmac
import requests
import hashlib
import time
import json
from datetime import datetime
import jwt

now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def get_signature(access_key_client, secret_key_client,method, url, query_string=None, payload_string=None):
    key = access_key_client       # api_key
    secret = secret_key_client    # api_secret

    t = time.time()
    m = hashlib.sha512()
    m.update((payload_string or "").encode('utf-8'))
    hashed_payload = m.hexdigest()
    s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
    sign = hmac.new(secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
    return {'KEY': key, 'Timestamp': str(t), 'SIGN': sign}

def get_trading_depth(pair):
    response = requests.get(
        'https://api.gateio.ws/api/v4/spot/order_book?currency_pair='+pair)
    lowest_sell = float(response.json()['asks'][0][0])
    highest_buy = float(response.json()['bids'][0][0])
    return [lowest_sell, highest_buy]

# BTC_USD
# print(get_trading_depth("DOGE_USDT"))

def order(pair, side, price, size, api_key, secret_key):

    header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    host = "https://api.gateio.ws"
    prefix = "/api/v4"
    url = '/spot/orders'
    full_url = host + prefix + url
    par = {}
    if(side == "buy"):
        par["side"] = "buy"
    else:
        par["side"] = "sell"

    par["currency_pair"] = pair
    par["text"] = "t-abc123"
    par["account"] = "spot"
    par["type"] = "limit"
    par["price"] = str(price)
    par["time_in_force"] = 'gtc'
    par["iceberg"] = '0'
    par["amount"] = str(size)
    request_content = json.dumps(par)
    
    sign_headers = get_signature(api_key,secret_key,'POST', prefix + url, "", request_content)
    sign_headers.update(header)
    
    response = requests.post(url=full_url,
                             headers=sign_headers, data=json.dumps(par))
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
                if 'id' in res:
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
                if 'id' in res:
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