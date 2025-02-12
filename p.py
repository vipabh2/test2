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
banned_words = ["ممنوع", "كلمةمحظورة", "شتيمة", "ئ", "الئ"]  # إضافة الكلمات والأحرف المحظورة

def normalize_text(text):
    """إزالة الحركات، علامات الترقيم، وحرف 'ئ' فقط"""
    text = re.sub(r'[\u064B-\u0652ـ]', '', text)  # إزالة الحركات والتطويل
    text = re.sub(r'[~.,!?;:"\'،؛…()\[\]{}<>]', '', text)  # إزالة علامات الترقيم فقط
    text = text.replace('ئ', '')  # إزالة حرف 'ئ' من النص
    text = text.replace('الئ', '')  # إزالة "الئ" من النص
    text = re.sub(r'(.)\1+', r'\1', text)  # إزالة التكرار الزائد لأي حرف متكرر
    return text

def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمة محظورة حتى لو كان فيها حروف مكررة"""
    words = message.split()  # تقسيم الرسالة إلى كلمات منفصلة
    normalized_words = [normalize_text(word) for word in words]  # تنظيف كل كلمة
    
    for banned_word in banned_words:
        if normalize_text(banned_word) in normalized_words:  # تطابق 100% بعد المعالجة
            return True
    return False

@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    # إضافة كلمات محظورة جديدة باستخدام علامة #
    if event.raw_text.startswith('!'):
        new_word = event.raw_text[1:].strip()  # إزالة العلامة #
        if new_word not in banned_words:  # إذا لم تكن الكلمة موجودة من قبل
            banned_words.append(new_word)  # إضافتها إلى القائمة
            await event.reply(f"✅ تم إضافة الكلمة '{new_word}' إلى قائمة الكلمات المحظورة!")
    
    elif check_message(event.raw_text):
        user_id = event.sender_id
        warning_msg = "🚨 **تحذير:** لا يمكنك استخدام كلمات محظورة في المحادثة! 🚫"
        await ABH.send_message(user_id, warning_msg)  # إرسال رسالة خاصة للشخص

# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
