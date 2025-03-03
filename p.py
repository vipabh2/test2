from telethon import TelegramClient
from telethon.sessions import StringSession
import os

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        # التأكد من تسجيل الدخول
        me = await client.get_me()
        
        # استخراج session string
        session_string = client.session.save()

        print("✅ تم استخراج الكود بنجاح!")
        print(f"Session String: {session_string}")
    
# تشغيل البرنامج
import asyncio
asyncio.run(main())
