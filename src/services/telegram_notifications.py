import datetime, os, json
import telebot
from services.kraken import Asset


telegramKeyPath = 'telegram.key' if os.getenv('TELEGRAM_KEY_PATH') == None else os.getenv('TELEGRAM_KEY_PATH')
settingsPath = 'settings.json' if os.getenv('SETTINGS_PATH') == None else os.getenv('SETTINGS_PATH')

token = ''
with open(telegramKeyPath) as telegramFile:
    token = telegramFile.read()

chatId = ''
with open(settingsPath) as json_file:
    chatId = json.load(json_file)['TelegramChatId']

bot = telebot.TeleBot(token, parse_mode=None)


def boughtCoinNotification(asset: Asset):
    roundedCurrentPrice = "{:.2f}".format(asset.currentPrice)
    message = f'''🚀 🚀 🚀 
{datetime.date.today().strftime("%d-%B-%Y")}
Picked {asset.crypto} 
{asset.orderMin} for {roundedCurrentPrice}€
Spend {asset.getPrice()}€'''
    bot.send_message(chatId, message)