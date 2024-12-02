import os
import telebot

# استدعاء التوكن من المتغير البيئي
bot_token = os.getenv("BOT_TOKEN")  # BOT_TOKEN هو اسم الـ Secret الذي أضفته في GitHub
if not bot_token:
    raise ValueError("Missing BOT_TOKEN environment variable")

bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: message.text in ['المزيد'])
def more(message):
    bot.reply_to(message, """
    ~ الالعاب المتوفره ~
\n •الكت تويت والأمر الخاص بيها `كتويت`
\n •الأرقام ، احزر الرقم المطلوب والأمر الخاص بيها /num 
\n •امر الميمز ، `ميم` او `ميمز` يرسلك صورة ميم 
\n \n استمتع ❤️
""", parse_mode='Markdown')
