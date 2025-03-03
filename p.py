from telethon import TelegramClient
import os

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

async def main():
    client = TelegramClient('userbot_session', api_id, api_hash)
    await client.start()

    # التأكد من تسجيل الدخول
    me = await client.get_me()
    
    # استخراج session string
    session_string = client.session.save()

    print("✅ تم استخراج الكود بنجاح!")
    print(f"Session String: {session_string}")

# تشغيل البرنامج
import asyncio
asyncio.run(main())
