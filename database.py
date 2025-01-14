from sqlalchemy import Column, Integer, String
from db import BASE, SESSION, engine

class Whisper(BASE):
    __tablename__ = "whispers"
    whisper_id = Column(String(255), primary_key=True)
    sender_id = Column(String(255))
    username = Column(String(255))
    message = Column(String(255))

    def __init__(self, whisper_id, sender_id, username, message):
        self.whisper_id = whisper_id
        self.sender_id = sender_id
        self.username = username
        self.message = message

    @classmethod
    def create_table(cls):
        cls.__table__.create(bind=engine, checkfirst=True)

    @classmethod
    def store_whisper(cls, whisper_id, sender_id, username, message):
        whisper = cls(whisper_id=whisper_id, sender_id=sender_id, username=username, message=message)
        SESSION.add(whisper)
        SESSION.commit()

    @classmethod
    def get_whisper(cls, whisper_id):
        whisper = SESSION.query(cls).filter(cls.whisper_id == whisper_id).first()
        return whisper

Whisper.create_table()
