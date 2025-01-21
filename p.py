from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.EditedMessage)
async def echo(event):
    await event.reply("ها ههههه سالمين")
    
ABH.run_until_disconnected()
