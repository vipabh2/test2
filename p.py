from telethon import TelegramClient, events
from db import add_approved_user, remove_approved_user, get_approved_users, create_table

# إعدادات العميل
ABH = TelegramClient('session_name', api_id='API_ID', api_hash='API_HASH')

# إنشاء الجدول عند بدء التشغيل
create_table()

@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_group:  # التأكد من أن الرسالة في مجموعة
        if event.is_reply:  # إذا كانت الرسالة ردًا
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id  # استخراج معرف المستخدم من الرسالة التي تم الرد عليها
            add_approved_user(user_id)  # إضافة المستخدم إلى قائمة المسموح لهم باستخدام الدالة من db.py
            await event.reply(f"✅ تم السماح للمستخدم {user_id} بالتعديلات.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        await event.reply("❗ هذا الأمر يعمل فقط في المجموعات.")

@ABH.on(events.NewMessage(pattern='إلغاء سماح'))
async def disapprove_user(event):
    if event.is_group:  # التأكد من أن الرسالة في مجموعة
        if event.is_reply:  # إذا كانت الرسالة ردًا
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id  # استخراج معرف المستخدم من الرسالة التي تم الرد عليها
            remove_approved_user(user_id)  # إزالة المستخدم من قائمة المسموح لهم باستخدام الدالة من db.py
            await event.reply(f"❌ تم إلغاء السماح للمستخدم {user_id} بالتعديلات.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إلغاء السماح له بالتعديلات.")
    else:
        await event.reply("❗ هذا الأمر يعمل فقط في المجموعات.")

@ABH.on(events.NewMessage(pattern='قائمة المسموح لهم'))
async def list_approved_users(event):
    if event.is_group:  # التأكد من أن الرسالة في مجموعة
        approved_users = get_approved_users()  # استرجاع قائمة المسموح لهم باستخدام الدالة من db.py
        if approved_users:
            approved_list = "\n".join([str(user_id) for user_id in approved_users])
            await event.reply(f"📝 قائمة المستخدمين المسموح لهم بالتعديلات:\n{approved_list}")
        else:
            await event.reply("❗ لا يوجد أي مستخدمين مسموح لهم بالتعديلات حالياً.")
    else:
        await event.reply("❗ هذا الأمر يعمل فقط في المجموعات.")

@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group:  # التأكد من أن الرسالة في مجموعة
        user_id = event.sender_id
        approved_users = get_approved_users()  # استرجاع قائمة المسموح لهم باستخدام الدالة من db.py
        approved_user_ids = [user_id for user_id in approved_users]
        if user_id in approved_user_ids:  # التحقق مما إذا كان المستخدم مسموحًا له بالتعديل
            return  # السماح بالتعديل بدون أي رد
        else:
            await event.reply("❌ أنت غير مسموح لك بالتعديل.")
    else:
        return  # لا تفعل شيئًا إذا كانت الرسالة في محادثة خاصة

# تشغيل العميل
ABH.run_until_disconnected()
