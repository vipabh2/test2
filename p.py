from telethon import TelegramClient, events
import os
import sqlite3

# إعداد بيانات الاتصال
api_id = int(os.getenv('API_ID'))  # تحويل إلى عدد صحيح
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

# إنشاء جلسة TelegramClient
ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# إنشاء قاعدة البيانات وجدول approvals
conn = sqlite3.connect('approvals.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS approvals (
    user_id INTEGER PRIMARY KEY,
    approved BOOLEAN NOT NULL
)
''')
conn.commit()

# معالجة أمر "سماح" لإضافة المستخدم إلى قائمة المسموح لهم
@ABH.on(events.NewMessage(pattern='سماح'))
async def approve_user(event):
    if event.is_reply:  # التحقق مما إذا كانت الرسالة ردًا
        reply_message = await event.get_reply_message()
        user_id = reply_message.sender_id  # استخراج معرف المستخدم من الرسالة التي تم الرد عليها
        
        # تخزين معرف المستخدم في قاعدة البيانات مع السماح بالتعديلات
        cursor.execute('INSERT OR REPLACE INTO approvals (user_id, approved) VALUES (?, ?)', (user_id, True))
        conn.commit()
        await event.reply(f"تم السماح بالتعديلات للمستخدم صاحب المعرف: {user_id}")
    else:
        # إذا لم تكن الرسالة ردًا
        await event.reply("❗ يرجى الرد على رسالة المستخدم الذي تريد السماح له بالتعديلات.")

# معالجة الرسائل المعدلة
@ABH.on(events.MessageEdited)
async def handle_edited_message(event):
    user_id = event.sender_id
    # التحقق مما إذا كان المستخدم مسموحًا له بالتعديل
    cursor.execute('SELECT approved FROM approvals WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result and result[0]:  # المستخدم مسموح له بالتعديل
        return  # لا يقوم بأي إجراء إضافي، يسمح بالتعديل فقط
    else:  # المستخدم غير مسموح له بالتعديل
        await event.reply("ها ههههه سالمين")  # إرسال الرسالة "ها ههههه سالمين"

# تشغيل العميل
ABH.run_until_disconnected()
