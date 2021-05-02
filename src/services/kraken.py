import krakenex
import json, os

class Asset:
    currentPrice = None
    def __init__(self, crypto, min):
        self.currency = str.upper('eur')
        self.crypto = str.upper(crypto)
        self.key = self.crypto + self.currency
        self.altKey = 'X' + self.crypto + 'Z' + self.currency
        self.leadingKey = ''
        self.min = min
    
    def getPriceForAsset(self):
        return self.currentPrice * self.min

def json2Assets(jsonObj): 
    arr = []
    for v in jsonObj:
        asset = Asset(v['crypto'], v['min'])
        arr.append(asset)
    return arr

class KrakenHelper:
    krakenPath = 'kraken.key' if os.getenv('KRAKEN_KEY_PATH') == None else os.getenv('KRAKEN_KEY_PATH')
    api = krakenex.API()
    def __init__(self):
        self.api.load_key(self.krakenPath)

    def getBudget(self):
        return float(self.api.query_private('Balance')['result']['ZEUR'])

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
                a.leadingKey = a.key
            elif a.altKey in result:
                assetData = result[a.altKey]
                a.leadingKey = a.altKey
            else:
                print(f'key for {a.crypto} not found. Looked for: ({a.key}, {a.altKey}).')
                break
            currentPrice = assetData['c'][0]
            print(f'{a.leadingKey} = {currentPrice} in {a.currency}')
            a.currentPrice = float(currentPrice)
        return assets
    
    def addOrder(self, key, amount):
        order = { 
            'pair': key,
            'volume': amount,
            'type': 'buy',
            'ordertype': 'market'
        }
        result = self.api.query_private("AddOrder", order)['result']['descr']['order']
        print(f'Result from Kraken: {result}')

