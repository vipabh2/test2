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

# حقوق التقييد: منع المستخدم من إرسال الرسائل والوسائط
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

# حقوق الرفع: السماح بإرسال كل شيء
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

@client.on(events.ChatAction)
async def auto_unrestrict(event):
    """
    يراقب البوت أي عملية تقييد تحدث في المجموعة، 
    إذا تم تقييد مستخدم، يعيد صلاحياته بعد 3 ثوانٍ.
    """
    try:
        # التحقق مما إذا كان المستخدم قد تم تقييده
        if event.user_restricted:
            user = await event.get_user()
            chat = await event.get_chat()

            await event.reply(f"🚫 {user.first_name} تم تقييده في المجموعة!")

            # الانتظار 3 ثواني ثم إعادة الصلاحيات
            await asyncio.sleep(3)

            try:
                await client(EditBannedRequest(chat.id, user.id, unrestrict_rights))
                await event.reply(f"✅ تم إعادة صلاحيات {user.first_name} لإرسال الرسائل.")
            except Exception as e:
                print(f"خطأ أثناء إعادة الحقوق: {e}")

    except Exception as e:
        print(f"خطأ في معالجة الحدث: {e}")

client.run_until_disconnected()
