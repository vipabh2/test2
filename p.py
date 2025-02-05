from telethon import TelegramClient, events, Button
import os, uuid
from db import get_whisper, store_whisper

# تحميل متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

if not all([api_id, api_hash, bot_token]):
    raise ValueError("API_ID, API_HASH, and BOT_TOKEN must be set as environment variables")

# تشغيل البوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.InlineQuery)
async def inline_query_handler(event):
    replied = await event.get_reply_message()
    sender = event.sender_id
    query = event.text.strip()
    builder = event.builder

    if query:
        parts = query.split(' ')
        if len(parts) >= 2:
            message = ' '.join(parts[:-1])
            username = parts[-1]

            # إذا لم يكن هناك "@" في بداية الاسم، نضيفها
            if not username.startswith('@'):
                username = f'@{username}'

            # ✅ إذا كانت الرسالة ردًا، يتم إرسال الهمسة إلى الشخص الذي عليه الرد عبر ID الخاص به
            if replied:
                reciver_id = replied.sender_id
                username = f'User({reciver_id})'  # لتوضيح أنه ID وليس username
            else:
                # الحصول على الـ ID الخاص بالمستلم من `username`
                try:
                    reciver = await ABH.get_entity(username)
                    reciver_id = reciver.id
                except Exception as e:
                    result = builder.article(
                        title='خطأ في الإرسال',
                        description=f"خطأ: {str(e)}",
                        text='تعذر إرسال الهمسة بسبب خطأ.'
                    )
                    await event.answer([result])
                    return

            # إنشاء معرّف فريد للهمسة
            whisper_id = str(uuid.uuid4())
            store_whisper(whisper_id, sender, reciver_id, username, message)

            # ✅ تحديث `description` ليشمل إرسال الهمسة إلى الـ ID عند الرد
            result = builder.article(
                title='اضغط لإرسال الهمسة',
                description=f'إرسال الرسالة إلى {reciver_id}' if replied else f'إرسال الرسالة إلى {username}',
                text=f"همسة سرية إلى \n الله يثخن اللبن عمي 😌 ({username})",
                buttons=[
                    Button.inline(
                        text='🫵🏾 اضغط لعرض الهمسة', 
                        data=f'send:{whisper_id}'
                    )
                ]
            )

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
