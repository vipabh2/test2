from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

# إعداد قاعدة البيانات
engine = create_engine(DATABASE_URL, echo=False)
BASE = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# تعريف جدول الأدمن
class Admin(BASE):
    __tablename__ = 'admins'
    user_id = Column(BigInteger, primary_key=True)
    group_id = Column(BigInteger, primary_key=True)  # إضافة group_id


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

# إضافة مستخدم إلى قائمة الموافقات
def add_approved_user(user_id):
    if not isinstance(user_id, int):
        raise ValueError(f"المعرّف {user_id} ليس رقمًا صحيحًا.")
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

# إضافة مجموعة إلى قاعدة البيانات
def add_group(group_id, group_name):
    db_session = SessionLocal()
    new_group = Group(group_id=group_id, group_name=group_name)
    db_session.add(new_group)
    db_session.commit()
    db_session.close()
