from telethon import TelegramClient, events
from db import add_approved_user, remove_approved_user, get_approved_users, create_table
import os

# تحميل القيم من متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تحقق من وجود القيم المطلوبة
if not api_id or not api_hash or not bot_token:
    raise ValueError("تأكد من ضبط API_ID و API_HASH و BOT_TOKEN في متغيرات البيئة.")

# إعداد العميل
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# إنشاء جداول قاعدة البيانات
create_table()

@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_group:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            add_approved_user(user_id)  # إضافة المستخدم باستخدام user_id فقط
            await event.reply(f"✅ تم السماح للمستخدم صاحب ID: {user_id} بالتعديلات.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        return

@ABH.on(events.NewMessage(pattern='رفض'))
async def disapprove_user(event):
    if event.is_group:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            remove_approved_user(user_id)  # إزالة المستخدم باستخدام user_id فقط
            await event.reply(f"تم إلغاء السماح للمستخدم صاحب ID: {user_id} بالتعديلات.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إلغاء السماح له بالتعديلات.")
    else:
        return

@ABH.on(events.NewMessage(pattern='المسموح لهم'))
async def list_approved_users(event):
    if event.is_group:
        approved_users = get_approved_users()
        if approved_users:
            approved_list = "\n".join([str(user_id) for user_id in approved_users])
            await event.reply(f"📝 قائمة المستخدمين المسموح لهم بالتعديلات:\n{approved_list}")
        else:
            await event.reply("❗ لا يوجد أي مستخدمين مسموح لهم بالتعديلات حالياً.")
    else:
        return

@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group:
        user_id = event.sender_id
        approved_users = get_approved_users()

        if user_id in approved_users:  # التحقق مباشرة من قائمة المستخدمين
            return
        else:
            await event.reply("هنالك شخص عدل رسالة لكن غير معروف المقصد 🤔")
    else:
        return

# تشغيل العميل حتى يتم إيقافه
ABH.run_until_disconnected()
