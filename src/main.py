import json, random, os
from src.services.kraken import getAssets, KrakenHelper

krakenHelper = KrakenHelper()
settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')

coins = ''
with open(settingsPath) as json_file:
    coins = json.load(json_file)["Coins"]
assets = getAssets(coins)

budget = krakenHelper.getBudget()
print(f'Your current budget is {budget}€')
availableFunds = krakenHelper.hasEnough(budget, assets)
if not availableFunds:
    print('Not enough budget for next buy.')
    exit()

availableAssets = krakenHelper.getAffordable(budget, assets)
pickedAsset = random.choice(availableAssets)

buyFor = pickedAsset.getPrice()
budgetAfterOrder = budget - buyFor

print(f'Picked {pickedAsset.crypto} with min: {pickedAsset.orderMin}')

krakenHelper.addOrder(pickedAsset.leadingKey, pickedAsset.orderMin)
print(f'Bought for {buyFor}, remaining budget {budgetAfterOrder}')
print('Successfully bought some crypto today!')