from telethon import TelegramClient, events
from playwright.async_api import async_playwright  # type: ignore
import os
import asyncio
from googletrans import Translator

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN')
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

    try:
        detected_language = translator.detect(original_text).lang
        target_lang = "en" if detected_language == "ar" else "ar"
        translated_text = translator.translate(original_text, dest=target_lang).text

        response = (
            f"اللغة المكتشفة: {detected_language}\n"
            f"النص المترجم: `{translated_text}`"
        )
        await event.reply(response)
    except Exception as e:
        await event.reply(f"❌ حدث خطأ أثناء الترجمة: {e}")


print("✅ البوت يعمل... انتظر الأوامر!")
ABH.run_until_disconnected()
