import datetime
from telethon import events, TelegramClient
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='^/satrt$'))
async def cunt(event):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 3, 1)
    days_difference = (t2 - t.date()).days
    
    if days_difference < 0:
        await event.reply("The date has passed!")
    else:
        await event.reply(f"Days remaining: {days_difference} days")
        
print("Bot is running...")
ABH.run_until_disconnected()
