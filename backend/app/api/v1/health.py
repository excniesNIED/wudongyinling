from fastapi import APIRouter, Depends, HTTPException, status, WebSocket
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...models.health import HealthRecord
from pydantic import BaseModel
from datetime import datetime
import asyncio
import random

router = APIRouter()

class HealthRecordBase(BaseModel):
    blood_pressure: str
    heart_rate: int
    blood_sugar: float

class HealthRecordCreate(HealthRecordBase):
    user_id: int

class HealthRecordResponse(HealthRecordBase):
    id: int
    user_id: int
    recorded_at: datetime
    class Config:
        from_attributes = True

@router.get("/", response_model=List[HealthRecordResponse])
async def get_health_records(
    user_id: int | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(HealthRecord)
    if user_id:
        query = query.filter(HealthRecord.user_id == user_id)
    records = query.order_by(HealthRecord.recorded_at.desc()).offset(skip).limit(limit).all()
    return records

@router.post("/", response_model=HealthRecordResponse)
async def create_health_record(record: HealthRecordCreate, db: Session = Depends(get_db)):
    db_record = HealthRecord(**record.model_dump())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/{record_id}", response_model=HealthRecordResponse)
async def get_health_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(HealthRecord).filter(HealthRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record

@router.delete("/{record_id}")
async def delete_health_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(HealthRecord).filter(HealthRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    db.delete(record)
    db.commit()
    return {"message": "记录已删除"}

@router.put("/{record_id}", response_model=HealthRecordResponse)
async def update_health_record(record_id: int, record: HealthRecordBase, db: Session = Depends(get_db)):
    db_record = db.query(HealthRecord).filter(HealthRecord.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="记录不存在")
    for field, value in record.model_dump(exclude_unset=True).items():
        setattr(db_record, field, value)
    db.commit()
    db.refresh(db_record)
    return db_record

# WebSocket端点用于实时健康数据
@router.websocket("/ws/{user_id}")
async def health_data_websocket(websocket: WebSocket, user_id: int):
    await websocket.accept()
    try:
        while True:
            # 模拟实时数据
            data = {
                "blood_pressure": f"{random.randint(110,140)}/{random.randint(70,90)}",
                "heart_rate": random.randint(60,100),
                "blood_sugar": round(random.uniform(4.0,7.0), 1)
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except:
        await websocket.close() 