import google.generativeai as genai
from telethon import TelegramClient, events
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)


GEMINI = "AIzaSyA5pzOpKVcMGm6Aek82KoB3Pk94dYg3LX4"
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel("gemini-1.5-flash")

@ABH.on(events.NewMessage)
async def ai_aljoker(event):
    if event.text and not event.out:
        try:
            joker = model.generate_content(event.text.strip())
            await event.reply(f"**{joker.text}**")
        except Exception as e:
            await event.reply(f"صار خطأ: {e}")
ABH.run_until_disconnected()
