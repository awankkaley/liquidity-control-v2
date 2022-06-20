import json
from logging import exception
from utils.bitmart.api_spot import APISpot


def get_trading_depth(pair):
    spotAPI = APISpot("api_key", "secret_key", "memo", timeout=(3, 10))
    result = spotAPI.get_symbol_book(symbol=pair, size=3, precision=6)
    lowest_sell = float(result[0]['data']['sells'][0]['price'])
    highest_buy = float(result[0]['data']['buys'][0]['price'])
    return [lowest_sell, highest_buy]

# print(get_trading_depth("DOGE_USDT"))


def orderBatch(data, api_key, private_key, acton, priority, self):
    count = 0
    no = 0
    if acton == "add_bulk_order":
        for item in json.loads(data):
            no += 1
            try:
                res = order(item['symbol'], item['type'], item['price'],
                            item['amount'], api_key, private_key)
                if res[0]['code'] == 1000:
                    count += 1
                    self.f.write("\n")
                    self.f.write("Order "+str(no)+": Sukses")
                    print("Order "+str(no)+": Sukses")
                else:
                    self.f.write("\n")
                    self.f.write("Order "+str(no)+": Failed -" +
                                 str(res[0]['code']))
                    print("Order "+str(no)+": Failed -"+str(res[0]['code']))
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
                if res[0]['code'] == 1000:
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
                                status+"-"+str(res['error_code']))
                            self.f.write("Order Buy: "+status +
                                         "-"+str(res['error_code']))
                            self.f.write("\n")
                            print("Order Buy: "+status +
                                  "-"+str(res['error_code']))
                        else:
                            self.os['text'] = str(
                                status+"-"+str(res['error_code']))
                            self.f.write("Order Sell: "+status +
                                         "-"+str(res['error_code']))
                            self.f.write("\n")
                            print("Order Sell: "+status +
                                  "-"+str(res['error_code']))
                    else:
                        if(no == 1):
                            self.os['text'] = str(
                                status+"-"+str(res['error_code']))
                            self.f.write("Order Sell: "+status +
                                         "-"+str(res['error_code']))
                            self.f.write("\n")
                            print("Order Sell: "+status +
                                  "-"+str(res['error_code']))
                        else:
                            self.ob['text'] = str(
                                status+"-"+str(res['error_code']))
                            self.f.write("Order Buy: "+status +
                                         "-"+str(res['error_code']))
                            self.f.write("\n")
                            print("Order Buy: "+status +
                                  "-"+str(res['error_code']))
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


def order(pair, side, price, size, api_key, secret_key):
    memo = "liquiditytest"
    spotAPI = APISpot(api_key, secret_key, memo, timeout=(10, 10))
    result = spotAPI.post_submit_order(
        symbol=pair, side=side, type='limit', price=price, size=size)
    return result

# order("DOGE_USDT","buy","0.055950", "90")


def cancel(pair, side):
    api_key = "f75d7a56689230de4e8aaf1139181308330433f1"
    secret_key = "b8919eef8b955c754bf8c41bf906f09858c2bb510cacd801cf21b6f1b37112c5"
    memo = "liquiditytest"
    spotAPI = APISpot(api_key, secret_key, memo, timeout=(10, 10))
    result = spotAPI.post_cancel_orders(symbol=pair, side=side)
    print(result)

# cancel("DOGE_USDT", "sell")


def history(pair, status):
    api_key = "f75d7a56689230de4e8aaf1139181308330433f1"
    secret_key = "b8919eef8b955c754bf8c41bf906f09858c2bb510cacd801cf21b6f1b37112c5"
    memo = "liquiditytest"
    spotAPI = APISpot(api_key, secret_key, memo, timeout=(10, 10))
    result = spotAPI.get_user_orders_v2(symbol=pair, status=status, N=100)
    print(result[0]['data'])

# history("DOGE_USDT",4)
