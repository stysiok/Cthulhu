import json

class Asset:
    currentPrice = None
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

def getBudget():
    return 100 #to be implemented

def hasEnough(budget, assets) -> bool:
    return budget > min(map(lambda a: a.getMinPrice(), filter(lambda a: a is not None, assets)))

def getAffordable(budget, assets):
    return list(filter(lambda a: a.getMinPrice() < budget, assets))