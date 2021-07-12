from typing import Iterable, Sequence
import krakenex
import os

class Asset:
    currentPrice = None
    orderMin = None
    def __init__(self, crypto):
        self.currency = str.upper('eur')
        self.crypto = str.upper(crypto)
        self.key = self.crypto + self.currency
    
    def getPrice(self) -> float: 
        return self.currentPrice * self.orderMin



class KrakenHelper:
    krakenPath = 'kraken.key' if os.getenv('KRAKEN_KEY_PATH') == None else os.getenv('KRAKEN_KEY_PATH')
    api = krakenex.API()
    def __init__(self):
        self.api.load_key(self.krakenPath)

    def getBudget(self):
        return float(self.api.query_private('Balance')['result']['ZEUR'])

    def hasEnough(self, budget: float, assets: Iterable[Asset]) -> bool: 
        return budget > min(map(lambda a: a.getPrice(), assets))

    def getAffordable(self, budget: float, assets: Iterable[Asset]) -> Sequence[Asset]:
        return list(filter(lambda a: a.getPrice() < budget, assets))
    
    def checkAsset(self, assetName: str) -> bool:
        result = self.api.query_public(f'Assets?asset={assetName}')
        return 'result' in result
    
    def getMinBuys(self, assets: Iterable[Asset]):
        pairs = self.__assetsToPair(assets)
        result = self.api.query_public(f'AssetPairs?pair={pairs}')['result']
        return result

    def getCurrentPrices(self, assets: Iterable[Asset]):
        tickerPairs = self.__assetsToPair(assets)
        result = self.api.query_public(f'Ticker?pair={tickerPairs}')['result']
        return result
    
    def addOrder(self, key: str, amount: float) -> None:
        order = { 
            'pair': key,
            'volume': amount,
            'type': 'buy',
            'ordertype': 'market'
        }
        result = self.api.query_private("AddOrder", order)['result']['descr']['order']
        print(f'Result from Kraken: {result}')

    def __assetsToPair(self, assets: Iterable[Asset]) -> str:
        return ','.join(map(lambda x: x.key, assets))



def getAssets(cryptoNames: Iterable[str], helper: KrakenHelper) -> Sequence[Asset]:
    assets = list(map(lambda a: Asset(a), cryptoNames))
    currentPrices = helper.getCurrentPrices(assets)
    minOrders = helper.getMinBuys(assets)
    for a in assets:
        altKey = 'X' + a.crypto + 'Z' + a.currency
        if a.key not in currentPrices and altKey not in currentPrices:
            print(f'key for {a.crypto} not found. Looked for: ({a.key}, {altKey}).')
            continue
        elif altKey in currentPrices:
            a.key = altKey
        a.currentPrice = float(currentPrices[a.key]['c'][0])
        a.orderMin = float(minOrders[a.key]['ordermin'])
        print(f'{a.key} = {a.currentPrice} in {a.currency}')
    return list(filter(lambda a: a.currentPrice is not None or a.orderMin is not None, assets))