from telethon import TelegramClient, events
import os, random 

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='/start$'))
async def start(event):
    rl = random.randint(2, 273)
    url = f"https://t.me/IUABH/{rl}"
    await ABH.send_file(event.chat_id, url, caption="📹")

ABH.run_until_disconnected()
