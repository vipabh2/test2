from telethon import TelegramClient, events, Button
import random
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

choices = ["حجره", "ورقة", "مقص"]

@ABH.on(events.NewMessage(pattern="حجرة|/rock"))
async def start(event):
    buttons = [
        [Button.inline("🪨", b"rock"), Button.inline("✂️", b"cuter"), Button.inline("📜", b"paper")]
    ]
    await event.respond("اهلا صديقي، اختر أحد الاختيارات:", buttons=buttons)

@ABH.on(events.CallbackQuery())
async def callback_handler(event):
    user_choice = event.data.decode("utf-8")  # تحويل البيانات من bytes إلى string
    bot_choice = random.choice(choices)  # اختيار عشوائي من الروبوت

    # رسالة النتيجة
    result = f"📌 اختيارك: {user_choice}\n🤖 اختياري: {bot_choice}\n\n"

    if user_choice == "rock":
        if bot_choice == "حجره":
            result += "🤝 تعادل!"
        elif bot_choice == "ورقة":
            result += "😢 خسرت!"
        else:
            result += "🎉 فزت!"
    elif user_choice == "paper":
        if bot_choice == "ورقة":
            result += "🤝 تعادل!"
        elif bot_choice == "مقص":
            result += "😢 خسرت!"
        else:
            result += "🎉 فزت!"
    elif user_choice == "cuter":
        if bot_choice == "مقص":
            result += "🤝 تعادل!"
        elif bot_choice == "حجره":
            result += "😢 خسرت!"
        else:
            result += "🎉 فزت!"

    await event.answer(result, alert=True)

ABH.run_until_disconnected()
