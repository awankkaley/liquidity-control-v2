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
#     api_key="8fd780fc-d874-4f79-a3b8-626b264d9bfe",
#     private_key="MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAM6tzfXyLTJ+y05nUbY/Sv97Iylbvy9jqtgHYCVd21j7Ic7p+Db+PCMVYc60pji9rcY8YlnYWKQzDdiGY6vchPKkORwimQU+17S5iFuAPK+GBRvPm+6U7xkcrFg5OgfchcT1SH1msjUmOE9bcQpTZM4BRodp3rRThfesQNKzStnFAgMBAAECgYEAgZnrdTaPsQJhaqDPVIEL/niw69ZkZMsS7rRxTf009u9DnASLabCy9S0LUBtnwFzxA0YKRlyr+Qsqu4RKLBL0KjF8FEGKnZDLlXFdjV4F4G16OuhdGPLSiAXy3e/X1BYU85x1izKY6DADEtF4y0WQmRnOLX1IdwDpIZp2euCCO2ECQQD97roclbyIruMF52CDhVAsMmTkC3buwWv6Gy+1Hw95p5i0sApc7HDgPjeCYZ3hH/5HQoQ26jfr1NgNMIE+VbP3AkEA0FyWKkylYe6S1Fn5XsU8ciA0b+zAtQHnY3vBSrW7WhcsSxp4RRmSLxUiu7wrnzIIOVjvV+Uo+TU4HhdpSLj5IwJAc98IW9zT0AcFnv8Kolkl0VUZhpnYpm/qZpEbPumydQ/N9b1SrT5S73BUghErKrwfmsK2dByCcgGIqNQWVaxj1wJABRpPXyfTYQubsvGlJsoDyfO59QfCTGyIgyozuKWsue8ZWZmDWoXey6Jj4F8iXlq2Utk3u1pUX44LGsmN/YbyKwJADcl82y+IkR4iQpXa0Iz0YNiV0viMFcOZp1UyY/nCyb6kf/oc2CZ79AssQHBb2uoLA6MsW+cWG7fvPCZQtv1XMQ=="
# )
