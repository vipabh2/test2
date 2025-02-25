from telethon import TelegramClient, events
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
is_on = None
@ABH.on(events.NewMessage(pattern="تفعيل"))
async def set(event):
    global is_on
    await event.reply("تم التفعيل")
    is_on = True
@ABH.on(events.NewMessage(pattern="تعطيل"))
async def set(event):
    global is_on
    await event.reply("تم التعطيل")
    is_on = False
@ABH.on(events.MessageEdited)
async def handler(event):
     if is_on == False:
         return
     else:
          await event.reply('تم تعديل مرفق في هذه الرسالة!')
ABH.run_until_disconnected()
