from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from jose import jwt

from ..core.config import settings
from ..models.user import User
from ..repositories import user_repository
from ..schemas.user import UserCreate, UserUpdate, TokenResponse, UserPublic

class AuthService:
    """
    认证服务，处理用户认证、注册和令牌生成
    """
    
    def __init__(self):
        """
        初始化认证服务
        """
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        验证密码
        
        Args:
            plain_password: 明文密码
            hashed_password: 哈希密码
            
        Returns:
            验证是否成功
        """
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """
        获取密码哈希
        
        Args:
            password: 明文密码
            
        Returns:
            密码哈希
        """
        return self.pwd_context.hash(password)
    
    def create_access_token(
        self, 
        subject: int, 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        创建访问令牌
        
        Args:
            subject: 令牌主题（通常是用户ID）
            expires_delta: 有效期
            
        Returns:
            JWT令牌
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode = {"exp": expire, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    async def authenticate_user(
        self, 
        db: AsyncSession, 
        username: str, 
        password: str
    ) -> Optional[User]:
        """
        用户认证
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            认证成功返回用户对象，否则返回None
        """
        user = await user_repository.get_by_username(db, username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user
    
    async def login(
        self, 
        db: AsyncSession, 
        username: str, 
        password: str
    ) -> Optional[TokenResponse]:
        """
        用户登录
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            登录成功返回令牌信息，否则返回None
        """
        user = await self.authenticate_user(db, username, password)
        if not user:
            return None
            
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            subject=user.id,
            expires_delta=access_token_expires
        )
        
        # 确保role和unique_id有值
        from ..models.user import UserRole
        user_role = user.role if hasattr(user, 'role') and user.role else (UserRole.ADMIN if user.is_admin else UserRole.ELDERLY)
        user_unique_id = user.unique_id if hasattr(user, 'unique_id') and user.unique_id else f"{'A' if user.is_admin else 'U'}{user.id:06d}"
        
        # 构建UserPublic对象
        user_data = UserPublic(
            id=user.id,
            username=user.username,
            email=user.email,
            nickname=user.nickname if hasattr(user, 'nickname') else None,
            avatar=user.avatar if hasattr(user, 'avatar') else None,
            is_active=user.is_active,
            is_admin=user.is_admin,
            role=user_role,
            unique_id=user_unique_id,
            created_at=user.created_at
        )
        
        # 构建令牌响应
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=user_data
        )
    
    async def register(
        self, 
        db: AsyncSession, 
        user_in: UserCreate
    ) -> User:
        """
        用户注册
        
        Args:
            db: 数据库会话
            user_in: 用户信息
            
        Returns:
            注册成功的用户对象
        """
        # 检查用户名是否已存在
        existing_user = await user_repository.get_by_username(db, user_in.username)
        if existing_user:
            raise ValueError("用户名已被使用")
            
        # 检查邮箱是否已存在
        existing_email = await user_repository.get_by_email(db, user_in.email)
        if existing_email:
            raise ValueError("邮箱已被注册")
            
        # 哈希密码
        hashed_password = self.get_password_hash(user_in.password)
        
        # 准备用户数据
        user_data = user_in.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password
        
        # 确保role和is_admin字段的一致性
        from ..models.user import UserRole
        if hasattr(user_in, 'role') and user_in.role:
            user_data['role'] = user_in.role
            user_data['is_admin'] = (user_in.role == UserRole.ADMIN)
        else:
            if getattr(user_in, 'is_admin', False):
                user_data['role'] = UserRole.ADMIN
            else:
                user_data['role'] = UserRole.ELDERLY
        
        # 生成唯一用户ID
        import time
        import random
        prefix_map = {
            UserRole.ELDERLY: 'E',
            UserRole.CHILD: 'C',
            UserRole.VOLUNTEER: 'V',
            UserRole.TEACHER: 'T',
            UserRole.DOCTOR: 'D',
            UserRole.ADMIN: 'A'
        }
        prefix = prefix_map.get(user_data['role'], 'E')
        timestamp = str(int(time.time()))[-6:]
        random_num = str(random.randint(100, 999))
        user_data['unique_id'] = f"{prefix}{timestamp}{random_num}"
        
        # 直接使用User模型创建用户，而非通过repository
        user = User(**user_data)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user 