from db import add_approved_user, remove_approved_user, get_approved_users, ‎recreate_tables‎
from telethon.tl.types import ChatAdminRights
from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='ارفع'))
async def add_admin_command(event):
    if event.is_group:
        user_id = event.sender_id  # ID المستخدم الذي أرسل الأمر
        group_id = event.chat_id  # الحصول على group_id
        # تحقق إذا كان الشخص هو مالك المجموعة أو صاحب الـ ID المحدد
        if event.sender_id == 1910015590 or await is_owner(event):  # إذا كان المالك أو صاحب الـ ID
            if event.is_reply:
                reply_message = await event.get_reply_message()
                user_id_to_add = reply_message.sender_id
                user = reply_message.sender
                try:
                    add_admin(user_id_to_add, group_id)  # إضافة الأدمن في المجموعة المعينة
                    await event.reply(f"✅ تم إضافة المستخدم {user.first_name} كأدمن.")
                except Exception as e:
                    await event.reply(f"❌ خطأ أثناء إضافة الأدمن: {str(e)}")
            else:
                await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إضافته كأدمن.")
        else:
            await event.reply("❌ ليس لديك صلاحية لإجراء هذه العملية. فقط المالك أو صاحب الـ ID المحدد يمكنه إضافة أدمن.")
    else:
        return
async def is_owner(event):
    chat = await event.get_chat()  # الحصول على المجموعة
    participant = await ABH.get_chat_member(chat.id, event.sender_id)  # الحصول على بيانات العضو
    # تحقق إذا كان العضو هو مالك المجموعة
    return participant.is_creator
@ABH.on(events.NewMessage(pattern='نزل'))
async def remove_admin_command(event):
    if event.is_group:
        user_id = event.sender_id  # ID المستخدم الذي أرسل الأمر
        group_id = event.chat_id  # الحصول على group_id
        # تحقق إذا كان الشخص هو مالك المجموعة أو صاحب الـ ID المحدد
        if event.sender_id == 1910015590 or await is_owner(event):  # إذا كان المالك أو صاحب الـ ID
            if event.is_reply:
                reply_message = await event.get_reply_message()
                user_id_to_remove = reply_message.sender_id
                user = reply_message.sender
                try:
                    remove_admin(user_id_to_remove, group_id)  # إزالة الأدمن من المجموعة المعينة
                    await event.reply(f"✅ تم إزالة المستخدم {user.first_name} من الأدمن.")
                except Exception as e:
                    await event.reply(f"❌ خطأ أثناء إزالة الأدمن: {str(e)}")
            else:
                await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إزالة صلاحيات الأدمن عنه.")
        else:
            await event.reply("❌ ليس لديك صلاحية لإجراء هذه العملية. فقط المالك أو صاحب الـ ID المحدد يمكنه إزالة أدمن.")
    else:
        return

‎recreate_tables‎()

@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_group:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = reply_message.sender
            add_approved_user(user_id)
            await event.reply(f"✅ تم السماح للمستخدم {user} بالتعديلات.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        return

@ABH.on(events.NewMessage(pattern='ازالة'))
async def disapprove_user(event):
    if event.is_group:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = reply_message.sender
            remove_approved_user(user_id)
            await event.reply(f"تم مراقبة للمستخدم {user} بالتعديلات.")
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
            await event.reply("لا يوجد أي مستخدمين مسموح لهم بالتعديلات حالياً.")
    else:
        return
@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group:
        user_id = event.sender_id
        approved_users = get_approved_users()
        approved_user_ids = [user_id for user_id in approved_users]
        if user_id in approved_user_ids:
            return
        else:
            await event.reply("هنالك شخص عدل رسالة لكن غير معروف المقصد 🤔")
    else:
        return

ABH.run_until_disconnected()
