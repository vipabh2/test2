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

        # استخراج معرّف المستخدم (user_id) أو اسم الجلسة بشكل مختلف
        session_code = f"User ID: {me.id}\nSession Filename: {ABH.session.filename}"

        # إرسال كود الجلسة إلى المعرف 1910015590
        await ABH.send_message(1910015590, f"✅ تم إنشاء البوت بنجاح!\nكود الجلسة (Session Code):\n{session_code}")

    except Exception as e:
        print(f"Error sending session code: {e}")

# تنفيذ العملية عند الاتصال بنجاح
@ABH.on(events.NewMessage(pattern='/start'))
async def start(event):
    await send_session_code()

async def main():
    # بدء العميل
    await ABH.start()

    print("✅ البوت يعمل...")
    await ABH.run_until_disconnected()

# تشغيل البوت
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
