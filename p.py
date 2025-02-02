import os
import datetime
from telethon import TelegramClient, events, Button
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# إعداد SQLAlchemy
DATABASE_URL = "sqlite:///user_dates.db"  # تحديد قاعدة البيانات (SQLite)
Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# تعريف الجدول
class UserDates(Base):
    __tablename__ = 'user_dates'

    user_id = Column(Integer, primary_key=True)
    saved_date = Column(String, nullable=False)

# إنشاء الجدول في قاعدة البيانات
Base.metadata.create_all(engine)

# إعداد البوت
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

ABH = TelegramClient('c', api_id, api_hash).start(bot_token=bot_token)

# دالة لحفظ التاريخ في قاعدة البيانات باستخدام SQLAlchemy
def save_date(user_id, date):
    existing_date = session.query(UserDates).filter_by(user_id=user_id).first()
    if existing_date:
        existing_date.saved_date = date  # تحديث التاريخ إذا كان موجودًا
    else:
        new_date = UserDates(user_id=user_id, saved_date=date)
        session.add(new_date)  # إضافة التاريخ الجديد
    session.commit()

# دالة لقراءة التاريخ من قاعدة البيانات
def get_saved_date(user_id):
    user_date = session.query(UserDates).filter_by(user_id=user_id).first()
    return user_date.saved_date if user_date else None

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

# دالة لاختيار التاريخ وحفظه (مثال لشهر "رجب")
@ABH.on(events.NewMessage(pattern='^رجب$'))
async def cunt_r(event):
    user_id = event.sender_id
    saved_date = '2025-06-26'  # تاريخ شهر رجب
    save_date(user_id, saved_date)  # حفظ التاريخ في قاعدة البيانات
    await event.reply(f"تم تحديد شهر رجب، وسيتم حساب الأيام المتبقية بالنسبة لهذا التاريخ.")

# دالة لاختيار تاريخ شهر شعبان
@ABH.on(events.NewMessage(pattern='^شعبان$'))
async def cunt_sh(event):
    user_id = event.sender_id
    saved_date = '2026-02-02'  # تاريخ شهر شعبان
    save_date(user_id, saved_date)
    await event.reply(f"تم تحديد شهر شعبان، وسيتم حساب الأيام المتبقية بالنسبة لهذا التاريخ.")

# دالة لاختيار تاريخ شهر رمضان
@ABH.on(events.NewMessage(pattern='^رمضان$'))
async def cunt_rm(event):
    user_id = event.sender_id
    saved_date = '2025-03-01'  # تاريخ شهر رمضان
    save_date(user_id, saved_date)
    await event.reply(f"تم تحديد شهر رمضان، وسيتم حساب الأيام المتبقية بالنسبة لهذا التاريخ.")

# دالة لاختيار تاريخ شهر محرم
@ABH.on(events.NewMessage(pattern='^محرم$'))
async def cunt_m(event):
    user_id = event.sender_id
    saved_date = '2025-09-01'  # تاريخ شهر محرم
    save_date(user_id, saved_date)
    await event.reply(f"تم تحديد شهر محرم، وسيتم حساب الأيام المتبقية بالنسبة لهذا التاريخ.")

print("Bot is running...")
ABH.run_until_disconnected()
