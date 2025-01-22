from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Approval(BASE):
    __tablename__ = 'approvals'
    user_id = Column(BigInteger, primary_key=True)  # تغيير من Integer إلى BigInteger

def create_table():
    # BASE.metadata.drop_all(bind=engine)
    BASE.metadata.create_all(bind=engine)  # إعادة إنشاء الجدول

def add_approved_user(user_id):
    if not isinstance(user_id, int):
        raise ValueError(f"المعرّف {user_id} ليس رقمًا صحيحًا.")
    db_session = SessionLocal()
    new_user = Approval(user_id=user_id)
    db_session.add(new_user)
    db_session.commit()
    db_session.close()


def remove_approved_user(user_id):
    db_session = SessionLocal()
    user = db_session.query(Approval).filter(Approval.user_id == user_id).first()
    if user:
        db_session.delete(user)
        db_session.commit()
    db_session.close()

def get_approved_users():
    db_session = SessionLocal()
    users = db_session.query(Approval).all()
    db_session.close()
    return [user.user_id for user in users]

def add_group(group_id, group_name):
    db_session = SessionLocal()
    new_group = Group(group_id=group_id, group_name=group_name)
    db_session.add(new_group)
    db_session.commit()
    db_session.close()
