import krakenex
import json, random
from services.kraken import KrakenHelper, json2Assets, KrakenOrder

krakenHelper = KrakenHelper()

jsonObj = ''
with open('settings.json') as json_file:
    jsonObj = json.load(json_file)
assets = json2Assets(jsonObj['ToBuy'])

assets = krakenHelper.updateCurrentPrices(assets)

budget = krakenHelper.getBudget()
availableFunds = krakenHelper.hasEnough(budget, assets)
if not availableFunds:
    raise Exception('Not enough budget for next buy $___$')

availableAssets = krakenHelper.getAffordable(budget, assets)
pickedAsset = random.choice(availableAssets)
order = KrakenOrder(pickedAsset.pair, pickedAsset.min)

buyFor = pickedAsset.getPriceForAsset()

budgetAfterOrder = budget - pickedAsset.getPriceForAsset()
enoughForNextBuy = krakenHelper.hasEnough(budgetAfterOrder, availableAssets)

if not enoughForNextBuy:
    order.amount = budget / pickedAsset.currentPrice

# krakenHelper.makeOrder(order)
