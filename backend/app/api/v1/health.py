from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime, date

from ...core.database import get_async_db
from ...schemas.health import HealthRecordCreate, HealthRecordUpdate, HealthRecordPublic, HealthStatistics
from ...schemas.base import DataResponse, PaginatedResponse
from ...services.health_service import HealthService
import asyncio
import random

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[HealthRecordPublic])
async def get_health_records(
    user_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 20,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    获取健康记录列表
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="必须提供用户ID")
    
    if start_date and end_date:
        # 按日期范围查询
        records = await health_service.get_by_date_range(
            db, 
            user_id=user_id, 
            start_date=start_date, 
            end_date=end_date
        )
        total = len(records)  # 简单处理，返回查询结果的长度
    else:
        # 默认查询
        records = await health_service.get_user_records(
            db, 
            user_id=user_id, 
            skip=skip, 
            limit=limit
        )
        # 获取总记录数
        total = await health_service.repository.count(
            db, 
            filters={"user_id": user_id}
        )
    
    return PaginatedResponse(
        data=records,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.post("/", response_model=DataResponse[HealthRecordPublic])
async def create_health_record(
    record: HealthRecordCreate, 
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    创建健康记录
    """
    db_record = await health_service.create_record(db, obj_in=record)
    return DataResponse(data=db_record, message="健康记录创建成功")

@router.get("/{record_id}", response_model=DataResponse[HealthRecordPublic])
async def get_health_record(
    record_id: int, 
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    通过ID获取健康记录
    """
    record = await health_service.get(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return DataResponse(data=record)

@router.put("/{record_id}", response_model=DataResponse[HealthRecordPublic])
async def update_health_record(
    record_id: int,
    record_update: HealthRecordUpdate,
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    更新健康记录
    """
    updated_record = await health_service.update_record(
        db, 
        record_id=record_id, 
        obj_in=record_update
    )
    
    if not updated_record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return DataResponse(data=updated_record, message="记录更新成功")

@router.delete("/{record_id}", response_model=DataResponse)
async def delete_health_record(
    record_id: int, 
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    删除健康记录
    """
    record = await health_service.delete(db, id=record_id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    return DataResponse(message="记录已删除")

@router.get("/statistics/{user_id}", response_model=DataResponse[HealthStatistics])
async def get_health_statistics(
    user_id: int,
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    获取用户健康统计数据
    """
    stats = await health_service.get_statistics(db, user_id=user_id, days=days)
    return DataResponse(data=stats)

@router.get("/summary/{user_id}/{year}/{month}", response_model=DataResponse[List[dict]])
async def get_monthly_summary(
    user_id: int,
    year: int,
    month: int,
    db: AsyncSession = Depends(get_async_db),
    health_service: HealthService = Depends()
):
    """
    获取用户月度健康记录摘要
    """
    summary = await health_service.get_monthly_summary(
        db, 
        user_id=user_id, 
        year=year, 
        month=month
    )
    
    return DataResponse(data=summary)

# WebSocket端点用于实时健康数据
@router.websocket("/ws/{user_id}")
async def health_data_websocket(websocket: WebSocket, user_id: int):
    """
    实时健康数据WebSocket
    """
    await websocket.accept()
    try:
        while True:
            # 模拟实时数据
            data = {
                "blood_pressure": f"{random.randint(110,140)}/{random.randint(70,90)}",
                "heart_rate": random.randint(60,100),
                "blood_sugar": round(random.uniform(4.0,7.0), 1),
                "timestamp": datetime.now().isoformat()
            }
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except:
        await websocket.close() 