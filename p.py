from telethon import TelegramClient, events
from db import add_approved_user, remove_approved_user, get_approved_users, create_table, is_admin, add_admin
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)
create_table()

# إضافة أدمن (إما المالك أو صاحب الـ ID المعين يمكنه ذلك)
@ABH.on(events.NewMessage(pattern='ارفع'))
async def add_admin_command(event):
    if event.is_group:
        user_id = event.sender_id  # ID المستخدم الذي أرسل الأمر
        # تحقق إذا كان الشخص هو مالك المجموعة أو صاحب الـ ID المحدد
        if event.sender_id == 1910015590 or await is_owner(event):  # إذا كان المالك أو صاحب الـ ID
            if event.is_reply:
                reply_message = await event.get_reply_message()
                user_id_to_add = reply_message.sender_id
                user = reply_message.sender
                try:
                    add_admin(user_id_to_add)
                    await event.reply(f"✅ تم إضافة المستخدم {user.first_name} كأدمن.")
                except Exception as e:
                    await event.reply(f"❌ خطأ أثناء إضافة الأدمن: {str(e)}")
            else:
                await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إضافته كأدمن.")
        else:
            await event.reply("❌ ليس لديك صلاحية لإجراء هذه العملية. فقط المالك أو صاحب الـ ID المحدد يمكنه إضافة أدمن.")
    else:
        return

# دالة للتحقق إذا كان الشخص مالك المجموعة
async def is_owner(event):
    # احصل على صلاحيات الشخص في المجموعة
    participant = await event.get_chat()
    if participant.admin_rights.is_creator:
        return True
    return False


# السماح للمستخدم (فقط الأدمن يمكنه ذلك)
@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_group:
        if event.is_reply:
            user_id = event.sender_id  # ID المستخدم الذي أرسل الأمر
            # تحقق إذا كان الشخص أدمن
            if is_admin(user_id):
                reply_message = await event.get_reply_message()
                user_id_to_approve = reply_message.sender_id
                user = reply_message.sender
                try:
                    add_approved_user(user_id_to_approve)
                    await event.reply(f"✅ تم السماح للمستخدم {user.first_name} بالتعديلات.")
                except Exception as e:
                    await event.reply(f"❌ خطأ أثناء السماح للمستخدم: {str(e)}")
            else:
                await event.reply("❌ ليس لديك صلاحية لإجراء هذه العملية. فقط الأدمن يمكنه السماح للمستخدمين.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        return

# رفض السماح للمستخدم (فقط الأدمن يمكنه ذلك)
@ABH.on(events.NewMessage(pattern='رفض'))
async def disapprove_user(event):
    if event.is_group:
        if event.is_reply:
            user_id = event.sender_id  # ID المستخدم الذي أرسل الأمر
            # تحقق إذا كان الشخص أدمن
            if is_admin(user_id):
                reply_message = await event.get_reply_message()
                user_id_to_reject = reply_message.sender_id
                user = reply_message.sender
                try:
                    remove_approved_user(user_id_to_reject)
                    await event.reply(f"❌ تم إلغاء السماح للمستخدم {user.first_name} بالتعديلات.")
                except Exception as e:
                    await event.reply(f"❌ خطأ أثناء إلغاء السماح للمستخدم: {str(e)}")
            else:
                await event.reply("❌ ليس لديك صلاحية لإجراء هذه العملية. فقط الأدمن يمكنه رفض المستخدمين.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إلغاء السماح له بالتعديلات.")
    else:
        return

# عرض قائمة المستخدمين المسموح لهم (فقط الأدمن يمكنه ذلك)
@ABH.on(events.NewMessage(pattern='المسموح لهم'))
async def list_approved_users(event):
    if event.is_group:
        user_id = event.sender_id  # ID المستخدم الذي أرسل الأمر
        # تحقق إذا كان الشخص أدمن
        if is_admin(user_id):
            approved_users = get_approved_users()
            if approved_users:
                approved_list = "\n".join([str(user_id) for user_id in approved_users])
                await event.reply(f"📝 قائمة المستخدمين المسموح لهم بالتعديلات:\n{approved_list}")
            else:
                await event.reply("لا يوجد أي مستخدمين مسموح لهم بالتعديلات حالياً.")
        else:
            await event.reply("❌ ليس لديك صلاحية لإجراء هذه العملية. فقط الأدمن يمكنه عرض قائمة المسموح لهم.")
    else:
        return

@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group:
        user_id = event.sender_id
        approved_users = get_approved_users()
        if user_id in approved_users:
            return
        else:
            await event.reply("هنالك شخص عدل رسالة لكن غير معروف المقصد 🤔")
    else:
        return

# بدء البوت
ABH.run_until_disconnected()
