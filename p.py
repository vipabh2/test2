import os
import re
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest, GetParticipantRequest
from telethon.tl.types import ChatBannedRights, ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.errors.rpcerrorlist import UserAdminInvalidError, UserNotParticipantError, ParticipantIdInvalidError

# تحميل المتغيرات البيئية
api_id = int(os.getenv('API_ID'))      
api_hash = os.getenv('API_HASH')  
bot_token = os.getenv('BOT_TOKEN') 

# بدء تشغيل البوت
ABH = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# قائمة الكلمات المحظورة
banned_words = [
    "افتحج","افتحك","انيچة","انيچة","nude","nudse","porn","pornhub","xnxx","سكس","سكسي",
    "منيوك","نتلاوط","حلوك","نودز","نودزها","نودزج","لوطي","ابن اللوكي","ابن المهان",
    "بت الزنا","بت الزانية","بت الزانيه","بنت الزانيا","بنت الزانيه","بنت الزانية",
    "بربوك","برابيك","بربوكه","بربوكة","المفتوحه","المفتوحة","الرخيصه","الرخيصة",
    "العير","الزب","عيرين","عيوره","عيورة","اعيورة","اعيوره","بعيرك","بالعير",
    "كس","كسه","كسمك","كسختك","كسخالتك","كسخالك","كسختيك","كسج","كسها","الكس",
    "تنيجون","نيجني","النيجه","النيجة","النيج","ناجوك","نيجة","نيجه","نيجوه",
    "كواده","كواد","كواويد","مكوده","مكودة","مكودين","بتالكواد","ابنالكواد",
    "فرخ","فرخي","فرخه","فرخة","فريخه","فريخة","فروخ","فريخ","الفرخ","يموط",
    "نيجها","انيجكم","انيجها","متنايج","نتنايج","ناجوني","ناجوها","ناجوكم",
    "بكسمك", "بكسختك", "🍑", "نغل", "نغولة", "نغوله","احطه بيك","احطة بيك",
    "تيز","تيزك","تيزج","تيزه","كثه","كثة","موطلي","ام الموطه","ام الموطة",
    "ارقئ جاي","ارقى جاي","ارقة جاي","ارقه جاي","كمبي","كومبي"," كوم بي",
    "كحبه","كحبة","كحاب","كحبتي","مكحبه","مكحبة","كحابي","الكحبه","تموط",
    "خنيث","الخنيث","خنيثه","خنيثة","مخانيث","كم بي","تكوم بي","شعرضج",
    "طيز","طيزك","طيزج","طيزها","طيزين","طيازه","طيزكم","طيزه","الطيز",
    "ابن زنا","ابن زنه","ابن زنة","ابن زانية","ابن زانيه","بنت الزنا",
    "كحبتك","كحبته","كحبتة","كحبتنه","كحبتنه","الكحبة","كحبا","بورن",
    "زب","زبي","زبة","زبه","عير","عيري","عيره","عيرة","عيرج","بعيري",
    "ينغل","النغل","كسمه","كسمة","كسمي","كسمكم","كسمها","كسي","كسك",
    "تنيج","ينيج","نيج","نياج","نياجك","نياجها","نياجكم","مناويج",
    "سب"
            ]

# دالة لتطبيع النص
def normalize_text(text):
    text = re.sub(r'[^أ-يa-zA-Z]', '', text)
    return text

# دالة لتنظيف الرسالة
def clean_message(message):
    words = message.split()
    cleaned_words = [word if word not in banned_words else "****" for word in words]
    return " ".join(cleaned_words)

# معالج الأحداث
@ABH.on(events.NewMessage)
async def handler(event):
    if event.is_group and event.sender_id == 1910015590:
        if event.raw_text.startswith('#'):
            new_word = event.raw_text[1:].strip()
            if new_word not in banned_words:
                banned_words.append(new_word)
                await event.reply(f"✅ تم إضافة الكلمة '{new_word}' إلى قائمة الكلمات المحظورة!")
        else:
            cleaned_text = clean_message(event.raw_text)
            if cleaned_text != event.raw_text:
                user_id = event.sender_id
                chat = await event.get_chat()
                try:
                    participant = await ABH(GetParticipantRequest(chat.id, user_id))
                    if isinstance(participant.participant, (ChannelParticipantAdmin, ChannelParticipantCreator)):
                        return
                except (UserAdminInvalidError, UserNotParticipantError, ParticipantIdInvalidError) as e:
                    print(f"حدث خطأ: {e}")
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
                await ABH(EditBannedRequest(chat.id, user_id, restrict_rights))
                await event.delete()
                await event.reply(f"⤶ المستخدم [{event.sender.first_name}](tg://user?id={event.sender_id}) \n تم تقييده لاستخدامه كلمة محظورة ☠")

print("✅ البوت شغال وينتظر الرسائل...")
ABH.run_until_disconnected()
