import krakenex
import json
from models.kraken import *

krakenApi = krakenex.API()

#Define which crypto to buy
jsonObj = ''
with open('settings.json') as json_file:
    jsonObj = json.load(json_file)
assets = json2Assets(jsonObj['ToBuy'])

tickerPairs = ','.join(map(lambda x: x.key, assets))
print(tickerPairs)
result = krakenApi.query_public(f'Ticker?pair={tickerPairs}')['result']

for a in assets:
    assetData = ''
    if a.key in result:
        assetData = result[a.key]
    elif a.altKey in result:
        assetData = result[a.altKey]
    else:
        raise Exception('key and alternative key are not part of the dictionary')
    currentPrice = assetData['c'][0]
    print(f'{a.key} = {currentPrice} in {a.currency}')
    a.currentPrice = currentPrice

balance = 100

#Auth to kraken
# krakenApi.load_key('kraken.key')

#Perform orders
