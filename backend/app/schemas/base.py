from datetime import datetime
from typing import Generic, TypeVar, List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

T = TypeVar('T')

class BaseSchema(BaseModel):
    """所有Pydantic模型的基类"""
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.isoformat()}
    )

class BaseAPIResponse(BaseModel):
    """API响应的基础格式"""
    code: int = Field(0, description="状态码，0表示成功")
    message: str = Field("success", description="响应消息")

class DataResponse(BaseAPIResponse, Generic[T]):
    """单个数据响应格式"""
    data: Optional[T] = Field(default=None, description="响应数据")

class ListResponse(BaseAPIResponse, Generic[T]):
    """列表数据响应格式"""
    data: List[T] = Field(default_factory=list, description="数据列表")

class PaginatedResponse(BaseAPIResponse, Generic[T]):
    """分页响应格式"""
    data: List[T] = Field(default_factory=list, description="数据列表")
    total: int = Field(0, description="总记录数")
    page: int = Field(1, description="当前页码")
    page_size: int = Field(10, description="每页记录数")

class Token(BaseSchema):
    """Token模型"""
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field("bearer", description="令牌类型")
    expires_in: int = Field(..., description="有效期(秒)")

class TokenPayload(BaseSchema):
    """Token负载数据"""
    sub: int = Field(..., description="用户ID")
    exp: datetime = Field(..., description="过期时间") 