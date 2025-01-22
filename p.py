from db import is_approved_user, remove_approved_user, get_approved_users
from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)
recreate_tables()

admins = [
    191001559,
    7176263278,
    6783332896,
    1494932118,
    201728276,
    1688194818,
    5399306464,
    6498922948,
    1446637898
          ]
@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_group and event.sender_id in admins:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            group_id = event.chat_id
            user = reply_message.sender.first_name            
            add_approved_user(user_id, group_id)
            await event.reply(f"✅ تم السماح للمستخدم {user} بالتعديلات في هذه المجموعة فقط.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        return
@ABH.on(events.NewMessage(pattern='رفض'))
async def disapprove_user(event):
    if event.is_group and event.sender_id in admins:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            group_id = event.chat_id
            user = reply_message.sender.first_name            
            remove_approved_user(user_id, group_id)
            await event.reply(f"❌ تم إلغاء السماح للمستخدم {user} بالتعديلات في هذه المجموعة فقط.")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إلغاء السماح له بالتعديلات.")
    else:
        return

@ABH.on(events.NewMessage(pattern='المسموح لهم'))
async def list_approved_users(event):
    senid = event.sender_id
    if event.is_group and senid in admins:
        approved_users = get_approved_users(event.chat_id)
        
        if approved_users:
            approved_list = ""
            for user_id, group_id in approved_users:
                try:
                    user = await event.client.get_entity(user_id)  # جلب الكائن للمستخدم
                    user_name = user.username if user.username else user.first_name
                    approved_list += f"{user_name} - {user_id} @\n"
                except Exception as e:
                    approved_list += f"خطأ في جلب اسم المستخدم: {user_id}\n"
            
            await event.reply(f"📝 قائمة المستخدمين المسموح لهم بالتعديلات:\n{approved_list}")
        else:
            await event.reply("لا يوجد أي مستخدمين مسموح لهم بالتعديلات حالياً.")
    else:
        return
@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group and event.sender_id not in admins:
        user_id = event.sender_id
        group_id = event.chat_id
        approved_users = get_approved_users(group_id)
        approved_user_ids = [user[0] for user in approved_users]
        if user_id in approved_user_ids or user_id in admins:
            return
        if event.media or (event.message and any(x in event.message.message for x in ["http://", "https://"])):
            return
        await event.reply("❗ هنالك شخص عدل رسالة لكنها ليست ملفًا أو رابطًا.")
    else:
        return

ABH.run_until_disconnected()
