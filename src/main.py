import json, random, os
from services.kraken import KrakenHelper, json2Assets, KrakenOrder

krakenHelper = KrakenHelper()
settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')

jsonObj = ''
with open(settingsPath) as json_file:
    jsonObj = json.load(json_file)
assets = json2Assets(jsonObj['ToBuy'])

assets = krakenHelper.updateCurrentPrices(assets)

budget = krakenHelper.getBudget()
availableFunds = krakenHelper.hasEnough(budget, assets)
if not availableFunds:
    print('Not enough budget for next buy $___$')
    exit()

availableAssets = krakenHelper.getAffordable(budget, assets)
pickedAsset = random.choice(availableAssets)
order = KrakenOrder(pickedAsset.altKey, pickedAsset.min)

buyFor = pickedAsset.getPriceForAsset()

budgetAfterOrder = budget - pickedAsset.getPriceForAsset()
enoughForNextBuy = krakenHelper.hasEnough(budgetAfterOrder, availableAssets)

if not enoughForNextBuy:
    order.amount = budget / pickedAsset.currentPrice

krakenHelper.addOrder(order.pair, order.amount)
print('done!')