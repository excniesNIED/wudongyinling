from typing import List, Optional, Dict, Any, Union
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from .base_service import BaseService
from ..models.user import User
from ..repositories import user_repository
from ..schemas.user import UserCreate, UserUpdate, PasswordChange
from ..core.security import get_password_hash

class UserService(BaseService[User, UserCreate, UserUpdate]):
    """
    用户服务，处理用户管理相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化用户服务
        """
        super().__init__(user_repository)
    
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        """
        创建用户，处理密码哈希
        
        Args:
            db: 数据库会话
            obj_in: 用户创建数据
            
        Returns:
            创建的用户对象
        """
        # 将密码哈希化并准备数据
        create_data = obj_in.model_dump(exclude={'password'})
        create_data['hashed_password'] = get_password_hash(obj_in.password)
        
        # 确保role和is_admin字段的一致性
        from ..models.user import UserRole
        if hasattr(obj_in, 'role') and obj_in.role:
            create_data['role'] = obj_in.role
            # 设置is_admin字段以保持向后兼容
            create_data['is_admin'] = (obj_in.role == UserRole.ADMIN)
        else:
            # 如果没有设置role，根据is_admin设置role
            if getattr(obj_in, 'is_admin', False):
                create_data['role'] = UserRole.ADMIN
            else:
                create_data['role'] = UserRole.ELDERLY
                
        # 生成唯一用户ID
        create_data['unique_id'] = await self._generate_unique_id(create_data['role'])
        
        # 使用User模型创建用户
        db_obj = User(**create_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_by_email(
        self, 
        db: AsyncSession, 
        email: str
    ) -> Optional[User]:
        """
        通过电子邮箱获取用户
        
        Args:
            db: 数据库会话
            email: 电子邮箱
            
        Returns:
            用户对象，如未找到返回None
        """
        return await self.repository.get_by_email(db, email)
    
    async def get_by_username(
        self, 
        db: AsyncSession, 
        username: str
    ) -> Optional[User]:
        """
        通过用户名获取用户
        
        Args:
            db: 数据库会话
            username: 用户名
            
        Returns:
            用户对象，如未找到返回None
        """
        return await self.repository.get_by_username(db, username)
    
    async def get_active_users(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        获取活跃用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            活跃用户列表
        """
        return await self.repository.get_active_users(db, skip, limit)
    
    async def get_admin_users(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[User]:
        """
        获取管理员用户列表
        
        Args:
            db: 数据库会话
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            管理员用户列表
        """
        return await self.repository.get_admin_users(db, skip, limit)
    
    async def update_profile(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        user_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Optional[User]:
        """
        更新用户资料
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            user_in: 更新数据
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        return await self.repository.update(db, db_obj=user, obj_in=user_in)
    
    async def activate_user(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int
    ) -> Optional[User]:
        """
        激活用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        update_data = {"is_active": True}
        return await self.repository.update(db, db_obj=user, obj_in=update_data)
    
    async def deactivate_user(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int
    ) -> Optional[User]:
        """
        停用用户
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        update_data = {"is_active": False}
        return await self.repository.update(db, db_obj=user, obj_in=update_data)
    
    async def set_admin_status(
        self, 
        db: AsyncSession, 
        *, 
        user_id: int, 
        is_admin: bool
    ) -> Optional[User]:
        """
        设置用户管理员状态
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            is_admin: 是否为管理员
            
        Returns:
            更新后的用户对象，如未找到返回None
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return None
            
        update_data = {"is_admin": is_admin}
        return await self.repository.update(db, db_obj=user, obj_in=update_data)
    
    async def is_active(
        self, 
        db: AsyncSession, 
        *, 
        user: User
    ) -> bool:
        """
        检查用户是否活跃
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            用户是否活跃
        """
        return await self.repository.is_active(user)
    
    async def is_admin(
        self, 
        db: AsyncSession, 
        *, 
        user: User
    ) -> bool:
        """
        检查用户是否是管理员
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            用户是否是管理员
        """
        return await self.repository.is_admin(user)
    
    async def change_password(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        password_data: PasswordChange
    ) -> bool:
        """
        修改用户密码
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            password_data: 密码修改数据
            
        Returns:
            修改是否成功
            
        Raises:
            ValueError: 当前密码错误或其他验证失败
        """
        # 获取用户
        user = await self.repository.get(db, user_id)
        if not user:
            raise ValueError("用户不存在")
        
        # 初始化密码上下文
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # 验证当前密码
        if not pwd_context.verify(password_data.current_password, user.hashed_password):
            raise ValueError("当前密码错误")
        
        # 生成新密码哈希
        new_hashed_password = pwd_context.hash(password_data.new_password)
        
        # 直接更新用户密码
        user.hashed_password = new_hashed_password
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        return True
    
    async def _generate_unique_id(self, role) -> str:
        """
        根据角色生成唯一用户ID
        
        Args:
            role: 用户角色
            
        Returns:
            唯一用户ID字符串
        """
        import time
        import random
        from ..models.user import UserRole
        
        # 根据角色确定前缀
        prefix_map = {
            UserRole.ELDERLY: 'E',    # 老年人
            UserRole.CHILD: 'C',      # 子女
            UserRole.VOLUNTEER: 'V',  # 志愿者
            UserRole.TEACHER: 'T',    # 教师
            UserRole.DOCTOR: 'D',     # 医生
            UserRole.ADMIN: 'A'       # 管理员
        }
        
        prefix = prefix_map.get(role, 'E')
        
        # 生成基于时间戳和随机数的唯一ID
        timestamp = str(int(time.time()))[-6:]  # 取时间戳后6位
        random_num = str(random.randint(100, 999))  # 3位随机数
        
        return f"{prefix}{timestamp}{random_num}"

    async def get_active_users(self, db: AsyncSession, since_date) -> List[User]:
        """
        获取指定日期以来的活跃用户
        
        Args:
            db: 数据库会话
            since_date: 起始日期
            
        Returns:
            活跃用户列表
        """
        return await self.repository.get_active_users_since(db, since_date)

    async def get_registration_trend(self, db: AsyncSession, start_date) -> List[Dict[str, Any]]:
        """
        获取用户注册趋势
        
        Args:
            db: 数据库会话
            start_date: 开始日期
            
        Returns:
            用户注册趋势数据
        """
        return await self.repository.get_registration_trend(db, start_date)

    async def get_user_activity_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """
        获取用户活跃度统计
        
        Args:
            db: 数据库会话
            
        Returns:
            用户活跃度统计信息
        """
        return await self.repository.get_user_activity_stats(db)

    async def get_role_distribution(self, db: AsyncSession) -> Dict[str, Any]:
        """
        获取用户角色分布统计
        
        Args:
            db: 数据库会话
            
        Returns:
            用户角色分布统计
        """
        return await self.repository.get_role_distribution(db)

    async def get_by_date_range(
        self,
        db: AsyncSession,
        start_date: date,
        end_date: date,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """
        获取指定日期范围内注册的用户
        
        Args:
            db: 数据库会话
            start_date: 开始日期
            end_date: 结束日期
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            用户列表
        """
        return await self.repository.get_by_date_range(db, start_date, end_date, skip, limit)

    async def reset_user_password(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        password: str
    ) -> bool:
        """
        重置用户密码（管理员操作）
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            password: 新密码
            
        Returns:
            重置是否成功
        """
        user = await self.repository.get(db, user_id)
        if not user:
            return False
        
        # 生成新密码哈希
        from ..core.security import get_password_hash
        new_hashed_password = get_password_hash(password)
        
        # 更新用户密码
        update_data = {"hashed_password": new_hashed_password}
        await self.repository.update(db, db_obj=user, obj_in=update_data)
        
        return True 