from telethon import TelegramClient, events, Button
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.errors.rpcerrorlist import PeerIdInvalidError
import os

# الحصول على متغيرات البيئة
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# تهيئة عميل البوت
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# متغير لتخزين معرف كروب التبليغ
notification_group_id = None

# أمر لإضافة كروب التبليغ باستخدام ID
@ABH.on(events.NewMessage(pattern=r'^اضف كروب (\d+)$'))
async def add_group(event):
    global notification_group_id  # الوصول إلى المتغير العام
    match = event.pattern_match  # استخراج الرقم من الأمر
    if match:
        notification_group_id = int(match.group(1))
        await event.reply(f"تم تعيين الكروب بمعرف: {notification_group_id} ككروب التبليغ.")
    else:
        await event.reply("يرجى إدخال معرف كروب صحيح. مثال: `اضف كروب 123456789`")

# معالجة الرسائل المعدلة في المجموعات
@ABH.on(events.MessageEdited)
async def handle_edited_message(event):
    if event.is_group and event.message.media:
        buttons = [
            [Button.inline("إبلاغ المشرفين", b"notify_admins"), Button.inline("مسح", b"delete_only")]
        ]
        await event.reply("تم تعديل هذه الرسالة", buttons=buttons)

# معالجة ردود الأزرار
@ABH.on(events.CallbackQuery)
async def callback_handler(event):
    try:
        if event.data == b"notify_admins":
            await notify_admins(event)
        elif event.data == b"delete_only":
            me = await event.client.get_me()
            participant = await event.client.get_permissions(event.chat_id, me)
            
            if participant.is_admin:
                original_message = await event.get_message()
                await original_message.delete()  # حذف الرسالة الأصلية
                await event.reply("تم مسح الرسالة.")
            else:
                await event.reply("لا يمكنك مسح هذه الرسالة، فقط المشرفين يمكنهم ذلك.")
    except Exception as e:
        await event.reply(f"حدث خطأ: {str(e)}")

# وظيفة لإبلاغ المشرفين في كروب التبليغ
async def notify_admins(event):
    global notification_group_id  # الوصول إلى معرف كروب التبليغ
    if not notification_group_id:
        await event.reply("لم يتم تعيين كروب التبليغ بعد. استخدم الأمر 'اضف كروب <معرف>'.")
        return

    try:
        # تفاصيل الرسالة المعدلة
        message = await event.get_message()
        sender = await event.client.get_entity(message.sender_id)
        message_link = f"https://t.me/c/{str(event.chat_id)[4:]}/{message.id}"  # صياغة رابط الرسالة
        
        # اسم المستخدم، المعرف، والـID
        sender_name = sender.first_name if sender.first_name else "غير معروف"
        sender_username = f"@{sender.username}" if sender.username else "لا يوجد"
        sender_id = sender.id

        # نص البلاغ
        report_text = (
            f"🚨 **تم تعديل رسالة في المجموعة**: {event.chat.title}\n"
            f"👤 **المرسل**: {sender_name}\n"
            f"🔗 **المعرف**: {sender_username}\n"
            f"🆔 **الايدي**: `{sender_id}`\n"
            f"📎 [رابط الرسالة المعدلة]({message_link})"
        )

        # إرسال البلاغ إلى كروب التبليغ
        await event.client.send_message(notification_group_id, report_text, link_
