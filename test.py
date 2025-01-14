from telethon import TelegramClient, events, Button
from database import Whisper, engine
from datetime import datetime, timedelta
import asyncio

api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# دالة لحذف الهمسات القديمة
async def delete_old_whispers():
    while True:
        current_time = datetime.utcnow()
        expiration_time = timedelta(days=1, hours=12)  # يوم ونصف
        expiration_time = timedelta(seconds=10)  # يوم ونصف
        whispers = Whisper.get_all_whispers()  # دالة لاسترجاع كل الهمسات
        for whisper in whispers:
            created_at = whisper.created_at
            if current_time - created_at > expiration_time:
                Whisper.delete_whisper(whisper.id)  # دالة لحذف الهمسة
        await asyncio.sleep(3600)  # الانتظار لمدة ساعة قبل التحقق مرة أخرى

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text

    if query.strip():
        parts = query.split(' ')
        if len(parts) >= 2:
            message = ' '.join(parts[:-1])
            username = parts[-1]

            if not username.startswith('@'):
                username = f'@{username}'

            try:
                user_entity = await client.get_entity(username)
                whisper_id = str(event.sender_id) + "_" + username
                created_at = datetime.utcnow()  # حفظ الوقت الحالي

                Whisper.store_whisper(whisper_id, event.sender_id, username, message, created_at)

                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"تم إنشاء همسة سرية إلى {username}. فقط المرسل والمستقبل يمكنهم رؤيتها.",
                    buttons=[
                        [Button.inline(text='عرض الهمسة', data=f'send:{whisper_id}')],
                    ]
                )
            except Exception as e:
                result = builder.article(
                    title='حدث خطأ',
                    description=str(e),
                    text=f'حدث خطأ: {str(e)}'
                )
        else:
            result = builder.article(
                title='خطأ في التنسيق',
                description='يرجى استخدام التنسيق الصحيح: @games_abh <message> @<username>',
                text='خطأ في التنسيق: يرجى استخدام التنسيق الصحيح: @games_abh <message> @<username>'
            )

        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        whisper_id = data.split(":")[1]
        whisper = Whisper.get_whisper(whisper_id)

        if whisper:
            await event.answer(f"الرسالة: {whisper.message}", alert=True)
        else:
            await event.answer("هذه الهمسة غير موجودة.", alert=True)

# بدء جدولة الحذف
client.loop.create_task(delete_old_whispers())

client.run_until_disconnected()
