from telethon import TelegramClient, events
from hijri_converter import Gregorian
import os, datetime, time

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', int(api_id), api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r'\bاحس\b'))
async def start_handler(event):
    t = datetime.datetime.now().date()
    hd = Gregorian(t.year, t.month, t.day).to_hijri()
    hd_str = f"{hd.day} {hd.month_name('ar')} {hd.year} هـ"    
    await event.reply(f"{hd_str}")


print("Bot is running...")
ABH.run_until_disconnected()
