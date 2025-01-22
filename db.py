from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

# إعداد قاعدة البيانات
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# تعريف جدول الموافقات
class Approval(BASE):
    __tablename__ = 'approvals'
    user_id = Column(BigInteger, primary_key=True)

# تعريف جدول المجموعات
class Group(BASE):
    __tablename__ = 'groups'
    group_id = Column(BigInteger, primary_key=True)
    group_name = Column(String, nullable=False)

# إنشاء الجداول
def create_table():
    BASE.metadata.create_all(bind=engine)

# إضافة مستخدم إلى قائمة الموافقات
def add_approved_user(user_id):
    db_session = SessionLocal()
    new_user = Approval(user_id=user_id)
    db_session.add(new_user)
    db_session.commit()
    db_session.close()

# إزالة مستخدم من قائمة الموافقات
def remove_approved_user(user_id):
    db_session = SessionLocal()
    user = db_session.query(Approval).filter(Approval.user_id == user_id).first()
    if user:
        db_session.delete(user)
        db_session.commit()
    db_session.close()

# الحصول على قائمة المستخدمين المسموح لهم
def get_approved_users():
    db_session = SessionLocal()
    users = db_session.query(Approval).all()
    db_session.close()
    return [user.user_id for user in users]

# إضافة مجموعة
def add_group(group_id, group_name):
    db_session = SessionLocal()
    new_group = Group(group_id=group_id, group_name=group_name)
    db_session.add(new_group)
    db_session.commit()
    db_session.close()
