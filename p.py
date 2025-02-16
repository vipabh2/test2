import requests, os, operator, asyncio, random, uuid, datetime 
from telethon import TelegramClient, events, Button
from hijri_converter import Gregorian
from telethon.tl.custom import Button
from googletrans import Translator
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)
     
translator = Translator()
@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def handle_message(event):
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None
    if not original_text:
        await event.reply("عزيزي ...\n يرجئ كتابة النص مع الامر او بالرد عليه.")
        return
    detected_language = translator.detect(original_text).lang
    if detected_language == "ar":
        translated = translator.translate(original_text, dest="en")
    else:
        translated = translator.translate(original_text, dest="ar")
    response = (
        f" **اللغة المكتشفة:** `{detected_language}`\n"
        f" **النص المترجم:** `{translated.text}`"
        )
    await event.reply(response)

ABH.run_until_disconnected()
