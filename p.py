from telethon import TelegramClient, events
import os

# بيانات البوت
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تشغيل العميل
ABH = TelegramClient("bot_session", api_id, api_hash).start(bot_token=bot_token)

# دالة لإرسال كود السيشن إلى الرسائل المحفوظة
async def send_session_code():
    # الحصول على المعلومات الخاصة بالبوت
    me = await ABH.get_me()

    # إرسال كود السيشن إلى الرسائل المحفوظة
    session_code = ABH.session.filename  # استخراج اسم السيشن
    # إرسال رسالة إلى حسابك الشخصي أو الرسائل المحفوظة
    await ABH.send_message(me.id, f"✅ تم إنشاء البوت بنجاح!\nكود السيشن: `{session_code}`")

# تنفيذ العملية عند الاتصال بنجاح
@ABH.on(events.NewMessage(pattern='/start'))
async def start(event):
    await send_session_code()

print("✅ البوت يعمل...")
ABH.run_until_disconnected()
