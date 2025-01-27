from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

# تعريف نموذج (Model) للهمسات
class Whisper(Base):
    __tablename__ = 'whispers'

    id = Column(Integer, primary_key=True, autoincrement=True)  # مفتاح فريد لكل سجل
    whisper_id = Column(String)  # يمكن أن يكون مكررًا الآن
    sender_id = Column(Integer)
    reciver_id = Column(Integer)
    username = Column(String)
    message = Column(String)

# إنشاء الجداول
Base.metadata.create_all(engine)

# إنشاء جلسة
Session = sessionmaker(bind=engine)
session = Session()

# دالة لتخزين الهمسات في قاعدة البيانات
def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    whisper = Whisper(whisper_id=whisper_id, sender_id=sender_id, reciver_id=reciver_id, username=username, message=message)
    session.add(whisper)
    try:
        session.commit()
    except Exception as e:
        session.rollback()  # إذا حدث خطأ، تراجع عن العملية
        print(f"حدث خطأ أثناء إضافة الهمسة: {str(e)}")

# دالة لاسترجاع الهمسة من قاعدة البيانات
def get_whisper(whisper_id):
    return session.query(Whisper).filter_by(whisper_id=whisper_id).all()
