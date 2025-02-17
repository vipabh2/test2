import os
import re
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator

# جلب البيانات من متغيرات البيئة
api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# تشغيل البوت
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

banned_words = [
    "سب", "كس", "عير", "كسمك", "كسختك", "كس امك", "طيز", "طيزك", "فرخ", "كواد", 
    "انيجك", "نيجك", "كحبة", "ابن الكحبة", "ابن الكحبه", "تنيج", "اتنيج", "ينيج", 
    "اينيج", "بربوك", "زب", "طيزها", "عيري", "خرب الله", "العير", "بعيري", "كحبه", 
    "برابيك", "نيجني", "نيچني", "نودز", "نتلاوط", "لواط", "لوطي", "فروخ", "منيوك", 
    "مايا", "ماية", "مايه", "بكسمك", "بكسختك", "🍑", "نغل", "نغولة", "نغوله", "ينغل", 
    "سكسي", "كحاب", "مناويج", "منيوج", "عيورة", "عيورتكم", "انيجة", "انيچة", "انيجه", 
    "انيچه", "أناج", "اناج", "انيج", "أنيج", "فريخ", "فريخة", "فريخه", "فرخي","قضيب", 
    "🖕", "كسك", "كسه", "كسة", "اكحاب", "أكحاب", "زنا", "كوم بي", "كمبي", "ارقة جاي", 
    "ارقه جاي", "يموط", "تموط", "موطلي", "اموط", "بورن", "الفرخ", "الفرحْ", "تيز", "كسم"
]
normalized_banned_words = {word: re.sub(r'(.)\1+', r'\1', word) for word in banned_words}
def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[^أ-يa-zA-Z\s]', '', text)
    replace_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ى': 'ي', 'ؤ': 'و', 'ئ': 'ي'}
    for old, new in replace_map.items():
        text = text.replace(old, new)
    text = re.sub(r'(.)\1+', r'\1', text)
    return text
async def is_admin(chat, user_id):
    """التحقق مما إذا كان المستخدم مشرفًا أو منشئ المجموعة"""
    try:
        participant = await ABH(GetParticipantRequest(chat, user_id))
        return isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator))
    except:
        return False
def check_message(message):
    """التحقق مما إذا كانت الرسالة تحتوي على كلمة محظورة"""
    normalized_message = normalize_text(message)
    words = normalized_message.split()
    return any(word in normalized_banned_words.values() for word in words)
@ABH.on(events.NewMessage)
async def handler(event):
    """التعامل مع الرسائل"""
    if event.is_group:
        message_text = event.raw_text.strip()
        user_id = event.sender_id
        chat = await event.get_chat()

        if check_message(message_text):
            if await is_admin(chat, user_id):
                await event.delete()
                await event.reply(f"المشرف [{event.sender.first_name}](tg://user?id={event.sender_id})، لا تستخدم الكلمات المحظورة!")
                return
            me = await ABH.get_me()
            if not await is_admin(chat, me.id):
                await event.reply("❌ لا أملك صلاحية تقييد الأعضاء، الرجاء إعطائي الصلاحيات اللازمة!")
                return
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
            try:
                await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
                await event.delete()
                await event.reply(f"المستخدم [{event.sender.first_name}](tg://user?id={event.sender_id}) تم تقييده لاستخدامه كلمات محظورة.")
                await asyncio.sleep(1)
                await ABH(EditBannedRequest(chat.id, user_id, unrestrict_rights))

            except Exception as e:
                await event.reply(f"لم أتمكن من تقييد المستخدم بسبب: {str(e)}")
                
# تشغيل البوت
print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
