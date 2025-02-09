from telethon import TelegramClient, events
import os
from database import add_user_to_db, is_user_allowed, delete_user_from_db
from models import Base, engine

# تهيئة البوت
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

# إنشاء الجداول في قاعدة البيانات (إذا لم تكن موجودة)
Base.metadata.create_all(bind=engine)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id

    # التحقق من أن المستخدم مسموح له باستخدام البوت
    if not is_user_allowed(user_id):
        await event.respond("⚠️ عذرًا، أنت غير مسموح لك باستخدام هذا البوت.")
        return

    await event.respond("مرحبًا! أنت مسموح لك باستخدام هذا البوت.")

@client.on(events.NewMessage(pattern='/addme'))
async def add_me(event):
    user_id = event.sender_id

    # إضافة المستخدم إلى قاعدة البيانات
    add_user_to_db(user_id)
    await event.respond("تمت إضافتك إلى قائمة المستخدمين المسموح لهم.")

@client.on(events.NewMessage(pattern='/delme'))
async def del_me(event):
    user_id = event.sender_id

    # حذف المستخدم من قاعدة البيانات
    if delete_user_from_db(user_id):
        await event.respond("تم حذفك من قائمة المستخدمين المسموح لهم.")
    else:
        await event.respond("⚠️ لم يتم العثور عليك في قائمة المستخدمين المسموح لهم.")

client.start(bot_token=bot_token)
client.run_until_disconnected()
