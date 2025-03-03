from telethon import TelegramClient, events
import os

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')

# تشغيل العميل
ABH = TelegramClient("userbot_session", api_id, api_hash)

# دالة لإرسال كود الجلسة (الذي يمكن استخدامه لاحقاً)
async def send_session_code():
    try:
        # الحصول على المعلومات الخاصة بالبوت
        me = await ABH.get_me()

        # استخراج اسم الجلسة (والذي يمكن استخدامه ككود)
        session_code = ABH.session.filename

        # إرسال كود الجلسة إلى الرسائل المحفوظة باستخدام معرف الحساب الشخصي
        await ABH.send_message(me.id, f"✅ تم إنشاء البوت بنجاح!\nكود الجلسة (Session Code): `{session_code}`")

    except Exception as e:
        print(f"Error sending session code: {e}")

# تنفيذ العملية عند الاتصال بنجاح
@ABH.on(events.NewMessage(pattern='/start'))
async def start(event):
    await send_session_code()

print("✅ البوت يعمل...")
ABH.run_until_disconnected()
