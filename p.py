from telethon import TelegramClient, events
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
@ABH.on(events.MessageEdited)
async def handler(event):
     await event.reply('تم تعديل مرفق في هذه الرسالة!')
ABH.run_until_disconnected()
