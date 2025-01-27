from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

DATABASE_URL = "sqlite:///db.sqlite3"  # رابط قاعدة البيانات
engine = create_engine(DATABASE_URL, echo=False)

Base = declarative_base()

class Whisper(Base):
    __tablename__ = 'whispers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    whisper_id = Column(String, unique=True, nullable=False)
    sender_id = Column(Integer, nullable=False)
    reciver_id = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    message = Column(String, nullable=False)

Base.metadata.create_all(engine)  # إنشاء الجداول في قاعدة البيانات

Session = sessionmaker(bind=engine)
session = Session()

def store_whisper(whisper_id, sender_id, reciver_id, username, message):
    whisper = Whisper(whisper_id=whisper_id, sender_id=sender_id, reciver_id=reciver_id, username=username, message=message)
    session.add(whisper)
    session.commit()

def get_whisper(whisper_id):
    return session.query(Whisper).filter_by(whisper_id=whisper_id).first()
