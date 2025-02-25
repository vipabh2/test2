import re
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto, MessageMediaVideo  # استيراد أنواع الوسائط المناسبة
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
    if not is_on:
        return

    # تحقق من الوسائط
    if event.message.media:
        if isinstance(event.message.media, MessageMediaDocument):
            await event.reply('تم تعديل مرفق (ملف) في هذه الرسالة!')
        elif isinstance(event.message.media, MessageMediaPhoto):
            await event.reply('تم تعديل صورة في هذه الرسالة!')
        elif isinstance(event.message.media, MessageMediaVideo):
            await event.reply('تم تعديل فيديو في هذه الرسالة!')

    # تحقق من وجود روابط في النصوص المعدلة
    elif event.message.text and re.search(r'http[s]?://', event.message.text):
        await event.reply('تم تعديل رابط في هذه الرسالة!')

    # حذف الرسالة المعدلة بعد الرد عليها
    await event.delete()

ABH.run_until_disconnected()
