from db import BASE, SESSION, engine
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Whisper(BASE):
    __tablename__ = "whispers"
    id = Column(Integer, primary_key=True, index=True)
    whisper_id = Column(String, index=True)
    sender_id = Column(String)
    username = Column(String)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, whisper_id, sender_id, username, message, created_at):
        self.whisper_id = whisper_id
        self.sender_id = sender_id
        self.username = username
        self.message = message
        self.created_at = created_at

    @classmethod
    def store_whisper(cls, whisper_id, sender_id, username, message, created_at):
        whisper = cls(whisper_id=whisper_id, sender_id=sender_id, username=username, message=message, created_at=created_at)
        SESSION.add(whisper)
        SESSION.commit()

    @classmethod
    def get_whisper(cls, whisper_id):
        return SESSION.query(cls).filter(cls.whisper_id == whisper_id).first()


    @classmethod
    def get_all_whispers(cls):
        return SESSION.query(cls).all()
