import krakenex
import os

class Asset:
    currentPrice = None
    key = None
    ordermin = None
    def __init__(self, crypto):
        self.currency = str.upper('eur')
        self.crypto = str.upper(crypto)
    
    def getPriceForMinAsset(self):
        return self.currentPrice * self.min

    def getAssets(cryptoNames):
        krakenHelper = KrakenHelper()
        assets = list(map(lambda a: Asset(a), cryptoNames))
        currentPrices = krakenHelper.getCurrentPrices(assets)
        minOrders = krakenHelper.getMinBuys(assets)
        for a in assets:
            key = a.crypto + a.currency
            altKey = 'X' + a.crypto + 'Z' + a.currency
            if key in currentPrices:
                a.key = key
            elif altKey in currentPrices:
                a.key = altKey
            else:
                print(f'key for {a.crypto} not found. Looked for: ({key}, {altKey}).')
                break
            a.currentPrice = float(currentPrices[a.key]['c'][0])
            a.ordermin = float(minOrders[a.key]['ordermin'])
            print(f'{a.key} = {a.currentPrice} in {a.currency}')
        return assets



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
    
    def getMinBuys(self, assets):
        pairs = self.__assetsToPair(assets)
        result = self.api.query_public(f'AssetPairs?pair={pairs}')['result']
        return result

    def getCurrentPrices(self, assets):
        tickerPairs = self.__assetsToPair(assets)
        result = self.api.query_public(f'Ticker?pair={tickerPairs}')['result']
        return result
    
    def addOrder(self, key, amount):
        order = { 
            'pair': key,
            'volume': amount,
            'type': 'buy',
            'ordertype': 'market'
        }
        result = self.api.query_private("AddOrder", order)['result']['descr']['order']
        print(f'Result from Kraken: {result}')

    def __assetsToPair(self, assets):
        return ','.join(map(lambda x: x.key, assets))
