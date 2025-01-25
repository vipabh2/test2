# from sqlalchemy import create_engine, Column, Integer, String, Text
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
# DATABASE_URL = os.getenv('DATABASE_URL')
# if not DATABASE_URL:
#     raise ValueError("متغير البيئة 'DATABASE_URL' غير موجود. تأكد من تعيينه بشكل صحيح.")
# Base = declarative_base()

# class Message(Base):
#     __tablename__ = 'messages'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, nullable=False)
#     subject = Column(String, nullable=False)
#     body = Column(Text, nullable=False)
#     recipient = Column(String, nullable=False)
#     sender_email = Column(String, nullable=False)
#     password = Column(String, nullable=False)

# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()
