import os
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

# الحصول على المتغيرات من البيئة
api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء عميل Telethon
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# الحقوق عند التقييد (منع الإرسال والكتابة)
restrict_rights = ChatBannedRights(
    until_date=None,
    send_messages=True,  # منع إرسال الرسائل
    send_media=True,  # منع إرسال الوسائط
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True
)

# الحقوق عند رفع التقييد (إعادة الصلاحيات)
unrestrict_rights = ChatBannedRights(
    until_date=None,
    send_messages=False,  # السماح بإرسال الرسائل
    send_media=False,  # السماح بإرسال الوسائط
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)

@client.on(events.ChatAction)
async def monitor_restrictions(event):
    """
    يستمع البوت لأي تغيير في صلاحيات المستخدمين في المجموعة،
    وعند سحب صلاحيات الكتابة والإرسال، يعيدها بعد 30 دقيقة تلقائيًا.
    """
    if event.restricted:
        user = await event.get_user()
        chat = await event.get_chat()
        
        # التأكد أن المستخدم قد تم تقييده
        if event.restricted.default_banned_rights.send_messages:
            await event.reply(f"تم تقييد {user.first_name} من الكتابة والإرسال، سيتم رفع التقييد بعد 30 دقيقة.")
            
            # الانتظار لمدة 30 دقيقة
            await asyncio.sleep(1)

            # إعادة الصلاحيات
            await client(EditBannedRequest(chat.id, user.id, unrestrict_rights))
            await event.reply(f"تمت إعادة صلاحيات {user.first_name} بعد 30 دقيقة ✅")

client.start()
client.run_until_disconnected()
