from telethon import TelegramClient, events
import os
import re

# جلب البيانات من متغيرات البيئة
api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل البوت
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# قائمة الكلمات المحظورة
banned_words = ["ممنوع", "كلمةمحظورة", "شتيمة"]

def normalize_text(text):
    """إزالة التغوييش من النص"""
    return re.sub(r'[^أ-يa-zA-Z0-9]', '', text)

def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمات محظورة"""
    normalized_message = normalize_text(message)
    for word in banned_words:
        if normalize_text(word) in normalized_message:
            return True
    return False

@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if check_message(event.raw_text):
        user_id = event.sender_id
        warning_msg = "🚨 **تحذير:** لا يمكنك استخدام كلمات محظورة في المحادثة! 🚫"
        await ABH.send_message(user_id, warning_msg)  # إرسال رسالة خاصة للشخص

# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
