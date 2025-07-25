from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ...core.database import get_async_db
from ...schemas.user import UserCreate, UserUpdate, UserPublic
from ...schemas.base import DataResponse, ListResponse
from ...services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=ListResponse[UserPublic])
async def get_users(
    skip: int = 0, 
    limit: int = 10, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    获取用户列表
    """
    users = await user_service.get_multi(db, skip=skip, limit=limit)
    total = await user_service.repository.count(db)
    
    return ListResponse(
        data=users,
        total=total,
        page=skip // limit + 1 if limit else 1,
        page_size=limit
    )

@router.get("/{user_id}", response_model=DataResponse[UserPublic])
async def get_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    通过ID获取用户信息
    """
    user = await user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(data=user)

@router.put("/{user_id}", response_model=DataResponse[UserPublic])
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    更新用户信息
    """
    user = await user_service.get(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    updated_user = await user_service.update_profile(
        db, 
        user_id=user_id, 
        user_in=user_update
    )
    
    return DataResponse(data=updated_user)

@router.delete("/{user_id}", response_model=DataResponse)
async def delete_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    删除用户
    """
    user = await user_service.delete(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(message="用户已删除")

@router.patch("/{user_id}/activate", response_model=DataResponse[UserPublic])
async def activate_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    激活用户
    """
    user = await user_service.activate_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(data=user, message="用户已激活")

@router.patch("/{user_id}/deactivate", response_model=DataResponse[UserPublic])
async def deactivate_user(
    user_id: int, 
    db: AsyncSession = Depends(get_async_db),
    user_service: UserService = Depends()
):
    """
    停用用户
    """
    user = await user_service.deactivate_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return DataResponse(data=user, message="用户已停用") 