import json

class Asset:
    currentPrice = -1
    def __init__(self, crypto, currency, min):
        self.currency = str.upper(currency)
        self.crypto = str.upper(crypto)
        self.key = self.crypto + self.currency
        self.altKey = 'X' + self.crypto + 'Z' + self.currency
        self.min = min
    
    def getMinPrice(self):
        return self.currentPrice * self.min

def json2Assets(jsonObj): 
    arr = []
    for v in jsonObj:
        asset = Asset(v['crypto'], v['currency'], v['min'])
        arr.append(asset)
    return arr