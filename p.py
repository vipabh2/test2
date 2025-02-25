import re
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaVideo, MessageMediaDocument  # إضافة أنواع الميديا الأخرى
import os

api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)

is_on = False

@ABH.on(events.NewMessage(pattern="تفعيل"))
async def activate(event):
    global is_on
    await event.reply("تم التفعيل")
    is_on = True

@ABH.on(events.NewMessage(pattern="تعطيل"))
async def deactivate(event):
    global is_on
    await event.reply("تم التعطيل")
    is_on = False

@ABH.on(events.MessageEdited)
async def handler(event):
    # تحقق إذا كان التفاعل مفعل (is_on = True)
    if not is_on:
        return

    # تحقق إذا كانت الرسالة تحتوي على مرفق من نوع ملف
    if event.message.media:
        # تحقق إذا كان المرفق من نوع ملف
        if isinstance(event.message.media, MessageMediaDocument):
            await event.reply('تم تعديل مرفق (ملف) في هذه الرسالة!')
        # تحقق إذا كان المرفق من نوع صورة
        elif isinstance(event.message.media, MessageMediaPhoto):
            await event.reply('تم تعديل صورة في هذه الرسالة!')
        # تحقق إذا كان المرفق من نوع فيديو
        elif isinstance(event.message.media, MessageMediaVideo):
            await event.reply('تم تعديل فيديو في هذه الرسالة!')
        # تحقق إذا كانت الرسالة تحتوي على رابط
        elif event.message.text and re.search(r'http[s]?://', event.message.text):
            await event.reply('تم تعديل رابط في هذه الرسالة!')

ABH.run_until_disconnected()
