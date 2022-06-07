from ast import If
from cgitb import reset
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
    lowest_sell = float(response.json()['data']['asks'][0][0])
    print('lowest_sell: ' + str(lowest_sell))
    highest_buy = float(response.json()['data']['bids'][0][0])
    print('highest_buy: ' + str(highest_buy))
    return [lowest_sell, highest_buy]


def get_time_stamp():
    response = req.get('https://api.lbkex.com/v2/timestamp.do')
    result = response.json()
    return result["data"]


def orderBatch(data, api_key, private_key, acton):
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
    res = req.post(url=urlstr, data=par, headers=header)

    if res.status_code == 200:
        resp = res.json()
        if acton == "add_bulk_order":
            responseForBulk(resp=resp)
        if acton == "create_volume":
            responseForVolume(resp=resp)
    else:
        input("--------TRANSACTION FAILED-----------")


def responseForBulk(resp):
    if(resp['result']):
        no = 0
        print("---RESULT----")
        for res in resp['data']:
            no += 1
            status = "Failed"
            if res['result']:
                status = "Success"
                print("Order "+str(no)+": "+status)
            else:
                print("Order "+str(no)+": "+status+"-"+str(res['error_code']))

    else:
        input("--------TRANSACTION FAILED-----------")


def responseForVolume(resp):
    if(resp['result']):
        print("---RESULT----")
        no = 0
        for res in resp['data']:
            no += 1
            status = "Failed"
            if res['result']:
                status = "Success"
                if(no == 1):
                    print("Order Sell: "+status)
                else:
                    print("Order Buy: "+status)
            else:
                if(no == 1):
                    print("Order Sell: "+status+"-"+str(res['error_code']))
                else:
                    print("Order Buy: "+status+"-"+str(res['error_code']))
    else:
        print("--------TRANSACTION FAILED-----------")


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
