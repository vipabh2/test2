from telethon import TelegramClient, events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import asyncio
from datetime import datetime

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

# صلاحيات التقييد (منع الكتابة)
restrict_permissions = ChatBannedRights(
    until_date=None,  # سيتم تحديد المدة لاحقًا
    send_messages=True  # منع الكتابة
)

# صلاحيات الإعادة (إعادة الكتابة)
restore_permissions = ChatBannedRights(
    until_date=None,
    send_messages=False  # السماح بالكتابة
)

# قاموس لتخزين المستخدمين المقيدين
restricted_users = {}

# حدث لمراقبة التقييدات
@client.on(events.ChatAction)
async def track_restrictions(event):
    if event.is_group or event.is_channel:
        # التحقق من أن الحدث هو تقييد مستخدم
        if event.restricted:
            user_id = event.user_id
            chat_id = event.chat_id
            admin_id = event.action_message.from_id

            # تسجيل التقييد
            restricted_users[user_id] = {
                'chat_id': chat_id,
                'restricted_at': datetime.now(),
                'restricted_by': admin_id
            }

            # إعلام المشرفين
            admin = await client.get_entity(admin_id)
            user = await client.get_entity(user_id)
            await event.reply(
                f"تم تقييد المستخدم {user.first_name} (ID: {user_id}) بواسطة {admin.first_name} (ID: {admin_id})."
            )

            # جدولة إعادة الصلاحية بعد 30 دقيقة
            await asyncio.sleep(30 * 60)

            # إعادة الصلاحية
            await client(EditBannedRequest(
                chat_id=chat_id,
                user_id=user_id,
                banned_rights=restore_permissions
            ))

            # إعلام المشرفين بإعادة الصلاحية
            await event.reply(f"تم إعادة صلاحية الكتابة للمستخدم {user.first_name} (ID: {user_id}).")

            # إزالة المستخدم من القائمة
            if user_id in restricted_users:
                del restricted_users[user_id]

# حدث لعرض قائمة المستخدمين المقيدين
@client.on(events.NewMessage(pattern='/restricted_list'))
async def show_restricted_list(event):
    if event.is_group or event.is_channel:
        # التحقق من أن المرسل هو مشرف
        chat = await event.get_chat()
        sender = await event.get_sender()
        is_admin = False

        if hasattr(chat, 'participants'):
            participants = await client.get_participants(chat)
            for participant in participants:
                if participant.id == sender.id and participant.is_admin:
                    is_admin = True
                    break

        if is_admin:
            if restricted_users:
                message = "المستخدمون المقيدون حاليًا:\n"
                for user_id, details in restricted_users.items():
                    user = await client.get_entity(user_id)
                    admin = await client.get_entity(details['restricted_by'])
                    message += (
                        f"- {user.first_name} (ID: {user_id}) "
                        f"تم تقييده بواسطة {admin.first_name} (ID: {details['restricted_by']}) "
                        f"في {details['restricted_at']}\n"
                    )
                await event.reply(message)
            else:
                await event.reply("لا يوجد مستخدمون مقيدون حاليًا.")
        else:
            await event.reply("فقط المشرفون يمكنهم استخدام هذا الأمر.")
    else:
        await event.reply("هذا الأمر يعمل فقط في المجموعات والقنوات.")

# بدء تشغيل البوت
print("Bot is running...")
client.run_until_disconnected()
