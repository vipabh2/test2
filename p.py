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
    """إزالة الحركات، علامات الترقيم، وحرف 'ئ' فقط"""
    text = re.sub(r'[\u064B-\u0652ـ]', '', text)  # إزالة الحركات العربية والتطويل
    text = re.sub(r'[~.,!?;:"\'،؛…()\[\]{}<>]', '', text)  # إزالة علامات الترقيم فقط
    text = text.replace('ئ', '')  # إزالة حرف 'ئ'
    return text  # **الإبقاء على باقي الأحرف والرموز كما هي**

def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمة مطابقة 100% من الكلمات المحظورة"""
    words = message.split()  # تقسيم الرسالة إلى كلمات منفصلة
    normalized_words = [normalize_text(word) for word in words]  # تنظيف كل كلمة على حدة
    
    for banned_word in banned_words:
        if normalize_text(banned_word) in normalized_words:  # تطابق 100%
            return True
    return False

@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if check_message(event.raw_text):
        user_id = event.sender_id
        warning_msg = "شباب لحد يفشر ويانه بنات بالكروب"
        await event.reply(warning_msg)  # إرسال رسالة خاصة للشخص

# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
