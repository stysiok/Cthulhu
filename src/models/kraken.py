import json

class Crypto(object):
    def __init__(self, currency, min):
        self.currency = str.upper(currency)
        self.min = min

def json2Cryptos(jsonObj): 
    arr = []
    for v in jsonObj:
        crypto = Crypto(v['currency'], v['min'])
        arr.append(crypto)
    return arr