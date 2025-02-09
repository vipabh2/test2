from telethon import TelegramClient, events
import os
from database import add_user_to_db, is_user_allowed, delete_user_from_db, get_allowed_users
from models import Base, engine
from datetime import datetime

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
    try:
        add_user_to_db(user_id)
        t1 = datetime.now()
        formatted_time = t1.strftime("%Y-%m-%d %I:%M:%S %p")
        await event.respond(f"تمت إضافتك إلى قائمة المستخدمين المسموح لهم في: {formatted_time}.")
    except Exception as e:
        await event.respond(f"⚠️ حدث خطأ أثناء إضافتك: {e}")

@client.on(events.NewMessage(pattern='/delme'))
async def del_me(event):
    user_id = event.sender_id

    # حذف المستخدم من قاعدة البيانات
    try:
        if delete_user_from_db(user_id):
            await event.respond("تم حذفك من قائمة المستخدمين المسموح لهم.")
        else:
            await event.respond("⚠️ لم يتم العثور عليك في قائمة المستخدمين المسموح لهم.")
    except Exception as e:
        await event.respond(f"⚠️ حدث خطأ أثناء حذفك: {e}")

@client.on(events.NewMessage(pattern='/list'))
async def list_users(event):
    # عرض قائمة المستخدمين المسموح لهم مع الوقت
    try:
        users = get_allowed_users()
        if users:
            user_list = "\n".join([f"👤 {user.user_id} - 🕒 {user.added_at.strftime('%Y-%m-%d %I:%M:%S %p')}" for user in users])
            await event.respond(f"قائمة المستخدمين المسموح لهم:\n{user_list}")
        else:
            await event.respond("⚠️ لا يوجد مستخدمين مسموح لهم حاليًا.")
    except Exception as e:
        await event.respond(f"⚠️ حدث خطأ أثناء جلب القائمة: {e}")

@client.on(events.NewMessage(pattern='/help'))
async def help_command(event):
    # عرض جميع الأوامر المتاحة
    help_text = """
    🛠️ الأوامر المتاحة:
    /start - بدء استخدام البوت.
    /addme - إضافتك إلى قائمة المستخدمين المسموح لهم.
    /delme - حذفك من قائمة المستخدمين المسموح لهم.
    /list - عرض قائمة المستخدمين المسموح لهم.
    /help - عرض هذه الرسالة.
    """
    await event.respond(help_text)

client.start(bot_token=bot_token)
client.run_until_disconnected()
