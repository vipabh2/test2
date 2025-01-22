from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

# تأكد من تعيين المتغير البيئي بشكل صحيح
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")

# إعداد قاعدة البيانات
Base = declarative_base()

# تعريف جدول "المستخدمين المعتمدين"
class ApprovedUser(Base):
    __tablename__ = 'approved_users'
    
    user_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, primary_key=True)
    
    def __repr__(self):
        return f"<ApprovedUser(user_id={self.user_id}, group_id={self.group_id})>"

# إعداد محرك قاعدة البيانات
engine = create_engine(DATABASE_URL, echo=False)

# تهيئة قاعدة البيانات عند بدء تشغيل البرنامج
def init_db():
    # إنشاء الجداول إذا لم تكن موجودة
    Base.metadata.create_all(bind=engine)

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()

# إعداد الجلسة
Session = sessionmaker(bind=engine)

# دالة لإضافة المستخدم إلى قائمة المعتمدين
def add_approved_user(user_id, group_id):
    # فتح جلسة جديدة
    with Session() as session:
        # تحقق مما إذا كان المستخدم موجودًا بالفعل في قاعدة البيانات
        if not is_approved_user(user_id, group_id):
            approved_user = ApprovedUser(user_id=user_id, group_id=group_id)
            session.add(approved_user)
            session.commit()

# دالة لإزالة المستخدم من قائمة المعتمدين
def remove_approved_user(user_id, group_id):
    # فتح جلسة جديدة
    with Session() as session:
        user_to_remove = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        if user_to_remove:
            session.delete(user_to_remove)
            session.commit()

# دالة للتحقق إذا كان المستخدم معتمدًا في مجموعة معينة
def is_approved_user(user_id, group_id):
    # فتح جلسة جديدة
    with Session() as session:
        user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
        return user is not None

# دالة لجلب جميع المستخدمين المعتمدين
def get_approved_users(group_id):
    # فتح جلسة جديدة
    with Session() as session:
        users = session.query(ApprovedUser).filter_by(group_id=group_id).all()
        user_list = [(user.user_id, user.group_id) for user in users]
        return user_list
