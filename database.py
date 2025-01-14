from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Whisper(BASE):
    __tablename__ = "whispers"
    whisper_id = Column(String(255), primary_key=True)
    sender_id = Column(Integer)
    username = Column(String(255))
    message = Column(String(255))
    created_at = Column(Integer)

    def __init__(self, whisper_id, sender_id, username, message):
        self.whisper_id = whisper_id
        self.sender_id = sender_id
        self.username = username
        self.message = message

    @classmethod
    def store_whisper(cls, whisper_id, sender_id, username, message):
        whisper = cls(whisper_id=whisper_id, sender_id=sender_id, username=username, message=message)
        SESSION.add(whisper)
        SESSION.commit()

    @classmethod
    def get_whisper(cls, whisper_id):
        return SESSION.query(cls).filter(cls.whisper_id == whisper_id).first()

    @classmethod
    def delete_whisper(cls, whisper_id):
        whisper = SESSION.query(cls).filter(cls.whisper_id == whisper_id).first()
        if whisper:
            SESSION.delete(whisper)
            SESSION.commit()

    @classmethod
    def get_all_whispers(cls):
        return SESSION.query(cls).all()
