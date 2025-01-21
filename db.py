from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

if DATABASE_URL.startswith('postgresql://'):
    # الاتصال بقاعدة بيانات PostgreSQL باستخدام SQLAlchemy
    engine = create_engine(DATABASE_URL, echo=False)
    BASE = declarative_base()
    SessionLocal = sessionmaker(bind=engine)
    SESSION = SessionLocal()

    # نموذج SQLAlchemy لجدول المسموح لهم
    class Approval(BASE):
        __tablename__ = 'approvals'
        user_id = Column(Integer, primary_key=True)

    # إنشاء جدول المسموح لهم بالتعديلات
    def create_table():
        BASE.metadata.create_all(bind=engine)

    # إضافة مستخدم إلى قائمة المسموح لهم
    def add_approved_user(user_id):
        db_session = SessionLocal()
        new_user = Approval(user_id=user_id)
        db_session.add(new_user)
        db_session.commit()
        db_session.close()

    # إزالة مستخدم من قائمة المسموح لهم
    def remove_approved_user(user_id):
        db_session = SessionLocal()
        user = db_session.query(Approval).filter(Approval.user_id == user_id).first()
        if user:
            db_session.delete(user)
            db_session.commit()
        db_session.close()

    # استرجاع قائمة المستخدمين المسموح لهم
    def get_approved_users():
        db_session = SessionLocal()
        users = db_session.query(Approval).all()
        db_session.close()
        return [user.user_id for user in users]

else:
    raise ValueError("رابط قاعدة البيانات غير صالح أو غير مدعوم. تأكد من أنه PostgreSQL.")
