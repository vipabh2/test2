from telethon import TelegramClient, events
from db import add_approved_user, remove_approved_user, get_approved_users, create_table, add_group
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# تأكد من أن الجدول تم إنشاؤه عند بدء التشغيل
create_table()

# إضافة مجموعة إلى قاعدة البيانات
@ABH.on(events.NewMessage(pattern='اضف كروب'))
async def add_group_command(event):
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            group_id = int(reply_message.text.split()[1])  # تحويل ID المجموعة إلى عدد صحيح
            group_name = ' '.join(reply_message.text.split()[2:])  # اسم المجموعة
            add_group(group_id, group_name)
            await event.respond(f"تم إضافة المجموعة {group_name} (ID: {group_id}) إلى قاعدة البيانات بنجاح.")
        except IndexError:
            await event.respond("❗ لم يتم توفير معرّف المجموعة أو الاسم.")
        except ValueError:
            await event.respond("❗ معرّف المجموعة غير صحيح.")
    else:
        await event.respond("❗ يرجى الرد على رسالة تحتوي على معرّف المجموعة واسمها.")

# السماح للمستخدم
@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_group:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = reply_message.sender
            try:
                add_approved_user(user_id)
                await event.reply(f"✅ تم السماح للمستخدم {user.first_name} بالتعديلات.")
            except Exception as e:
                await event.reply(f"❌ خطأ أثناء السماح للمستخدم: {str(e)}")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")
    else:
        return

# رفض السماح للمستخدم
@ABH.on(events.NewMessage(pattern='رفض'))
async def disapprove_user(event):
    if event.is_group:
        if event.is_reply:
            reply_message = await event.get_reply_message()
            user_id = reply_message.sender_id
            user = reply_message.sender
            try:
                remove_approved_user(user_id)
                await event.reply(f"❌ تم إلغاء السماح للمستخدم {user.first_name} بالتعديلات.")
            except Exception as e:
                await event.reply(f"❌ خطأ أثناء إلغاء السماح للمستخدم: {str(e)}")
        else:
            await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد إلغاء السماح له بالتعديلات.")
    else:
        return

# عرض قائمة المستخدمين المسموح لهم
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

# مراقبة الرسائل المعدلة
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
