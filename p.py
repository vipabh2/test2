from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.UserUpdate)
async def handler(event):
    # مراقبة الحظر أو رفع الحظر
    if event.is_blocked:
        print(f"تم حظر عضو: {event.user_id}")
    else:
        print(f"تم رفع الحظر عن عضو: {event.user_id}")

client.start()
client.run_until_disconnected()
