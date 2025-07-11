from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from ...core.database import get_db
from ...models.prescription import Prescription
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PrescriptionBase(BaseModel):
    disease_type: str
    training_plan: str
    schedule: Dict[str, list]  # 格式: {"monday": ["运动1", "运动2"], "tuesday": [...]}

class PrescriptionCreate(PrescriptionBase):
    user_id: int

class PrescriptionUpdate(BaseModel):
    disease_type: Optional[str] = None
    training_plan: Optional[str] = None
    schedule: Optional[Dict[str, list]] = None

class PrescriptionResponse(PrescriptionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    class Config:
        from_attributes = True

@router.get("/", response_model=List[PrescriptionResponse])
async def get_prescriptions(
    user_id: Optional[int] = None,
    disease_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Prescription)
    if user_id:
        query = query.filter(Prescription.user_id == user_id)
    if disease_type:
        query = query.filter(Prescription.disease_type == disease_type)
    prescriptions = query.offset(skip).limit(limit).all()
    return prescriptions

@router.post("/", response_model=PrescriptionResponse)
async def create_prescription(prescription: PrescriptionCreate, db: Session = Depends(get_db)):
    db_prescription = Prescription(**prescription.model_dump())
    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

@router.get("/{prescription_id}", response_model=PrescriptionResponse)
async def get_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    return prescription

@router.put("/{prescription_id}", response_model=PrescriptionResponse)
async def update_prescription(
    prescription_id: int,
    prescription_update: PrescriptionUpdate,
    db: Session = Depends(get_db)
):
    db_prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not db_prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    
    update_data = prescription_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_prescription, field, value)
    
    db.commit()
    db.refresh(db_prescription)
    return db_prescription

@router.delete("/{prescription_id}")
async def delete_prescription(prescription_id: int, db: Session = Depends(get_db)):
    prescription = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if not prescription:
        raise HTTPException(status_code=404, detail="处方不存在")
    
    db.delete(prescription)
    db.commit()
    return {"message": "处方已删除"} 