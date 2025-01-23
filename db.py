from sqlalchemy import create_engine, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# إعداد قاعدة البيانات
Base = declarative_base()

# تعريف جدول "المستخدمين المعتمدين"
class ApprovedUser(Base):
    __tablename__ = 'approved_users'
    
    user_id = Column(Integer, primary_key=True)
    group_id = Column(Integer, primary_key=True)
    
    def __repr__(self):
        return f"<ApprovedUser(user_id={self.user_id}, group_id={self.group_id})>"

# إعداد الاتصال بقاعدة البيانات
DATABASE_URL = "sqlite:///approved_users.db"  # يمكنك تغيير نوع قاعدة البيانات حسب الحاجة
engine = create_engine(DATABASE_URL, echo=True)

# إنشاء الجداول في قاعدة البيانات
Base.metadata.create_all(bind=engine)

# إعداد الجلسة
Session = sessionmaker(bind=engine)
session = Session()

# دالة لإضافة مستخدم مع السماح له
def add_approved_user(user_id, group_id):
    # التحقق إذا كان المستخدم معتمدًا بالفعل
    existing_user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    
    if not existing_user:
        new_user = ApprovedUser(user_id=user_id, group_id=group_id)
        session.add(new_user)
        session.commit()

# دالة لإزالة المستخدم من قائمة المعتمدين
def remove_approved_user(user_id, group_id):
    user_to_remove = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    
    if user_to_remove:
        session.delete(user_to_remove)
        session.commit()

# دالة للتحقق إذا كان المستخدم معتمدًا في مجموعة معينة
def is_approved_user(user_id, group_id):
    user = session.query(ApprovedUser).filter_by(user_id=user_id, group_id=group_id).first()
    return user is not None

# تهيئة قاعدة البيانات عند بدء تشغيل البرنامج
def init_db():
    Base.metadata.create_all(bind=engine)

# تهيئة قاعدة البيانات عند بدء التشغيل
init_db()
