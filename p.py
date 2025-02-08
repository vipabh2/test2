from telethon import TelegramClient, events
import os
import asyncio
from googletrans import Translator

# تحميل المتغيرات البيئية
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')

# بدء عميل التليجرام
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def handle_message(event):
    translator = Translator()
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text 
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None
    if not original_text:
        await event.reply("يرجى الرد على رسالة تحتوي على النص المراد ترجمته أو كتابة النص بجانب الأمر.")
        return
    detected_language = translator.detect(original_text)
    if detected_language.lang == "ar": 
        translated = translator.translate(original_text, dest="en")
    else: 
        translated = translator.translate(original_text, dest="ar")
    response = (
        f"اللغة المكتشفة: {detected_language.lang}\n"
        f"النص المترجم: `{translated.text}`"
    )
    await event.reply(response)

ABH.run_until_disconnected()
