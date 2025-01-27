from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# إعداد قاعدة البيانات
DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

# تعريف جدول الهمسات
class Whisper(Base):
    __tablename__ = 'whispers'

    id = Column(Integer, primary_key=True, autoincrement=True)  # مفتاح أساسي فريد
    whisper_id = Column(String)  # معرف الهمسة (يمكن أن يكون مكررًا)
    sender_id = Column(Integer)  # معرف المرسل
    reciver_id = Column(Integer)  # معرف المستقبل
    username = Column(String)  # اسم المستخدم
    message = Column(String)  # الرسالة نفسها

# إنشاء الجدول
Base.metadata.create_all(engine)

# إعداد الجلسة
Session = sessionmaker(bind=engine)
session = Session()

# دالة لتخزين الهمسات
def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    whisper = Whisper(
        whisper_id=whisper_id,
        sender_id=sender_id,
        reciver_id=reciver_id,
        username=username,
        message=message
    )
    session.add(whisper)  # إضافة الهمسة
    session.commit()  # حفظها في قاعدة البيانات

# دالة لاسترجاع الهمسة
def get_whisper(whisper_id):
    return session.query(Whisper).filter_by(whisper_id=whisper_id).first()  # استرجاع أول همسة فقط


