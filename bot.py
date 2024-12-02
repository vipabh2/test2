import os
import telebot

# الحصول على التوكن من المتغير البيئي
bot_token = os.getenv("BOT_TOKEN")

# التحقق من التوكن
if not bot_token:
    raise ValueError("Missing BOT_TOKEN environment variable")
else:
    print("Bot token received")

try:
    # إنشاء البوت
    bot = telebot.TeleBot(bot_token)
    print("Bot initialized successfully.")
except Exception as e:
    print(f"Error initializing bot: {e}")

# مثال لإرسال رسالة عند استقبال الأمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello, welcome to the bot!")

# بدء البوت
print("Starting bot polling...")
bot.polling()
