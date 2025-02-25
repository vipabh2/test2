from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage)
async def handler(event):
    # تحقق من أن الرسالة تحتوي على مرفق وتم تعديلها
    if event.message.media and event.message.edit_date:
        await event.reply('تم تعديل مرفق في هذه الرسالة!')

ABH.run_until_disconnected()
