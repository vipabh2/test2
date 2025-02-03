import os
from telethon import TelegramClient, events

# جلب القيم من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء جلسة للبوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r"^ارسل\s+(.+?)\s+(@\w+)$"))
async def send_message_to_user(event):
    # استخراج النص واسم المستخدم من الرسالة
    message = event.pattern_match.group(1)  # النص المرسل
    username = event.pattern_match.group(2)  # اسم المستخدم

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

print("✅ Bot is running...")
ABH.run_until_disconnected()
