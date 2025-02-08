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

# تعريف دالة معالجة الرسائل
@ABH.on(events.NewMessage(pattern=r'(ترجمة|ترجمه)'))
async def handle_message(event):
    translator = Translator()
    
    # التحقق من وجود رد على الرسالة
    if event.is_reply:
        replied_message = await event.get_reply_message()
        original_text = replied_message.text 
    else:
        command_parts = event.message.text.split(' ', 1)
        original_text = command_parts[1] if len(command_parts) > 1 else None

    # التحقق من وجود نص للترجمة
    if not original_text:
        await event.reply("يرجى الرد على رسالة تحتوي على النص المراد ترجمته أو كتابة النص بجانب الأمر.")
        return

    try:
        # الكشف عن اللغة الأصلية
        detected_language = translator.detect(original_text).lang
        
        # التحقق من أن اللغة المكتشفة ليست None
        if not detected_language:
            await event.reply("❌ تعذر الكشف عن اللغة الأصلية.")
            return
        
        # تحديد اللغة الهدف
        target_lang = "en" if detected_language == "ar" else "ar"
        
        # ترجمة النص
        translated_text = translator.translate(original_text, dest=target_lang).text

        # التحقق من أن النص المترجم ليس None
        if not translated_text:
            await event.reply("❌ تعذر ترجمة النص.")
            return

        # إعداد الرد
        response = (
            f"اللغة المكتشفة: {detected_language}\n"
            f"النص المترجم: `{translated_text}`"
        )
        
        # إرسال الرد
        await event.reply(response)
    except Exception as e:
        # إرسال رسالة خطأ في حالة فشل الترجمة
        await event.reply(f"❌ حدث خطأ أثناء الترجمة: {str(e)}")

# بدء البوت
print("✅ البوت يعمل... انتظر الأوامر!")
ABH.run_until_disconnected()
