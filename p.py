import asyncio, os
from telethon import TelegramClient, events
from telethon.tl.types import ChatBannedRights

# تحميل API_ID و API_HASH و BOT_TOKEN من البيئة
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')

# إعداد عميل Telethon
client = TelegramClient('session_name', api_id, api_hash)
from telethon import events
from telethon.tl.types import UpdateChatParticipantAdmin, ChatBannedRights

@client.on(events.Raw)
async def handler(event):
    if isinstance(event, UpdateChatParticipantAdmin):
        user_id = event.user_id
        chat_id = event.chat_id
        rights = event.banned_rights

        if isinstance(rights, ChatBannedRights):
            if rights.send_messages:
                print(f"🚨 المستخدم {user_id} فقد صلاحية الإرسال في المجموعة {chat_id}")

client.start()
client.run_until_disconnected()
