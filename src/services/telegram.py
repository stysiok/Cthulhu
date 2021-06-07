import os
import telebot, json

telegramKeyPath = 'telegram.key' if os.getenv('TELEGRAM_KEY_PATH') == None else os.getenv('TELEGRAM_KEY_PATH')

token = ''
with open(telegramKeyPath) as telegramFile:
    token = telegramFile.read()

bot = telebot.TeleBot(token, parse_mode=None)

@bot.message_handler(commands=['all'])
def getAllCoins(message):
    settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')
    coins = ''
    with open(settingsPath) as json_file:
        coins = json.load(json_file)["Coins"]
    bot.reply_to(message, f'List of all current coins to be bought: {", ".join(coins)}')
    
@bot.message_handler(commands=['add'])
def addNewCoin(message):
    bot.reply_to(message, '123321')
