from telethon import TelegramClient, events, Button
from db import store_whisper, get_whisper  # استيراد الدوال من ملف models.py

api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    builder = event.builder
    query = event.text
    sender = event.sender_id

    if query.strip(): 
        parts = query.split(' ')
        if len(parts) >= 2: 
            message = ' '.join(parts[:-1]) 
            username = parts[-1] 
            
            if not username.startswith('@'):
                username = f'@{username}'
            
            try:
                reciver = await client.get_entity(username)  # الحصول على ID المستلم
                reciver_id = reciver.id  # الحصول على ID المستلم
                whisper_id = f"{sender}:{reciver_id}"  # إنشاء معرف خاص بالهمسة
                store_whisper(whisper_id, sender, reciver_id, username, message)

                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي ({username})",
                    buttons=[Button.inline(text='tap to see', data=f'send:{username}:{message}:{sender}:{whisper_id}')])
            except Exception as e:
                result = builder.article(
                    title='لرؤية المزيد حول الهمس',
                    description="همس",
                    text=f'خطأ: {str(e)}'
                )
        else:
            result = builder.article(
                title='خطأ في التنسيق',
                description="يرجى استخدام التنسيق الصحيح: @username <message>",
                text='التنسيق غير صحيح، يرجى إرسال الهمسة بالتنسيق الصحيح: @username <message>'
            )
        await event.answer([result])

@client.on(events.CallbackQuery)
async def callback_query_handler(event):
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        _, username, message, sender_id, whisper_id = data.split(':', 4)
        try:
            whisper = get_whisper(whisper_id)

            if whisper:
                # التحقق من أن الشخص الذي يطلب الهمسة هو إما المرسل أو المستلم
                if event.sender_id == whisper.sender_id or event.sender_id == whisper.reciver_id:
                    await event.answer(f"{whisper.message}", alert=True)
                else:
                    await event.answer("هذه الرسالة ليست موجهة لك!", alert=True)
            else:
                await event.answer("لم يتم العثور على الهمسة!", alert=True)

        except Exception as e:
            await event.answer(f'حدث خطأ: {str(e)}', alert=True)

client.run_until_disconnected()
