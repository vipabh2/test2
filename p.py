import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# جلب البيانات من متغيرات البيئة
api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل البوت
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# قائمة الكلمات المحظورة
banned_words = [
    "سب", "كس", "عير", "كسمك", "كسختك", "كس امك", "طيز", "طيزك", "فرخ", "كواد", 
    "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "اتنيج", "ينيج", 
    "اينيج", "بربوك", "زب", "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", 
    "برابيك", "نيجني", "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", 
    "مايا", "ماية", "مايه", "بكسمك", "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", 
    "سكسي", "كحاب", "مناويج", "منيوج", "عيورة", "عيورتكم", "انيجة", "انيچة", "انيجه", 
    "انيچه", "أناج", "اناج", "انيج", "أنيج", "فريخ", "فريخة", "فريخه", "فرخي", "🍆", 
    "🖕", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", "ارقة جاي", 
    "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", "الفرخ", "الفرحْ", "تيز", "كسم"
]

def normalize_text(text):
    """إزالة كل شيء عدا الأحرف مع إزالة الأرقام والحروف 'ـ' و 'ى'"""
    text = re.sub(r'[^أ-يa-zA-Z]', '', text)
    remove_chars = ['پ', 'ڤ', 'هـ', 'چ', 'گ', 'أ', 'إ', 'آ', 'ئ', 'ژ']
    for char in remove_chars:
        text = text.replace(char, '')
    text = text.replace('ـ', '')
    text = text.replace('ى', '')
    text = re.sub(r'(.)\1+', r'\1', text)
    return text

def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمة محظورة حتى لو كان فيها حروف مكررة"""
    words = message.split()
    normalized_words = [normalize_text(word) for word in words]
    for word in normalized_words:
        if "ى" * 3 in word:  # إذا كانت الكلمة تحتوي على ىىى
            return True
    for banned_word in banned_words:
        if normalize_text(banned_word) in normalized_words:
            return True
    return False

@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if event.is_group:
        if event.raw_text.startswith('#'):
            new_word = event.raw_text[1:].strip()
            if new_word not in banned_words:
                banned_words.append(new_word)
                await event.reply(f"✅ تم إضافة الكلمة '{new_word}' إلى قائمة الكلمات المحظورة!")
        
        elif check_message(event.raw_text):
            user_id = event.sender_id
            warning_msg = "🚨 **تحذير:** لا يمكنك استخدام كلمات محظورة في المحادثة! 🚫"
            await event.reply(warning_msg)

# حقوق التقييد ورفع الحقوق
restrict_rights = ChatBannedRights(
    until_date=None, 
    send_messages=True,  
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

unrestrict_rights = ChatBannedRights(
    until_date=None,  
    send_messages=False,  
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)

@ABH.on(events.ChatAction)
async def auto_unrestrict(event):
    try:
        if event.user_kicked:
            user = await event.get_user()
            chat = await event.get_chat()
            await ABH(EditBannedRequest(chat.id, user.id, unrestrict_rights))
            await event.reply(f"🚫 تم طرد {user.first_name} من المجموعة.")
        
        if hasattr(event.original_update, 'banned_rights'):
            if event.original_update.banned_rights:
                user = await event.get_user()
                chat = await event.get_chat()
                await ABH(EditBannedRequest(chat.id, user.id, restrict_rights))
                await event.reply(f"🚫 تم تقييد {user.first_name}.")
                await asyncio.sleep(3)
                await ABH(EditBannedRequest(chat.id, user.id, unrestrict_rights))
                await event.reply(f"✅ تم إعادة صلاحيات {user.first_name}.")

    except Exception as e:
        print(f"خطأ: {e}")

# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
