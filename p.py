from telethon import TelegramClient, events
import os

# إعداد بيانات الاتصال
api_id = int(os.getenv('API_ID'))  # تحويل القيم إلى أعداد صحيحة
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء جلسة TelegramClient
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# قائمة للمستخدمين المسموح لهم بالتعديلات
approved_users = set()

# أمر "سماح" لإضافة المستخدم إلى قائمة المسموح لهم بالتعديلات
@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_reply:  # إذا كانت الرسالة ردًا
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id  # استخراج معرف المستخدم من الرسالة التي تم الرد عليها
        
        # إضافة المستخدم إلى قائمة المسموح لهم
        approved_users.add(user_id)
        await event.reply(f"✅ تم السماح للمستخدم {user_id} بالتعديلات.")
    else:
        await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")

# معالجة الرسائل المعدلة
@ABH.on(events.MessageEdited)
async def echo(event):
    user_id = event.sender_id
    if user_id in approved_users:  # التحقق مما إذا كان المستخدم مسموحًا له بالتعديل
        return  # السماح بالتعديل بدون أي رد
    elif event.message.media:  # إذا كان المستخدم غير مسموح وكان هناك وسائط
        await event.reply("ها ههههه سالمين")
    else:
        return  # لا تفعل شيئًا إذا لم تكن هناك وسائط

# تشغيل العميل
ABH.run_until_disconnected()
