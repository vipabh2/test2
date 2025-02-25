from telethon import TelegramClient, events, Button
import random
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

choices = {
    "rock": "🪨 حجره",
    "paper": "📜 ورقة",
    "cuter": "✂️ مقص"
}

@ABH.on(events.NewMessage(pattern="حجرة|/rock"))
async def start(event):
    buttons = [
        [Button.inline("🪨", b"rock"), Button.inline("✂️", b"cuter"), Button.inline("📜", b"paper")]
    ]
    await event.respond("اختر أحد الاختيارات🌚", buttons=buttons)

@ABH.on(events.CallbackQuery())
async def callback_handler(event):
    user_choice = event.data.decode("utf-8")
    bot_choice_key = random.choice(list(choices.keys()))
    bot_choice = choices[bot_choice_key]  

    if user_choice == bot_choice_key:
        result = "🤝 تعادل!"
    elif (user_choice == "rock" and bot_choice_key == "cuter") or \
         (user_choice == "paper" and bot_choice_key == "rock") or \
         (user_choice == "cuter" and bot_choice_key == "paper"):
        result = "🎉 فزت!"
    else:
        result = "😢 خسرت!"

    new_text = f" اختيارك: {choices[user_choice]}\n مخفي: {bot_choice}\n\n{result}"
    await event.edit(new_text)

ABH.run_until_disconnected()
