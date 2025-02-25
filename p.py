from telethon import TelegramClient, events, Button
import random
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

choices = ["حجره", "ورقة", "مقص"]

@ABH.on(events.NewMessage(pattern="حجرة|/rock"))
async def game_handler(event):
    button = [
        [Button.inline("🪨", b"rock"), Button.inline("✂️", b"cuter"), Button.inline("📜", b"paper")]
    ]
    await event.respond("اهلا صديقي، اختر أحد الاختيارات:", buttons=button)

ABH.run_until_disconnected()
