import google.generativeai as genai
from telethon import TelegramClient, events

API_ID = ايبي ايدي
API_HASH = "ايبي هاش"
BOT_TOKEN = "توكن بوتك"

GEMINI = "AIzaSyA5pzOpKVcMGm6Aek82KoB3Pk94dYg3LX4"
genai.configure(api_key=GEMINI)
model = genai.GenerativeModel("gemini-1.5-flash")

lMl10l = TelegramClient("aljoker_b", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@lMl10l.on(events.NewMessage)
async def ai_aljoker(event):
    if event.text and not event.out:
        try:
            joker = model.generate_content(event.text.strip())
            await event.reply(f"**{joker.text}**")
        except Exception as e:
            await event.reply(f"صار خطأ: {e}")
