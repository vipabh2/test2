from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")
Base = declarative_base()
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    recipient = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)
    password = Column(Text, nullable=False)
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
def get_saved_messages(user_id=None):
    """
    استرجاع الرسائل المحفوظة من قاعدة البيانات.
    :param user_id: إذا تم تحديده، سيتم استرجاع الرسائل المتعلقة بهذا المستخدم فقط.
    :return: قائمة من الرسائل.
    """
    with Session() as session:
        if user_id:
            messages = session.query(Message).filter_by(user_id=user_id).all()
        else:
            messages = session.query(Message).all()
        return messages
if __name__ == "__main__":
    with Session() as session:
        new_message = Message(
            user_id=12345,
            subject="اختبار",
            body="هذا نص الرسالة",
            recipient="example@telegram.org",
            sender_email="myemail@gmail.com",
            password="mysecurepassword"
        )
        session.add(new_message)
        session.commit()
        all_messages = get_saved_messages()
        for msg in all_messages:
            print(f"ID: {msg.id}, Subject: {msg.subject}, Recipient: {msg.recipient}")
