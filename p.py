from telethon import TelegramClient, events, Button

api_id = "20464188"
api_hash = "91f0d1ea99e43f18d239c6c7af21c40f"
bot_token = "6965198274:AAEEKwAxxzrKLe3y9qMsjidULbcdm_uQ8IE"
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

whispers = {}

def store_whisper(whisper_id, sender_id, username, message):
    whispers[whisper_id] = {
        'sender_id': sender_id,
        'username': username,
        'message': message
    }

def get_whisper(whisper_id):
    return whispers.get(whisper_id)

@client.on(events.InlineQuery)
async def inline_query_handler(event):
    global whispers, sender
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
                whisper_id = f"{event.sender_id}:{username}"
                store_whisper(whisper_id, event.sender_id, username, message)

                result = builder.article(
                    title='اضغط لارسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text=f"همسة سرية إلى \n الله يثخن اللبن عمي ({username})",
                    buttons=[Button.inline(text='tap to see', data=f'send:{username}:{message}:{event.sender_id}:{whisper_id}')]
                )
            except Exception:
                result = builder.article(
                    title='لرؤية المزيد حول الهمس',
                    description="همس",
                    text='اضغط هنا'
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
    global whispers, sender, reciver, username
    reciver = event.username
    if reciver != username:
        await event.answer("هذه الرسالة ليست موجهة لك!", alert=True)
        return
    
    data = event.data.decode('utf-8')
    if data.startswith('send:'):
        _, username, message, sender_id, whisper_id = data.split(':', 4)
        try:
            whisper = get_whisper(whisper_id)

            if whisper:
                if sender_id == whisper['sender_id']:
                    await event.answer(f"{whisper['message']}", alert=True)
                else:
                    await event.answer("هذه الرسالة ليست موجهة لك!", alert=True)
            else:
                await event.answer("لم يتم العثور على الهمسة!", alert=True)

        except Exception as e:
            await event.answer(f'حدث خطأ: {str(e)}', alert=True)

client.run_until_disconnected()
