from datetime import datetime, date
from typing import Optional, List
from pydantic import EmailStr, Field, validator

from .base import BaseSchema
from ..models.user import UserRole, Gender

class UserBase(BaseSchema):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="电子邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    gender: Optional[Gender] = Field(None, description="性别")
    birthdate: Optional[date] = Field(None, description="出生日期")
    role: Optional[UserRole] = Field(UserRole.ELDERLY, description="用户角色")
    
    # 健康相关字段
    medical_history: Optional[str] = Field(None, description="病史")
    chronic_diseases: Optional[str] = Field(None, description="慢性病")
    emergency_contact: Optional[str] = Field(None, max_length=100, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")
    
    @validator('phone')
    def validate_phone(cls, v):
        """验证手机号格式"""
        import re
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('请输入正确的手机号码')
        return v

class UserCreate(UserBase):
    """创建用户的请求模型"""
    password: str = Field(..., min_length=6, description="密码")
    is_admin: Optional[bool] = Field(False, description="是否管理员")
    is_active: Optional[bool] = Field(True, description="是否激活")
    role: Optional[UserRole] = Field(UserRole.ELDERLY, description="用户角色")
    
    @validator('password')
    def password_complexity(cls, v):
        """验证密码复杂度"""
        if len(v) < 6:
            raise ValueError('密码长度至少为6位')
        # 可以添加更多密码复杂度验证逻辑
        return v

class UserUpdate(BaseSchema):
    """更新用户的请求模型"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="电子邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, description="头像URL")
    gender: Optional[Gender] = Field(None, description="性别")
    birthdate: Optional[date] = Field(None, description="出生日期")
    password: Optional[str] = Field(None, min_length=8, description="密码")
    is_active: Optional[bool] = Field(None, description="是否激活")
    role: Optional[UserRole] = Field(None, description="用户角色")
    
    # 健康相关字段
    medical_history: Optional[str] = Field(None, description="病史")
    chronic_diseases: Optional[str] = Field(None, description="慢性病")
    emergency_contact: Optional[str] = Field(None, max_length=100, description="紧急联系人")
    emergency_phone: Optional[str] = Field(None, max_length=20, description="紧急联系电话")

class UserInDB(UserBase):
    """数据库中的用户模型"""
    id: int = Field(..., description="用户ID")
    hashed_password: str = Field(..., description="哈希密码")
    is_active: bool = Field(True, description="是否激活")
    is_admin: bool = Field(False, description="是否管理员")
    role: UserRole = Field(UserRole.ELDERLY, description="用户角色")
    unique_id: str = Field(..., description="唯一用户标识")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

class UserPublic(UserBase):
    """返回给客户端的用户模型"""
    id: int = Field(..., description="用户ID")
    is_active: bool = Field(..., description="是否激活")
    is_admin: bool = Field(..., description="是否管理员")
    role: UserRole = Field(..., description="用户角色")
    unique_id: str = Field(..., description="唯一用户标识")
    created_at: datetime = Field(..., description="创建时间")

class UserLogin(BaseSchema):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class PasswordChange(BaseSchema):
    """修改密码请求模型"""
    current_password: str = Field(..., description="当前密码")
    new_password: str = Field(..., min_length=6, description="新密码")
    confirm_password: str = Field(..., description="确认新密码")
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        """验证两次输入的密码是否一致"""
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('两次输入的密码不一致')
        return v

class TokenResponse(BaseSchema):
    """登录响应模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    user: UserPublic = Field(..., description="用户信息") 