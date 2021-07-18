import os, json
import telebot
from telebot import apihelper
from kraken import KrakenHelper

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
def addNewCoins(message):
    coinsToAdd = set(message.text[5:].split(','))
    file = ''
    coins = []
    with open(settingsPath) as json_file:
        file = json.load(json_file)
        coins = file["Coins"]
    alreadyAddedCoins = set(filter(lambda c: c in coins, coinsToAdd))
    newCoins = coinsToAdd - alreadyAddedCoins
    validCoins = set(filter(lambda c: helper.checkAsset(c), newCoins))
    invalidCoins = newCoins - validCoins
    coins += validCoins
    file['Coins'] = coins
    with open(settingsPath, 'w') as json_file:
        json.dump(file, json_file)
    reply = 'Your message has been processed with given result:'
    reply += f'\nAdded: {",".join(map(lambda x: x, validCoins))} ✅' if validCoins else ''
    reply += f'\nInvalid: {",".join(map(lambda x: x, invalidCoins))} ❌' if invalidCoins else ''
    reply += f'\nExisting: {",".join(map(lambda x: x, alreadyAddedCoins))} ❓' if alreadyAddedCoins else ''
    bot.reply_to(message, reply)

@bot.message_handler(commands=['remove'])
def removeCoins(message):
    coinsToRemove = set(message.text[8:].split(','))
    file = ''
    coins = []
    with open(settingsPath) as json_file:
        file = json.load(json_file)
        coins = file["Coins"]
    coinsInSettings = set(filter(lambda c: c in coins, coinsToRemove))
    validCoins = set(coins) - coinsInSettings
    invalidCoins = coinsToRemove - coinsInSettings
    file['Coins'] = list(validCoins)
    with open(settingsPath, 'w') as json_file:
        json.dump(file, json_file)
    reply = 'Your message has been processed with given result:'
    reply += f'\nRemoved: {",".join(map(lambda x: x, coinsInSettings))} ✅' if coinsInSettings else ''
    reply += f'\nInvalid: {",".join(map(lambda x: x, invalidCoins))} ❌' if invalidCoins else ''
    bot.reply_to(message, reply)

bot.polling()
