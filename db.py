from sqlalchemy import create_engine, Column, BigInteger, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL')  # تأكد من تعيين المتغير البيئي بشكل صحيح

if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

# إعداد قاعدة البيانات PostgreSQL
engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# تعريف جدول الأدمن
class Admin(BASE):
    __tablename__ = 'admins'
    user_id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, primary_key=True)

# تعريف جدول الموافقات
class Approval(BASE):
    __tablename__ = 'approvals'
    user_id = Column(BigInteger, primary_key=True)

# تعريف جدول المجموعات
class Group(BASE):
    __tablename__ = 'groups'
    group_id = Column(BigInteger, primary_key=True)
    group_name = Column(String, index=True)

# إنشاء الجداول من جديد
def recreate_tables():
    BASE.metadata.drop_all(bind=engine)  # حذف الجداول الحالية
    BASE.metadata.create_all(bind=engine)  # إنشاء الجداول من جديد

recreate_tables()

# إضافة أدمن إلى مجموعة معينة
def add_admin(user_id, group_id):
    db_session = SessionLocal()
    new_admin = Admin(user_id=user_id, group_id=group_id)
    db_session.add(new_admin)
    db_session.commit()
    db_session.close()

# إزالة أدمن من مجموعة معينة
def remove_admin(user_id, group_id=None):
    db_session = SessionLocal()
    if group_id:
        # إزالة الأدمن من مجموعة معينة
        admin = db_session.query(Admin).filter(Admin.user_id == user_id, Admin.group_id == group_id).first()
    else:
        # إزالة الأدمن من جميع المجموعات
        admin = db_session.query(Admin).filter(Admin.user_id == user_id).first()
        
    if admin:
        db_session.delete(admin)
        db_session.commit()
    db_session.close()

# التحقق من كون المستخدم أدمن في مجموعة معينة
def is_admin(user_id, group_id):
    db_session = SessionLocal()
    admin = db_session.query(Admin).filter(Admin.user_id == user_id, Admin.group_id == group_id).first()
    db_session.close()
    return admin is not None

# إضافة مجموعة إلى قاعدة البيانات
def add_group(group_id, group_name):
    db_session = SessionLocal()
    new_group = Group(group_id=group_id, group_name=group_name)
    db_session.add(new_group)
    db_session.commit()
    db_session.close()
