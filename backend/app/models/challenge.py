from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

# 用户-挑战关联表
challenge_participants = Table(
    'challenge_participants',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('challenge_id', Integer, ForeignKey('challenges.id')),
    Column('joined_at', DateTime(timezone=True), server_default=func.now())
)

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    participants = relationship("User", secondary=challenge_participants, backref="challenges")

class ChallengeRecord(Base):
    __tablename__ = "challenge_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    check_in_date = Column(DateTime(timezone=True), server_default=func.now())
    completed = Column(Boolean, default=True)
    
    user = relationship("User", backref="challenge_records")
    challenge = relationship("Challenge", backref="records") 