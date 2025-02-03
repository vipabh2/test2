import os
from telethon import TelegramClient, events, Button

# جلب القيم من المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء جلسة للبوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text.strip()

    if query:
        parts = query.split(' ')
        if parts[0] == 'تيل' and len(parts) >= 3:
            message = ' '.join(parts[1:-1])  # استخراج الرسالة
            username = parts[-1]  # استخراج اسم المستخدم

            if not username.startswith('@'):
                username = f'@{username}'

            try:
                reciver = await ABH.get_entity(username)  # جلب معلومات المستلم
                reciver_id = reciver.id  # ID المستخدم المستلم

                result = builder.article(
                    title='📩 إرسال رسالة سرية',
                    description=f'اضغط لإرسال رسالة إلى {username}',
                    text=f"🔹 اضغط على الزر لإرسال رسالة سرية إلى {username} 👇",
                    buttons=[
                        Button.inline(f"📩 إرسال إلى {username}", data=f'send|{event.query.user_id}|{reciver_id}|{message}')
                    ]
                )

            except Exception as e:
                result = builder.article(
                    title='❌ خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                )
        else:
            return
        
        # ✅ تصحيح الخطأ بإعادة تفعيل إرسال الرد على الإنلاين
        await event.answer([result])

@ABH.on(events.CallbackQuery)
async def callback_handler(event):
    """ عند الضغط على زر إرسال الرسالة """
    data = event.data.decode().split('|')

    if data[0] == 'send':
        sender_id = int(data[1])  # معرف المرسل
        reciver_id = int(data[2])  # معرف المستلم
        secret_message = data[3]  # محتوى الرسالة

        if event.query.user_id != sender_id:
            await event.answer("❌ ليس لديك صلاحية لإرسال هذه الرسالة!", alert=True)
            return

        # إرسال الرسالة في محادثة البوت للمرسل
        await ABH.send_message(
            sender_id,
            f"✅ **تم إرسال الرسالة إلى المستخدم المطلوب!**\n"
            f"💬 **الرسالة:** {secret_message}"
        )

        # إرسال الرسالة إلى المستخدم المستهدف
        await ABH.send_message(
            reciver_id,
            f"📩 **لديك رسالة سرية من شخص مجهول!**\n"
            f"💬 **الرسالة:** {secret_message}"
        )

        await event.answer("✅ تم إرسال الرسالة!", alert=True)

print("✅ Bot is running...")
ABH.run_until_disconnected()
