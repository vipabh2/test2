# db.py
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# الاتصال بقاعدة البيانات باستخدام متغير البيئة DATABASE_URL
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

# إنشاء محرك الاتصال
engine = create_engine(DATABASE_URL, echo=False)

# إنشاء الكلاس الأساسي
BASE = declarative_base()

# تعريف الجدول الذي سيحتوي على الهمسات
class Whisper(BASE):
    __tablename__ = 'whispers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    sender_username = Column(String, nullable=False)
    receiver_username = Column(String, nullable=False)

# إنشاء الجلسة
SessionLocal = sessionmaker(bind=engine)
SESSION = SessionLocal()

# دالة لإنشاء الجداول في قاعدة البيانات
def create_table():
    BASE.metadata.create_all(bind=engine)

# دالة لحفظ الهمسة في قاعدة البيانات
def save_whisper(message, sender_username, receiver_username):
    session = SessionLocal()
    whisper = Whisper(message=message, sender_username=sender_username, receiver_username=receiver_username)
    session.add(whisper)
    session.commit()
    session.close()
