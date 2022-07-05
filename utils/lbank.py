import random
import string
import requests as req
import hashlib

from base64 import b64encode

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def buildRSASignV2(params, t, private_key):
    rsa_private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + \
        private_key+"\n-----END RSA PRIVATE KEY-----"
    p = params
    p["timestamp"] = t
    p["signature_method"] = 'RSA'
    par = []
    for k in sorted(p.keys()):
        par.append(k + '=' + str(p[k]))
    par = '&'.join(par)
    msg = hashlib.md5(par.encode("utf8")).hexdigest().upper()
    key = RSA.importKey(rsa_private_key)
    signer = PKCS1_v1_5.new(key)
    digest = SHA256.new()
    digest.update(msg.encode('utf8'))
    sig1 = signer.sign(digest)
    sig = b64encode(sig1)
    return sig


def get_trading_depth(pair):
    response = req.get(
        'https://api.lbkex.com/v2/depth.do?symbol='+pair+'&size=3')
    print(str(response.json()))
    lowest_sell = float(response.json()['data']['asks'][0][0])
    highest_buy = float(response.json()['data']['bids'][0][0])
    return [lowest_sell, highest_buy]


def get_time_stamp():
    response = req.get('https://api.lbkex.com/v2/timestamp.do')
    result = response.json()
    return result["data"]


def orderBatch(data, api_key, private_key, acton,priority, self):
    urlstr = "https://api.lbkex.com/v2/batch_create_order.do"

    num = string.ascii_letters + string.digits
    randomstr = "".join(random.sample(num, 35))
    timestamp = get_time_stamp()
    par = {}
    header = {"signature_method": "RSA",
              'timestamp': str(timestamp), 'echostr': randomstr, "Content-Type": "application/x-www-form-urlencoded"}
    par["api_key"] = api_key
    par["signature_method"] = "RSA"
    par["echostr"] = randomstr
    par['orders'] = data

    sign = buildRSASignV2(params=par, t=timestamp, private_key=private_key)

    del par["echostr"]
    del par["signature_method"]
    del par["timestamp"]

    par['sign'] = sign
    res =  req.post(url=urlstr, data=par, headers=header)

    if res.status_code == 200:
        resp = res.json()
        if acton == "add_bulk_order":
            responseForBulk(resp=resp, self=self)
        if acton == "create_volume":
            responseForVolume(resp=resp,priority=priority,self=self)
    else:
        self.result['text'] = "Process Failed"


def responseForBulk(resp, self):
    if(resp['result'] == True):
        count = 0
        no = 0
        self.f.write("\n")
        self.f.write("------RESULT------")
        for res in resp['data']:
            no += 1
            status = "Failed"
            if res['result']:
                count += 1
                status = "Success"
                self.f.write("\n")
                self.f.write("Order "+str(no)+": "+status)
                print("Order "+str(no)+": "+status)
            else:
                self.f.write("\n")
                self.f.write("Order "+str(no)+": "+status+"-"+str(res['error_code']))
                print("Order "+str(no)+": "+status+"-"+str(res['error_code']))
        self.success['text'] = str(count)
        self.result['text'] = "Process Completed, please check log"
        self.f.close()
    else:
        self.result['text'] = "Process Failed"
        self.f.close()


def responseForVolume(resp,priority,self):
    if(resp['result'] == True):
        print("---RESULT----")
        no = 0
        for res in resp['data']:
            no += 1
            status = "Failed"
            if res['result']:
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
                        self.ob['text'] = str(status+"-"+str(res['error_code']))
                        self.f.write("Order Buy: "+status+"-"+str(res['error_code']))
                        self.f.write("\n")
                        print("Order Buy: "+status+"-"+str(res['error_code']))
                    else:
                        self.os['text'] = str(status+"-"+str(res['error_code']))
                        self.f.write("Order Sell: "+status+"-"+str(res['error_code']))
                        self.f.write("\n")
                        print("Order Sell: "+status+"-"+str(res['error_code']))
                else:
                    if(no == 1):
                        self.os['text'] = str(status+"-"+str(res['error_code']))
                        self.f.write("Order Sell: "+status+"-"+str(res['error_code']))
                        self.f.write("\n")
                        print("Order Sell: "+status+"-"+str(res['error_code']))
                    else:
                        self.ob['text'] = str(status+"-"+str(res['error_code']))
                        self.f.write("Order Buy: "+status+"-"+str(res['error_code']))
                        self.f.write("\n")
                        print("Order Buy: "+status+"-"+str(res['error_code']))
            
    else:
        self.result['text'] = "Process Failed"


def asset_information(api_key, private_key):
    urlstr = "https://api.lbkex.com/v2/user_info.do"

    num = string.ascii_letters + string.digits
    randomstr = "".join(random.sample(num, 35))
    timestamp = get_time_stamp()
    par = {}
    header = {"signature_method": "RSA",
              'timestamp': str(timestamp), 'echostr': randomstr, "Content-Type": "application/x-www-form-urlencoded"}
    par["api_key"] = api_key
    par["signature_method"] = "RSA"
    par["echostr"] = randomstr

    sign = buildRSASignV2(params=par, t=timestamp, private_key=private_key)

    del par["echostr"]
    del par["signature_method"]
    del par["timestamp"]

    par['sign'] = sign
    res = req.post(url=urlstr, data=par, headers=header)

    if res.status_code == 200:
        resp = res.json()
        print(resp)
        return resp
    else:
        print(res.status_code)

# asset_information(
#     api_key="da2c345e-d354-415c-beae-9e55d9e1d415",
#     private_key="MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKS49YniYbvKc04Z+9TnT/aFzJl19moJ5ubsMxPodEPN2z696jOzry6ovzPUnPN2Q08iJHwLLyttCw5HuJAahPvoucD3rutK8XlwQVKB1YrGKczzGauY/n5VC8W96nJq/ENFhXKpM8et0hJLJiqKf+Zm6KdjA2hloxGAN7QQO8ENAgMBAAECgYAbxVcYJQOHLo2cCENt1IWlsU8aPEoL/JliK0Y9P/6CA+3HuSsIBm4tdqOtsFW5siGM8Nun0hbkwmCPysWx/daXgItjcLaTIMjZTVsRv6EW06X1jJOfPSp/8WvB48sG45TfvsLTUSfRJ3LmVkQNKGkNaLzir7C22cl2r2gSUGtaYQJBANXd64TaCmyO82m+OUV00U8zZZWS8++IBfTO/JebfijeRz/DmWrvEI5/sCELQwbkFIcwWcpNaB/xyl/Q9P5at7kCQQDFLIKpWV2JGTCkGkEMTgoN6rjFRn7sut02JTcThRXi5VnAa7nHi3HW3pZQsk6tYOF4y0rTdaWTO8wlUaU5ddX1AkB26VAlavJ2z7jJp6nCU6R5a/NkifO10CS3rErHpP4tjQGCk6f+y/Oht59fkBpxf2lmjVyvXgCyGkdSpSVDM3+JAkEAltUj5xS73uLsOLz0wcr5GghS7GavNb0E+CSj60TFp1q3u+Esrx9XKH4CEx0z3qHcGaG6TeUTknwOAQZiFIC1+QJAM2vSjYQ7BtL2itb94s+nkhG3C+e8rnJdn51k8KsdVpMwcdpVFrfGvr1kphqA6u4GF4CGw66GEHXuwcYahC7HMg=="
# )
