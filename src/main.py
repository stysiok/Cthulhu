import krakenex
import json
from models.kraken import *

krakenApi = krakenex.API()

#Define which crypto to buy
jsonObj = ''
with open('settings.json') as json_file:
    jsonObj = json.load(json_file)
cryptos = json2Cryptos(jsonObj['ToBuy'])

buyCurrency = 'EUR'
pairs = map(lambda x: f'{x.currency}{buyCurrency}', cryptos)
tickerPairs = ','.join(pairs)
print(tickerPairs)
result = krakenApi.query_public(f'Ticker?pair={tickerPairs}', )
print(result)
#Auth to kraken
krakenApi.load_key('kraken.key')

#Perform orders

