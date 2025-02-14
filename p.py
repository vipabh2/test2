import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserNotParticipantError

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
    text = re.sub(r'(.)\1+', r'\1', text)  # إزالة التكرارات الزائدة
    return text

def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمة محظورة حتى لو كان فيها حروف مكررة"""
    words = message.split()
    normalized_words = [normalize_text(word) for word in words]
    for banned_word in banned_words:
        if normalize_text(banned_word) in normalized_words:
            return True
    return False

@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if event.is_group:
        chat = await event.get_chat()
        user_id = event.sender_id

        if event.raw_text.startswith('#'):
            new_word = event.raw_text[1:].strip()
            if new_word and new_word not in banned_words:
                banned_words.append(new_word)
                await event.reply(f"✅ تم إضافة الكلمة '{new_word}' إلى قائمة الكلمات المحظورة!")

        elif check_message(event.raw_text):
            await event.delete()
            warning_msg = "🚨 **تحذير:** لا يمكنك استخدام كلمات محظورة في المحادثة! 🚫"
            await event.reply(warning_msg)

            try:
                # 🔹 التأكد من أن المستخدم عضو في المجموعة
                participant = await ABH(GetParticipantRequest(chat, user_id))

                # 🔹 التحقق مما إذا كان المستخدم مشرفًا أو مالك المجموعة
                if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                    await event.reply("🚫 لا يمكن تقييد مشرف أو مالك المجموعة!")
                    return
                
                # 🔹 تنفيذ التقييد إذا لم يكن مشرفًا
                restrict_rights = ChatBannedRights(
                    until_date=None,  # لا يوجد تاريخ انتهاء
                    send_messages=True,  # منع إرسال الرسائل
                    send_media=True,
                    send_stickers=True,
                    send_gifs=True,
                    send_games=True,
                    send_inline=True,
                    embed_links=True
                )
                await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
                await event.reply(f"↩ المستخدم **{event.sender.first_name}** تم تقييده بسبب استخدامه لكلمة محظورة ☠")

            except UserNotParticipantError:
                await event.reply("⚠ المستخدم غير موجود في المجموعة، لا يمكن تقييده.")
            
            except UserAdminInvalidError:
                await event.reply("⚠ لا يمكن للبوت تقييد هذا المستخدم لأنه مشرف.")

            except Exception as e:
                await event.reply(f"❌ حدث خطأ غير متوقع: {str(e)}")

# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
