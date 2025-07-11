from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.challenge import Challenge, ChallengeRecord
from ...models.user import User
from pydantic import BaseModel
from datetime import datetime, date

router = APIRouter()

class ChallengeBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime

class ChallengeCreate(ChallengeBase):
    pass

class ChallengeUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

class ChallengeResponse(ChallengeBase):
    id: int
    created_at: datetime
    participant_count: int
    class Config:
        from_attributes = True

class ChallengeRecordResponse(BaseModel):
    id: int
    user_id: int
    challenge_id: int
    check_in_date: datetime
    completed: bool
    class Config:
        from_attributes = True

@router.get("/", response_model=List[ChallengeResponse])
async def get_challenges(
    active_only: bool = False,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Challenge)
    if active_only:
        now = datetime.now()
        query = query.filter(Challenge.start_date <= now, Challenge.end_date >= now)
    challenges = query.offset(skip).limit(limit).all()
    
    # 添加参与人数
    for challenge in challenges:
        challenge.participant_count = len(challenge.participants)
    
    return challenges

@router.post("/", response_model=ChallengeResponse)
async def create_challenge(challenge: ChallengeCreate, db: Session = Depends(get_db)):
    db_challenge = Challenge(**challenge.model_dump())
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    db_challenge.participant_count = 0
    return db_challenge

@router.post("/{challenge_id}/join")
async def join_challenge(challenge_id: int, user_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user in challenge.participants:
        raise HTTPException(status_code=400, detail="已经参加过该挑战")
    
    challenge.participants.append(user)
    db.commit()
    return {"message": "成功加入挑战"}

@router.post("/{challenge_id}/check-in")
async def check_in(challenge_id: int, user_id: int, db: Session = Depends(get_db)):
    # 检查是否已经打卡
    today = date.today()
    existing_record = db.query(ChallengeRecord).filter(
        ChallengeRecord.challenge_id == challenge_id,
        ChallengeRecord.user_id == user_id,
        func.date(ChallengeRecord.check_in_date) == today
    ).first()
    
    if existing_record:
        raise HTTPException(status_code=400, detail="今日已打卡")
    
    # 创建打卡记录
    record = ChallengeRecord(
        user_id=user_id,
        challenge_id=challenge_id
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"message": "打卡成功"}

@router.get("/{challenge_id}/records", response_model=List[ChallengeRecordResponse])
async def get_challenge_records(
    challenge_id: int,
    user_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(ChallengeRecord).filter(ChallengeRecord.challenge_id == challenge_id)
    if user_id:
        query = query.filter(ChallengeRecord.user_id == user_id)
    records = query.order_by(ChallengeRecord.check_in_date.desc()).all()
    return records

@router.get("/{challenge_id}", response_model=ChallengeResponse)
async def get_challenge_by_id(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    challenge.participant_count = len(challenge.participants)
    return challenge

@router.put("/{challenge_id}", response_model=ChallengeResponse)
async def update_challenge(challenge_id: int, challenge_update: ChallengeUpdate, db: Session = Depends(get_db)):
    db_challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not db_challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    update_data = challenge_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_challenge, field, value)
    db.commit()
    db.refresh(db_challenge)
    db_challenge.participant_count = len(db_challenge.participants)
    return db_challenge

@router.delete("/{challenge_id}")
async def delete_challenge(challenge_id: int, db: Session = Depends(get_db)):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="挑战不存在")
    
    db.delete(challenge)
    db.commit()
    return {"message": "挑战已删除"}