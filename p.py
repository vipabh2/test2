import os
from telethon import TelegramClient, events

# جلب القيم من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء جلسة للبوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern="ارسل"))
async def send_message_to_user(event):
    # استخراج النص بعد كلمة "ارسل"
    query = event.text.strip()
    parts = query.split(' ', 2)  # نقوم بتقسيم النص إلى 3 أجزاء: الامر، النص، واسم المستخدم

    if len(parts) >= 3:
        message = parts[1]  # النص المرسل
        username = parts[2]  # اسم المستخدم

        # التأكد من أن اسم المستخدم يبدأ بـ @، وإذا لم يكن يبدأ بـ @، نضيفه
        if not username.startswith('@'):
            username = f'@{username}'

        try:
            # جلب معلومات المستلم
            reciver = await ABH.get_entity(username)
            reciver_id = reciver.id  # ID المستخدم المستلم
            sender_id = event.sender_id  # معرف المرسل

            # إرسال الرسالة إلى المستخدم المستهدف
            await ABH.send_message(
                reciver_id,
                f"📩 **لديك رسالة سرية من شخص مجهول!**\n"
                f"💬 **الرسالة:** {message}"
            )

            # إرسال تأكيد للمرسل في محادثة البوت
            await ABH.send_message(
                sender_id,
                f"✅ **تم إرسال الرسالة إلى {username} بنجاح!**\n"
                f"💬 **الرسالة:** {message}"
            )

        except Exception as e:
            await event.reply("❌ **حدث خطأ أثناء محاولة إرسال الرسالة. تأكد من صحة اسم المستخدم.**")
    else:
        await event.reply("❌ **الصيغة غير صحيحة. يرجى استخدام الصيغة: ارسل [نص الرسالة] @username**")

print("✅ Bot is running...")
ABH.run_until_disconnected()
