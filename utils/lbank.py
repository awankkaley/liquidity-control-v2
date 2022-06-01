import random
import string
import requests as req
import hashlib

from base64 import b64encode

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

api_key = "da2c345e-d354-415c-beae-9e55d9e1d415"
secret_key = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAKS49YniYbvKc04Z+9TnT/aFzJl19moJ5ubsMxPodEPN2z696jOzry6ovzPUnPN2Q08iJHwLLyttCw5HuJAahPvoucD3rutK8XlwQVKB1YrGKczzGauY/n5VC8W96nJq/ENFhXKpM8et0hJLJiqKf+Zm6KdjA2hloxGAN7QQO8ENAgMBAAECgYAbxVcYJQOHLo2cCENt1IWlsU8aPEoL/JliK0Y9P/6CA+3HuSsIBm4tdqOtsFW5siGM8Nun0hbkwmCPysWx/daXgItjcLaTIMjZTVsRv6EW06X1jJOfPSp/8WvB48sG45TfvsLTUSfRJ3LmVkQNKGkNaLzir7C22cl2r2gSUGtaYQJBANXd64TaCmyO82m+OUV00U8zZZWS8++IBfTO/JebfijeRz/DmWrvEI5/sCELQwbkFIcwWcpNaB/xyl/Q9P5at7kCQQDFLIKpWV2JGTCkGkEMTgoN6rjFRn7sut02JTcThRXi5VnAa7nHi3HW3pZQsk6tYOF4y0rTdaWTO8wlUaU5ddX1AkB26VAlavJ2z7jJp6nCU6R5a/NkifO10CS3rErHpP4tjQGCk6f+y/Oht59fkBpxf2lmjVyvXgCyGkdSpSVDM3+JAkEAltUj5xS73uLsOLz0wcr5GghS7GavNb0E+CSj60TFp1q3u+Esrx9XKH4CEx0z3qHcGaG6TeUTknwOAQZiFIC1+QJAM2vSjYQ7BtL2itb94s+nkhG3C+e8rnJdn51k8KsdVpMwcdpVFrfGvr1kphqA6u4GF4CGw66GEHXuwcYahC7HMg=="
rsa_private_key = "-----BEGIN RSA PRIVATE KEY-----\n"+secret_key+"\n-----END RSA PRIVATE KEY-----"

def buildRSASignV2(params, t):
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

def get_trading_depth():
    response = req.get(
        'https://api.lbkex.com/v2/depth.do?symbol=doge_usdt&size=3')
    lowest_sell = float(response.json()['data']['asks'][0][0])
    print('lowest_sell: ' + str(lowest_sell))
    highest_buy = float(response.json()['data']['bids'][0][0])
    print('highest_buy: ' + str(highest_buy))
    return [lowest_sell, highest_buy]


def get_time_stamp():
    response = req.get('https://api.lbkex.com/v2/timestamp.do')
    result = response.json()
    return result["data"]


def orderBatch(data):
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

    sign = buildRSASignV2(params=par, t=timestamp)

    del par["echostr"]
    del par["signature_method"]
    del par["timestamp"]

    par['sign'] = sign
    print('get response with header {h} and param {p} by {url}'.format(
        h=header, p=par, url=urlstr))
    res = req.post(url=urlstr, data=par, headers=header)

    if res.status_code == 200:
        resp = res.json()
        print(resp)
        return resp
    else:
        print(res.status_code)


def asset_information():
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

    sign = buildRSASignV2(params=par, t=timestamp)

    del par["echostr"]
    del par["signature_method"]
    del par["timestamp"]

    par['sign'] = sign
    print('get response with header {h} and param {p} by {url}'.format(
        h=header, p=par, url=urlstr))
    res = req.post(url=urlstr, data=par, headers=header)

    if res.status_code == 200:
        resp = res.json()
        print(resp)
        return resp
    else:
        print(res.status_code)
        
    