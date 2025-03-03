from telethon import TelegramClient, events
import os

# بيانات اليوزر
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

if not api_id or not api_hash:
    print("❌ تأكد من إعداد API_ID و API_HASH في البيئة.")
    exit()

# تشغيل العميل
client = TelegramClient("user_session", int(api_id), api_hash)

# دالة لإرسال كود السيشن إلى الرسائل المحفوظة
async def send_session_code():
    # الحصول على معلومات الحساب
    me = await client.get_me()

    # إرسال كود السيشن إلى الرسائل المحفوظة
    session_code = client.session.filename  # استخراج اسم السيشن
    await client.send_message('me', f"✅ تم إنشاء السيشن بنجاح!\nكود السيشن: `{session_code}`")

# تنفيذ العملية عند الاتصال بنجاح
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await send_session_code()

print("✅ اليوزر بوت يعمل...")
client.start()
client.run_until_disconnected()
