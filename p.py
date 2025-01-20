from telethon import TelegramClient, events
import os
from database import save_notification_group, get_notification_group, delete_notification_group, approve_user, remove_approval, is_user_approved, initialize_db

# الحصول على متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تهيئة عميل البوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

initialize_db()

@ABH.on(events.NewMessage(pattern=r'^اضف (\d+)$'))
async def add_group(event):
    match = event.pattern_match
    if match:
        notification_group_id = int(match.group(1))
        group_id = event.chat_id
        chat_link = await event.get_chat()
        chat_link = chat_link.username if chat_link.username else None
        if chat_link:
            chat_link = f"https://t.me/{chat_link}"
        else:
            chat_link = "رابط غير متاح"
        save_notification_group(group_id, notification_group_id)
        await event.reply(f"تم تعيين الكروب بمعرف: {notification_group_id} ككروب التبليغ. رابط المجموعة: {chat_link}")
    else:
        await event.reply("يرجى إدخال معرف كروب صحيح. مثال: `اضف كروب 123456789`")

@ABH.on(events.NewMessage(pattern=r'^احذف (\d+)$')) 
async def delete_group(event):
    match = event.pattern_match
    if match:
        group_id = event.chat_id
        result = delete_notification_group(group_id)
        if result:
            await event.reply(f"تم حذف الكروب بمعرف: {group_id} من قاعدة البيانات.")
        else:
            await event.reply("لا يوجد كروب تم تعيينه لهذه المجموعة بهذا المعرف.")
    else:
        await event.reply("يرجى إدخال معرف كروب صحيح. مثال: `احذف كروب 123456789`")

@ABH.on(events.NewMessage(pattern=r'^رفض (\d+)$'))
async def approve_user_command(event):
    match = event.pattern_match
    if match:
        user_id = int(match.group(1))
        group_id = event.chat_id
        approve_user(group_id, user_id)
        await event.reply(f"تم الرفض للمستخدم بمعرف: {user_id} بالتعديل.")

@ABH.on(events.NewMessage(pattern=r'^سماح (\d+)$'))
async def remove_approval_command(event):
    match = event.pattern_match
    if match:
        user_id = int(match.group(1))
        group_id = event.chat_id
        remove_approval(group_id, user_id)
        await event.reply(f"تم السماح للمستخدم بمعرف {user_id} بالتعديل.")

@ABH.on(events.MessageEdited)
async def handle_edited_message(event):
    if event.is_group and hasattr(event.original_update, 'message') and event.original_update.message.media:
        edited_message = event.original_update.message
        sender = await event.client.get_entity(edited_message.sender_id)
        if is_user_approved(event.chat_id, sender.id):
            return 
            try:
                await event.client.send_message(notification_group_id, report_text, link_preview=False)
            except Exception as e:
                await event.reply(f"تعذر إرسال البلاغ إلى كروب التبليغ: {str(e)}")
        else:
            await event.reply("لم يتم تعيين كروب التبليغ لهذه المجموعة. استخدم الأمر 'اضف كروب <معرف>' لتعيين كروب التبليغ.")

ABH.run_until_disconnected()
