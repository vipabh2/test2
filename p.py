import requests, os, operator, asyncio, random, uuid, datetime 
from telethon import TelegramClient, events, Button
from telethon.errors import BadRequestError
from telethon.tl.functions.users import GetFullUserRequest
from telethon import TelegramClient, events

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  


# إنشاء الجلسة
client = TelegramClient("userbot", API_ID, API_HASH)

@client.on(events.NewMessage(pattern=r"\.مطور"))
async def developer_info(event):
    "رد بسيط عند كتابة .مطور"
    await event.reply("👨‍💻 هذا البوت من تطوير @Username")

@client.on(events.NewMessage(pattern=r"\.بايو"))
async def get_bio(event):
    "إظهار البايو الخاص بك"
    user = await event.client.get_me()
    await event.reply(f"📌 البايو الحالي: {user.bio}")

@client.on(events.NewMessage)
async def logger(event):
    "يسجل كل رسالة تستلمها"
    print(f"📩 رسالة من {event.sender_id}: {event.text}")

# تشغيل البوت
print("🚀 UserBot يعمل الآن!")
client.start()
client.run_until_disconnected()

