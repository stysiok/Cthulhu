import json, random, os
from services.kraken import KrakenHelper, json2Assets

krakenHelper = KrakenHelper()
settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')

jsonObj = ''
with open(settingsPath) as json_file:
    jsonObj = json.load(json_file)
assets = json2Assets(jsonObj['ToBuy'])

assets = krakenHelper.updateCurrentPrices(assets)

budget = krakenHelper.getBudget()
print(f'Your current budget is {budget}€')
availableFunds = krakenHelper.hasEnough(budget, assets)
if not availableFunds:
    print('Not enough budget for next buy.')
    exit()

availableAssets = krakenHelper.getAffordable(budget, assets)
pickedAsset = random.choice(availableAssets)

buyFor = pickedAsset.getPriceForAsset()

budgetAfterOrder = budget - buyFor
enoughForNextBuy = krakenHelper.hasEnough(budgetAfterOrder, availableAssets)

amount = pickedAsset.min
if not enoughForNextBuy:
    amount = budget / pickedAsset.currentPrice

print(f'Picked {amount} {pickedAsset.leadingKey}')

krakenHelper.addOrder(pickedAsset.leadingKey, amount)
print('Successfully bought some crypto today!')