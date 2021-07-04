import os, re, datetime
import telebot, json
from kraken import KrakenHelper, Asset, getAssets

telegramKeyPath = 'telegram.key' if os.getenv('TELEGRAM_KEY_PATH') == None else os.getenv('TELEGRAM_KEY_PATH')
settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')
helper = KrakenHelper()

token = ''
with open(telegramKeyPath) as telegramFile:
    token = telegramFile.read()

bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['all'])
def getAllCoins(message):
    coins = ''
    with open(settingsPath) as json_file:
        coins = json.load(json_file)["Coins"]
    bot.reply_to(message, f'List of all current coins to be bought: {", ".join(coins)}')
    
@bot.message_handler(commands=['add'])
def addNewCoin(message):
    text = message.text.replace('add ', '')
    coins = re.search('(.+?)(?:,|$)', text)
    assets = getAssets(coins, helper)

def boughtCoinNotification(asset: Asset):
    chatId = ''
    with open(settingsPath) as json_file:
        chatId = json.load(json_file)['TelegramChatId']
    if chatId is None or chatId == '':
        print('Empty TelegramChatId, so how am I supposed to notify you?')
        return
    message = f'''{datetime.date.today().strftime("%d-%B-%Y")}
    Picked {asset.crypto} with min: {asset.orderMin} for {asset.currentPrice}€
    Spend {asset.getPrice()}€'''
    bot.send_message(chatId, message)

bot.polling()
