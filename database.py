from sqlalchemy import create_engine, Column, Integer, String, Text, and_
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

def store_unique_message(user_id, subject, body, recipient, sender_email, password):
    """
    تخزين رسالة فريدة لكل مستخدم في قاعدة البيانات.
    :param user_id: معرف المستخدم.
    :param subject: موضوع الرسالة.
    :param body: نص الرسالة.
    :param recipient: المستلم.
    :param sender_email: البريد الإلكتروني للمرسل.
    :param password: كلمة المرور.
    :return: تم التخزين بنجاح أم لا.
    """
    with Session() as session:
        existing_message = session.query(Message).filter(
            and_(
                Message.user_id == user_id,
                Message.subject == subject,
                Message.body == body,
                Message.recipient == recipient,
                Message.sender_email == sender_email
            )
        ).first()
        if existing_message is None:
            new_message = Message(
                user_id=user_id,
                subject=subject,
                body=body,
                recipient=recipient,
                sender_email=sender_email,
                password=password
            )
            session.add(new_message)
            session.commit()
            return True
        else:
            return False

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

    # Testing the new function
    success = store_unique_message(
        user_id=12345,
        subject="اختبار",
        body="هذا نص الرسالة",
        recipient="example@telegram.org",
        sender_email="myemail@gmail.com",
        password="mysecurepassword"
    )
    if success:
        print("تم تخزين الرسالة بنجاح.")
    else:
        print("الرسالة موجودة بالفعل.")
