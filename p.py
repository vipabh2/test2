from db import ApprovedUser, get_approved_users, remove_approved_user, is_approved_user, add_approved_user
from telethon import TelegramClient, events
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

@ABH.on(events.NewMessage(pattern='^سماح$'))
async def approve_user(event):
    if event.is_group and event.sender_id in admins:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            group_id = event.chat_id
            user = reply_message.sender.first_name
            add_approved_user(user_id, group_id)
            await event.reply(f"تم السماح للمستخدم {user}بالتعديل الحر .")
        else:
            await event.reply("عزيزي المشرف الفاهي... \n يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        return
@ABH.on(events.NewMessage(pattern='^رفض$'))
async def disapprove_user(event):
    if event.is_group and event.sender_id in admins:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            group_id = event.chat_id
            user = reply_message.sender.first_name
            remove_approved_user(user_id, group_id)
            await event.reply(f"المستخدم {user} تم رفض تعديلاتة القادمة \n والله خطية.")
        else:
            await event.reply("عزيزي المشرف الاغبر... \n يرجى الرد على رسالة المستخدم الذي تريد رفضه بالتعديلات.")
    else:
        return
@ABH.on(events.NewMessage(pattern='^المسموح لهم$'))
async def list_approved_users(event):
    senid = event.sender_id
    if event.is_group and senid in admins:
        approved_users = get_approved_users(event.chat_id)
        if approved_users:
            approved_list = ""
            for user_id, group_id in approved_users:
                try:
                    user = await event.client.get_entity(user_id)
                    user_name = user.username if user.username else user.first_name
                    approved_list += f"{user_name} - {user_id} \n"
                except Exception as e:
                    approved_list += f"خطأ في جلب اسم المستخدم: {user_id}\n"
            await event.reply(f"📝 قائمة المستخدمين ال VIP بالتعديلات:\n{approved_list}")
        else:
            await event.reply("ماكو مستخدمين VIP او HIGH CLASS حالياً \n ضيفلك كم واحد حبيبي.") 
    else:
        return
admins = [
    1910015590,
    7176263278,
    6783332896,
    1494932118,
    201728276,
    1688194818,
    5399306464,
    6498922948,
    1446637898
]
@ABH.on(events.MessageEdited)
async def echo(event):
    if event.is_group:
        user_id = event.sender_id
        group_id = event.chat_id
        approved_users = get_approved_users(group_id)
        approved_user_ids = [user[0] for user in approved_users]
        if user_id in admins or user_id in approved_user_ids:
            return
        if event.media or ('http://' in event.message.message or 'https://' in event.message.message):
            await event.reply("هنالك شخص عدل رسالة لكن غير معروف المقصد 🤔")
        else:
            return
    else:
        return
ABH.run_until_disconnected()
