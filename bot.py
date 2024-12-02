import os
import telebot

# استدعاء التوكن من المتغير البيئي
bot_token = os.getenv("BOT_TOKEN")

if not bot_token:
    raise ValueError("Missing BOT_TOKEN environment variable")

bot = telebot.TeleBot(bot_token)

# مثال لرسالة مبدئية أو تفاعل مع البوت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to the bot!")

bot.polling()
