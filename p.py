import sqlite3
import datetime
from telethon import TelegramClient, events, Button
import os

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# الاتصال بقاعدة البيانات أو إنشائها إذا كانت غير موجودة
conn = sqlite3.connect('user_dates.db')
c = conn.cursor()

# إنشاء جدول المستخدمين إذا لم يكن موجودًا
c.execute('''
CREATE TABLE IF NOT EXISTS user_dates (
    user_id INTEGER PRIMARY KEY,
    saved_date TEXT NOT NULL
)
''')
conn.commit()

# دالة لحفظ التاريخ في قاعدة البيانات
def save_date(user_id, date):
    c.execute("INSERT OR REPLACE INTO user_dates (user_id, saved_date) VALUES (?, ?)", (user_id, date))
    conn.commit()

# دالة لقراءة التاريخ من قاعدة البيانات
def get_saved_date(user_id):
    c.execute("SELECT saved_date FROM user_dates WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    return row[0] if row else None

# عندما يرسل المستخدم الأمر '/dates'
@ABH.on(events.NewMessage(pattern='^/dates$'))
async def show_dates(event):
    btton = [[
        Button.inline("محرم", b"m"),
        Button.inline("رمضان", b"rm"),
        Button.inline("شعبان", b"sh"),
        Button.inline("رجب", b"r"),
        Button.inline("حدد تاريخ", b"set_date")
    ]]
    await event.respond("اختر الشهر المناسب أو حدد تاريخ خاص 👇", buttons=btton)

# عندما يرسل المستخدم الأمر "حدد تاريخ"
@ABH.on(events.CallbackQuery(data=b"set_date"))
async def ask_for_date(event):
    await event.respond("من فضلك أدخل التاريخ بصيغة YYYY-MM-DD (مثال: 2025-06-26)")
    
# عندما يرسل المستخدم تاريخًا جديدًا
@ABH.on(events.NewMessage(pattern=r'^\d{4}-\d{2}-\d{2}$'))
async def set_user_date(event):
    user_id = event.sender_id
    date = event.text

    try:
        # التحقق من صحة التاريخ
        datetime.datetime.strptime(date, "%Y-%m-%d")
        save_date(user_id, date)
        await event.reply(f"تم حفظ التاريخ {date}. يمكنك الآن معرفة كم باقي.")
    except ValueError:
        await event.reply("التاريخ المدخل غير صالح، يرجى إدخاله بصيغة YYYY-MM-DD.")

# عندما يرسل المستخدم الأمر "كم باقي"
@ABH.on(events.NewMessage(pattern='^كم باقي$'))
async def cunt_m(event):
    user_id = event.sender_id
    saved_date = get_saved_date(user_id)  # الحصول على التاريخ المحفوظ من قاعدة البيانات

    if saved_date:
        t = datetime.datetime.today()
        saved_date_obj = datetime.datetime.strptime(saved_date, "%Y-%m-%d").date()
        days_difference = (saved_date_obj - t.date()).days
        if days_difference < 0:
            await event.reply(f"التاريخ قد مضى منذ {abs(days_difference)} يوم")
        else:
            await event.reply(f"باقي {days_difference} ايام")
    else:
        await event.reply("لم تحدد تاريخًا بعد، يرجى تحديد تاريخ أولاً.")

print("Bot is running...")
ABH.run_until_disconnected()
