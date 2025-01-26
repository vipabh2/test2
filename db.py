from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# إعداد الاتصال بقاعدة البيانات SQLite
DATABASE_URL = "sqlite:///db.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

# تعريف نموذج (Model) للهمسات
class Whisper(Base):
    __tablename__ = 'whispers'

    whisper_id = Column(String, primary_key=True)
    sender_id = Column(Integer)
    reciver_id = Column(Integer)
    username = Column(String)
    message = Column(String)

# إنشاء الجداول
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# دالة لتخزين الهمسات في قاعدة البيانات
def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    whisper = Whisper(whisper_id=whisper_id, sender_id=sender_id, reciver_id=reciver_id, username=username, message=message)
    session.add(whisper)
    session.commit()

# دالة لاسترجاع الهمسة من قاعدة البيانات
def get_whisper(whisper_id):
    return session.query(Whisper).filter_by(whisper_id=whisper_id).first()
