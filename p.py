from telethon import TelegramClient, events, Button
import os, uuid
from db import get_whisper, store_whisper

# تحميل متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text
    sender = event.sender_id

    if query.strip():
        parts = query.split(' ')
        if len(parts) >= 2:
            message = ' '.join(parts[:-1])
            recipient = parts[-1]

            try:
                if recipient.isdigit():  # إذا كان إدخالًا رقميًا، فاعتبره ID
                    reciver_id = int(recipient)
                    username = f'ID:{reciver_id}'
                else:  # إذا كان نصيًا، فاعتبره Username
                    if not recipient.startswith('@'):
                        recipient = f'@{recipient}'
                    reciver = await ABH.get_entity(recipient)
                    reciver_id = reciver.id
                    username = recipient  # استخدام اسم المستخدم كما هو

                whisper_id = str(uuid.uuid4())
                store_whisper(whisper_id, sender, reciver_id, username, message)

                result = builder.article(
                    title='اضغط لإرسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي 😌 ({username})",
                    buttons=[
                        Button.inline(
                            text='🫵🏾 اضغط لعرض الهمسة',
                            data=f'send:{whisper_id}'
                        )
                    ]
                )
            except Exception as e:
                result = builder.article(
                    title='خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
                    # text=f' خطأ: {str(e)}'
                )

        else:
            return
    
        await event.answer([result])

@ABH.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        whisper_id = data.split(':')[1]
        whisper = get_whisper(whisper_id)

        if whisper:
            if event.sender_id == whisper.sender_id or event.sender_id == whisper.reciver_id:
                await event.answer(f"{whisper.message}", alert=True)
            else:
                await event.answer("عزيزي الحشري، هذه الهمسة ليست موجهة إليك!", alert=True)

print("Bot is running...")
ABH.run_until_disconnected()
