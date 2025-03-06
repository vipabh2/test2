from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.NewMessage)
async def _(event):
    await event.respond('اهلا')
    await event.sleep(3)
    await event.edit('اهلا كيف حالك')
    await event.respond('اهلا ABH')

ABH.run_until_disconnected()
