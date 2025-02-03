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

@ABH.on(events.CallbackQuery)
async def handle_callback(event):
    data = event.data.decode("utf-8")

    if data == "set_date":
        await event.edit("من فضلك أدخل التاريخ بصيغة YYYY-MM-DD مثال: 2025-06-15", buttons=None)
    elif data == "m":
        await cunt_m(event, edit=True)
    elif data == "rm":
        await cunt_rm(event, edit=True)
    elif data == "sh":
        await cunt_sh(event, edit=True)
    elif data == "r":
        await cunt_r(event, edit=True)

@ABH.on(events.NewMessage(pattern=r'^\d{4}-\d{2}-\d{2}$'))
async def set_user_date(event):
    user_id = event.sender_id
    date = event.text

    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        save_date(user_id, date)
        await event.edit(f"تم حفظ التاريخ {date}. يمكنك الآن معرفة كم باقي.")
    except ValueError:
        await event.edit("التاريخ المدخل غير صالح، يرجى إدخاله بصيغة YYYY-MM-DD.")

@ABH.on(events.NewMessage(pattern='^كم باقي$'))
async def cunt_m(event):
    user_id = event.sender_id
    saved_date = get_saved_date(user_id)

    if saved_date:
        t = datetime.datetime.today()
        saved_date_obj = datetime.datetime.strptime(saved_date, "%Y-%m-%d").date()
        days_difference = (saved_date_obj - t.date()).days
        if days_difference < 0:
            await event.edit(f"التاريخ قد مضى منذ {abs(days_difference)} يوم")
        else:
            await event.edit(f"باقي {days_difference} ايام")
    else:
        await event.edit("لم تحدد تاريخًا بعد، يرجى تحديد تاريخ أولاً.")

async def cunt_r(event, edit=False):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 12, 22)
    days_difference = (t2 - t.date()).days
    msg = f"باقي {days_difference} ايام" if days_difference >= 0 else "الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1"
    await event.edit(msg)

async def cunt_sh(event, edit=False):
    t = datetime.datetime.today()
    t2 = datetime.date(2026, 1, 20)
    days_difference = (t2 - t.date()).days
    msg = f"باقي {days_difference} ايام" if days_difference >= 0 else "الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1"
    await event.edit(msg)

async def cunt_rm(event, edit=False):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 3, 1)
    days_difference = (t2 - t.date()).days
    msg = f"باقي {days_difference} ايام" if days_difference >= 0 else "الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1"
    await event.edit(msg)

async def cunt_m(event, edit=False):
    t = datetime.datetime.today()
    t2 = datetime.date(2025, 6, 26)
    days_difference = (t2 - t.date()).days
    msg = f"باقي {days_difference} ايام" if days_difference >= 0 else "الشهر قد بدأ \n يا مطوري حدث الكود @k_4x1"
    await event.edit(msg)

print("Bot is running...")
ABH.run_until_disconnected()
