import hashlib
import requests


def get_signature(api_key, query, secret_key):
    sign_param = 'api_key=' + api_key + '&' + query + '&secret_key=' + secret_key
    # print('sign_param: ' + sign_param)
    sign = hashlib.md5(sign_param.encode('utf-8')).hexdigest().upper()
    # print('sign: ' + sign)
    return sign


def get_signature_full_query(query):
    # print('query: ' + query)
    sign = hashlib.md5(query.encode('utf-8')).hexdigest().upper()
    # print('sign: ' + sign)
    return sign


def set_limit_order(api_key, secret_key, market, side, amount, price):
    query = 'amount='+str(amount)+'&api_key='+api_key+'&isfee=0&market='+market+'&price='+str(price)+'&side='+str(side)+'&secret_key='+secret_key
    request_params = {
        'api_key': api_key,
        # 'sign': get_signature_full_query(urllib.parse.urlencode(query)),
        'sign': get_signature_full_query(query),
        'market': market,
        'side': side,
        'amount': amount,
        'price': price,
        'isfee': 0
    }
    response = requests.post('https://api.hotbit.io/v2/p2/order.put_limit', data=request_params)
    print(response.json())

