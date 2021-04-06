import json, krakenex

class Asset:
    currentPrice = None
    def __init__(self, crypto, currency, min):
        self.currency = str.upper(currency)
        self.crypto = str.upper(crypto)
        self.key = self.crypto + self.currency
        self.altKey = 'X' + self.crypto + 'Z' + self.currency
        self.min = min
    
    def getPriceForAsset(self):
        return self.currentPrice * self.min

def json2Assets(jsonObj): 
    arr = []
    for v in jsonObj:
        asset = Asset(v['crypto'], v['currency'], v['min'])
        arr.append(asset)
    return arr

class KrakenHelper:
    api = krakenex.API()
    def __init__(self):
        self.api.load_key('kraken.key')

    def getBudget(self):
        return self.api.query_private('Balance')['result']['ZEUR']

    def hasEnough(self, budget, assets):
        return budget > min(map(lambda a: a.getPriceForAsset(), filter(lambda a: a is not None, assets)))

    def getAffordable(self, budget, assets):
        return list(filter(lambda a: a.getPriceForAsset() < budget, assets))

    def updateCurrentPrices(self, assets):
        tickerPairs = ','.join(map(lambda x: x.key, assets))
        result = self.api.query_public(f'Ticker?pair={tickerPairs}')['result']
        for a in assets:
            assetData = ''
            if a.key in result:
                assetData = result[a.key]
            elif a.altKey in result:
                assetData = result[a.altKey]
            else:
                break
            currentPrice = assetData['c'][0]
            print(f'{a.key} = {currentPrice} in {a.currency}')
            a.currentPrice = float(currentPrice)
        return assets
    
    def makeOrder(self, krakenOrder):
        result = self.api.query_private("MakeOrder", krakenOrder)

class KrakenOrder:
    def __init__(self, pair, amount):
        self.pair = pair
        self.amount = amount
        self.type = 'buy'
        self.order = 'market'
