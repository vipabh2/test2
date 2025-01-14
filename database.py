from db import BASE, SESSION, engine
from sqlalchemy import Column, Integer, String

class Whisper(BASE):
    __tablename__ = "whispers"
    id = Column(Integer, primary_key=True, index=True)
    whisper_id = Column(String, index=True)
    sender_id = Column(String)
    username = Column(String)
    message = Column(String)

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
        try:
            return SESSION.query(cls).filter(cls.whisper_id == whisper_id).first()
        except Exception as e:
            print(f"حدث خطأ أثناء استرجاع البيانات: {e}")
            return None  # إعادة قيمة فارغة في حال حدوث خطأ
