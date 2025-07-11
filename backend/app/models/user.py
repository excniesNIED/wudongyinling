from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from ..core.database import Base
from .health import HealthRecord
from .prescription import Prescription


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)  # 修改为hashed_password以匹配auth.py
    # email = Column(String(100), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)  # 修改为is_superuser以匹配auth.py
    
    # 添加关系
    health_records = relationship("HealthRecord", back_populates="user")
    prescriptions = relationship("Prescription", back_populates="user")

 