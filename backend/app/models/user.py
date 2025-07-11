from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # 修改为hashed_password以匹配auth.py
    email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)  # 修改为is_superuser以匹配auth.py
    
    # 添加关系
    health_records = relationship("HealthRecord", back_populates="user")
    prescriptions = relationship("Prescription", back_populates="user")
    sent_messages = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender")
    received_messages = relationship("ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver") 