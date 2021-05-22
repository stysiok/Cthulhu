from typing import Sequence
import krakenex
import os

class Asset:
    currentPrice = None
    orderMin = None
    def __init__(self, crypto):
        self.currency = str.upper('eur')
        self.crypto = str.upper(crypto)
        self.key = self.crypto + self.currency
    
    def getPrice(self):
        return self.currentPrice * self.orderMin



def getAssets(cryptoNames):
    krakenHelper = KrakenHelper()
    assets = list(map(lambda a: Asset(a), cryptoNames))
    currentPrices = krakenHelper.getCurrentPrices(assets)
    minOrders = krakenHelper.getMinBuys(assets)
    for a in assets:
        altKey = 'X' + a.crypto + 'Z' + a.currency
        if a.key in currentPrices:
            break
        elif altKey in currentPrices:
            a.key = altKey
        else:
            print(f'key for {a.crypto} not found. Looked for: ({key}, {altKey}).')
            break
        a.currentPrice = float(currentPrices[a.key]['c'][0])
        a.orderMin = float(minOrders[a.key]['ordermin'])
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
        return budget > min(map(lambda a: a.getPrice(), filter(lambda a: a is not None, assets)))

    def getAffordable(self, budget, assets) -> Sequence[Asset]:
        return list(filter(lambda a: a.getPrice() < budget, assets))
    
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
