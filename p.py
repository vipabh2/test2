from telethon import TelegramClient, events
import os
from database import add_user_to_db, is_user_allowed, delete_user_from_db, get_allowed_users # type: ignore
from models import Base, engine # type: ignore
from datetime import datetime

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

client = TelegramClient('session_name', api_id, api_hash)

Base.metadata.create_all(bind=engine)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if not is_user_allowed(user_id):
        await event.respond("⚠️ عذرًا، أنت غير مسموح لك باستخدام هذا البوت.")
        return

@client.on(events.NewMessage(pattern=r'اضف (\d+)'))
async def add_me(event):
    sender_id = event.sender_id
    
    # السماح فقط للمستخدم 1910015590
    if sender_id != 1910015590:
        return  # لا يتم تنفيذ أي شيء

    user_id = int(event.pattern_match.group(1))  # استخراج ID المستخدم المُراد إضافته
    add_user_to_db(user_id)
    t1 = datetime.now()
    formatted_time = t1.strftime("%Y-%m-%d %I:%M:%S %p")
    await event.respond(f"تمت إضافة المستخدم `{user_id}` إلى قائمة المسموح لهم في: {formatted_time}.")

@client.on(events.NewMessage(pattern=r'حذف (\d+)'))
async def delete_me(event):
    sender_id = event.sender_id
    
    # السماح فقط للمستخدم 1910015590
    if sender_id != 1910015590:
        return  # لا يتم تنفيذ أي شيء

    user_id = int(event.pattern_match.group(1))  # استخراج ID المستخدم المُراد حذفه
    if delete_user_from_db(user_id):
        await event.respond(f"تم حذف المستخدم `{user_id}` من قائمة المستخدمين المسموح لهم.")
    else:
        await event.respond("⚠️ لم يتم العثور على المستخدم في القائمة.")

@client.on(events.NewMessage(pattern='/list'))
async def list_users(event):
    user_id = event.sender_id
    if user_id != 1910015590:
        await event.respond("⚠️ عذرًا، أنت غير مسموح لك باستخدام هذا الأمر.")
        return
    users = get_allowed_users()
    if users:
        user_list = "\n".join([f"(`{user.user_id}`) -  {user.added_at.strftime('%Y-%m-%d %I:%M:%S %p')}" for user in users])
        await event.respond(f"قائمة المستخدمين المسموح لهم:\n{user_list}")
    else:
        await event.respond("⚠️ لا يوجد مستخدمين مسموح لهم حاليًا.")
client.start(bot_token=bot_token)
client.run_until_disconnected()
