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

# حقوق التقييد: إيقاف إرسال الرسائل بشكل دائم
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

# حقوق الرفع: السماح بإرسال الرسائل والوسائط
unrestrict_rights = ChatBannedRights(
    until_date=None,  # لا يوجد تاريخ انتهاء
    send_messages=False,  # السماح بإرسال الرسائل
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    embed_links=False
)

@client.on(events.ChatAction)
async def auto_unrestrict(event):
    await client(EditBannedRequest(chat.id, user.id, unrestrict_rights))
    await event.reply(f"✅ تم رفع التقييد عن {user.first_name} بعد 30 دقيقة.")
client.start()
client.run_until_disconnected()
