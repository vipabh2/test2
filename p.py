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
            message = ' '.join(parts[1:-1])  # استخراج النص المطلوب إرساله
            username = parts[-1]  # استخراج اسم المستخدم

            if not username.startswith('@'):
                username = f'@{username}'
            
            try:
                reciver = await ABH.get_entity(username)  # جلب معلومات المستلم
                reciver_id = reciver.id  # الحصول على ID المستلم

                result = builder.article(
                    title='اضغط لعرض الرسالة السرية',
                    description=f'رسالة سرية إلى {username}',
                    text=f"📩 لديك رسالة سرية من شخص مجهول!\n\n"
                         f"اضغط على الزر أدناه لعرضها 👇",
                    buttons=[
                        Button.inline("👀 عرض الرسالة", data=f'show:{reciver_id}:{message}')
                    ]
                )
            except Exception as e:
                result = builder.article(
                    title='خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                )
        else:
            return
        await event.answer([result])

@ABH.on(events.CallbackQuery)
async def callback_handler(event):
    """ معالجة الضغط على زر عرض الرسالة """
    data = event.data.decode().split(':')
    
    if data[0] == 'show':
        reciver_id = int(data[1])
        secret_message = data[2]

        if event.query.user_id == reciver_id:
            await event.answer(f"📢 الرسالة السرية:\n\n{secret_message}", alert=True)
        else:
            await event.answer("❌ لا يمكنك عرض هذه الرسالة!", alert=True)

print("Bot is running...")
ABH.run_until_disconnected()
