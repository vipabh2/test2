from telethon import TelegramClient, events, Button
import os
api_id = os.getenv('API_ID')      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 
ABH = TelegramClient('code', api_id, api_hash).start(bot_token=bot_token)


# إعدادات Telethon
API_ID = "YOUR_API_ID"
API_HASH = "YOUR_API_HASH"
BOT_TOKEN = "YOUR_BOT_TOKEN"

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

# تشغيل البوت
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if check_message(event.raw_text):
        user_id = event.sender_id
        warning_msg = "🚨 **تحذير:** لا يمكنك استخدام كلمات محظورة في المحادثة! 🚫"
        await bot.send_message(user_id, warning_msg)  # إرسال رسالة خاصة للشخص



ABH.run_until_disconnected() 
