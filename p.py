import os
from telethon import TelegramClient, events

# الحصول على المتغيرات من البيئة
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء عميل Telethon
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@client.on(events.chataction)
async def handle_chat_action(event):
    if event.user_restricted is not None:
        await client.send_message(event.user_restricted, "تم حظرك من البوت")

client.run_until_disconnected()
