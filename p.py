import os
from telethon import TelegramClient, events

api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.NewMessage(pattern='/start'))
async def sendf(event):
    await event.reply(file="https://t.me/VIPABH/1242")
    return
ABH.run_until_disconnected()
