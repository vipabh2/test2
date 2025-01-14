from sqlalchemy import Column, Integer, String
from db import BASE, SESSION, engine
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
BASE = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SESSION = SessionLocal()

class UserScore(BASE):
    __tablename__ = "user_scores"
    user_id = Column(String(255), primary_key=True)
    username = Column(String(255))
    score = Column(Integer, default=0)

    def __init__(self, user_id, username, score=0):
        self.user_id = str(user_id)
        self.username = str(username)
        self.score = score

    def create_table(cls):
        cls.__table__.create(bind=engine, checkfirst=True)

    def add_or_update_user(cls, user_id, username):
        user = SESSION.query(cls).get(str(user_id))
        if not user:
            user = cls(user_id=str(user_id), username=str(username))
            SESSION.add(user)
        SESSION.commit()

    def add_point_to_winner(cls, user_id):
        user = SESSION.query(cls).get(str(user_id))
        if user:
            user.score += 1
            SESSION.commit()

    def get_user_score(cls, user_id):
        user = SESSION.query(cls).get(str(user_id))
        return user.score if user else 0

class Whisper(BASE):
    __tablename__ = "whispers"
    whisper_id = Column(String(255), primary_key=True)
    sender_id = Column(String(255))
    recipient_username = Column(String(255))
    message = Column(String(1000))

    def __init__(self, whisper_id, sender_id, recipient_username, message):
        self.whisper_id = whisper_id
        self.sender_id = str(sender_id)
        self.recipient_username = recipient_username
        self.message = message

    def create_table(cls):
        cls.__table__.create(bind=engine, checkfirst=True)

    def store_whisper(cls, whisper_id, sender_id, recipient_username, message):
        whisper = cls(whisper_id=whisper_id, sender_id=sender_id, recipient_username=recipient_username, message=message)
        SESSION.add(whisper)
        SESSION.commit()

    def get_whisper(cls, whisper_id):
        whisper = SESSION.query(cls).filter(cls.whisper_id == whisper_id).first()
        return whisper

UserScore.create_table()
Whisper.create_table()

Whisper.store_whisper('whisper123', '12345', '@user1', 'هذه همسة سرية')

whisper = Whisper.get_whisper('whisper123')
if whisper:
    print(f"الهمسة: {whisper.message} المرسل: {whisper.sender_id} المستلم: {whisper.recipient_username}")
else:
    print("لم يتم العثور على الهمسة.")
