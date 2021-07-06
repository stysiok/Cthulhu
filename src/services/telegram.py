import os, datetime, json
import telebot
from telebot import apihelper
from kraken import KrakenHelper, Asset, getAssets

telegramKeyPath = 'telegram.key' if os.getenv('TELEGRAM_KEY_PATH') == None else os.getenv('TELEGRAM_KEY_PATH')
settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')

chatId = ''
with open(settingsPath) as json_file:
    chatId = json.load(json_file)['TelegramChatId']

helper = KrakenHelper()

token = ''
with open(telegramKeyPath) as telegramFile:
    token = telegramFile.read()

apihelper.ENABLE_MIDDLEWARE = True
bot = telebot.TeleBot(token, parse_mode=None)


@bot.middleware_handler(update_types=['message'])
def authorizeCommand(bot_instance, message):
    if chatId != message.chat.id:
        message.text = '/error'

@bot.message_handler(commands=['error'])
def error(message):
    bot.send_message(chat_id=message.chat.id, text='Unauthorized access')

@bot.message_handler(commands=['all'])
def getAllCoins(message):
    coins = ''
    with open(settingsPath) as json_file:
        coins = json.load(json_file)["Coins"]
    bot.reply_to(message, f'List of all current coins to be bought: {", ".join(coins)}')
    
@bot.message_handler(commands=['add'])
def addNewCoin(message):
    coinsToAdd = set(message.text[5:].split(','))
    coins = []
    with open(settingsPath) as json_file:
        coins = json.load(json_file)["Coins"]
    alreadyAddedCoins = set(filter(lambda c: c in coins, coinsToAdd))
    newCoins = set(coinsToAdd - alreadyAddedCoins)
    validCoins = set(filter(lambda c: helper.checkAsset(c), newCoins))
    invalidCoins = list(newCoins - validCoins)
    assets = getAssets(validCoins, helper)
    pass

    
    # bot.reply_to(message, )

def boughtCoinNotification(asset: Asset):
    message = f'''🚀 🚀 🚀 
    {datetime.date.today().strftime("%d-%B-%Y")}
    Picked {asset.crypto} with min: {asset.orderMin} for {asset.currentPrice}€
    Spend {asset.getPrice()}€'''
    bot.send_message(chatId, message)

bot.polling()
