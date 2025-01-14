from telethon import TelegramClient, events, Button
from database import store_whisper, get_whisper

api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

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

                store_whisper(whisper_id, event.sender_id, username, message)

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
        whisper = get_whisper(whisper_id)

        if whisper:
            await event.answer(f"الرسالة: {whisper.message}", alert=True)
        else:
            await event.answer("هذه الهمسة غير موجودة.", alert=True)

client.run_until_disconnected()
