from telethon import TelegramClient, events
import os

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# تشغيل العميل
ABH = TelegramClient("userbot_session", api_id, api_hash)

async def main():
    async with TelegramClient('userbot_session', api_id, api_hash) as client:
        # التأكد من تسجيل الدخول
        me = await client.get_me()
        
        # استخراج session string
        session_string = await client.session.save()

        print("✅ تم استخراج الكود بنجاح!")
        print(f"Session String: {session_string}")
    
# تشغيل البرنامج
import asyncio
asyncio.run(main())
