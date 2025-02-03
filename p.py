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
            username = parts[-1]  # استخراج اسم المستلم

            if not username.startswith('@'):
                username = f'@{username}'

            try:
                reciver = await ABH.get_entity(username)  # جلب معلومات المستلم
                reciver_id = reciver.id  # ID المستخدم

                # إرسال الرسالة في محادثة البوت
                bot_message = await event.client.send_message(
                    event.query.user_id,  # يتم إرسالها للشخص الذي استدعى الإنلاين
                    f"📩 **تم إرسال رسالة سرية إلى {username}!**\n"
                    f"💬 **الرسالة:** {message}"
                )

                # إرسال الرسالة إلى المستخدم المستهدف @k_4x1
                await event.client.send_message(
                    reciver, 
                    f"📩 **لديك رسالة سرية من شخص مجهول!**\n"
                    f"💬 **الرسالة:** {message}"
                )

                # إرسال زر تأكيد داخل الإنلاين
                result = builder.article(
                    title='📩 تم إرسال الرسالة السرية!',
                    description=f'تم إرسال رسالة إلى {username}',
                    text=f"✅ **تم إرسال الرسالة إلى {username} بنجاح!**",
                    buttons=[Button.inline("🗑 حذف الرسالة", data=f'delete|{bot_message.id}')]
                )

            except Exception as e:
                result = builder.article(
                    title='❌ خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                )
        else:
            return
        await event.answer([result])

@ABH.on(events.CallbackQuery)
async def callback_handler(event):
    """ معالجة الضغط على زر حذف الرسالة """
    data = event.data.decode().split('|')

    if data[0] == 'delete':
        message_id = int(data[1])  # ID الرسالة في محادثة البوت
        try:
            await event.client.delete_messages(event.query.user_id, message_id)
            await event.answer("✅ تم حذف الرسالة!", alert=True)
        except:
            await event.answer("❌ لا يمكن حذف الرسالة!", alert=True)

print("✅ Bot is running...")
ABH.run_until_disconnected()
