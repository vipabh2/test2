import os
from telethon import TelegramClient

# استبدل بـ API_ID و API_HASH الخاصة بك
api_id = os.getenv('API_ID')  # API_ID من تطبيق Telegram الخاص بك
api_hash = os.getenv('API_HASH')  # API_HASH من تطبيق Telegram الخاص بك

# أنشئ العميل باستخدام TelegramClient
client = TelegramClient('session_name', api_id, api_hash)

async def main():
    # ابدأ العميل وادخل رقم الهاتف
    await client.start()
    print("تم تسجيل الدخول بنجاح!")

with client:
    client.loop.run_until_complete(main())
