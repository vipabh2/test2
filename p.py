from database import remove_approved_user, ApprovedUser, get_approved_users, add_approved_user, is_approved_user, get_whisper, store_whisper #type: ignore
from telethon import TelegramClient, events, Button
import requests, os, operator, asyncio, random, uuid
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.InlineQuery)
async def inline_query_handler(event):
    ifid = await event.get_reply_message()
    if ifid:
        to_id = ifid.sender_id
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
                reciver = await ABH.get_entity(username)
                reciver_id = reciver.id
                whisper_id = str(uuid.uuid4())
                if not username and ifid:
                    reciver_id = to_id
                    whisper_id = str(uuid.uuid4())
                store_whisper(whisper_id, sender, reciver_id, username, message)
                result = builder.article(
                    title='اضغط لإرسال الهمسة',
                    description=f'إرسال الرسالة إلى {username}',
                    text="همسة سرية إلى \n الله يثخن اللبن عمي 😌 ({username})",
                    buttons=[
                        Button.inline(
                            text='🫵🏾 اضغط لعرض الهمسة', 
                            data=f'send:{whisper_id}'
                        )                    ]                )
            except Exception as e:
                result = builder.article(
                    title='خطأ في الإرسال',
                    description="حدث خطأ أثناء معالجة طلبك.",
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
                
ABH.run_until_disconnected() 
