from typing import List, Optional, Dict, Any, Union
from sqlalchemy.ext.asyncio import AsyncSession
import os
from datetime import datetime

from .base_service import BaseService
from ..models.course import Course
from ..repositories import course_repository
from ..schemas.course import CourseCreate, CourseUpdate
from ..core.config import settings

class CourseService(BaseService[Course, CourseCreate, CourseUpdate]):
    """
    课程服务，处理课程相关业务逻辑
    """
    
    def __init__(self):
        """
        初始化课程服务
        """
        super().__init__(course_repository)
    
    async def get_by_title(self, db: AsyncSession, title: str) -> Optional[Course]:
        """
        通过标题获取课程
        
        Args:
            db: 数据库会话
            title: 课程标题
            
        Returns:
            课程对象，如未找到返回None
        """
        return await self.repository.get_by_title(db, title)
    
    async def search(
        self, 
        db: AsyncSession, 
        *, 
        keyword: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        搜索课程
        
        Args:
            db: 数据库会话
            keyword: 搜索关键词
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        return await self.repository.search(db, keyword=keyword, skip=skip, limit=limit)
    
    async def get_by_difficulty(
        self, 
        db: AsyncSession, 
        *, 
        difficulty: str,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        获取指定难度的课程
        
        Args:
            db: 数据库会话
            difficulty: 难度级别
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        return await self.repository.get_by_difficulty(db, difficulty=difficulty, skip=skip, limit=limit)
    
    async def get_by_duration_range(
        self, 
        db: AsyncSession, 
        *, 
        min_duration: int,
        max_duration: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        获取指定时长范围内的课程
        
        Args:
            db: 数据库会话
            min_duration: 最小时长
            max_duration: 最大时长
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        return await self.repository.get_by_duration_range(
            db, 
            min_duration=min_duration, 
            max_duration=max_duration, 
            skip=skip, 
            limit=limit
        )
    
    async def get_by_instructor(
        self, 
        db: AsyncSession, 
        *, 
        instructor_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Course]:
        """
        获取指定讲师的课程
        
        Args:
            db: 数据库会话
            instructor_id: 讲师ID
            skip: 跳过的记录数
            limit: 返回的最大记录数
            
        Returns:
            课程列表
        """
        return await self.repository.get_by_instructor(
            db, 
            instructor_id=instructor_id, 
            skip=skip, 
            limit=limit
        )
    
    async def get_course_count_by_difficulty(self, db: AsyncSession) -> dict:
        """
        获取各难度级别的课程数量
        
        Args:
            db: 数据库会话
            
        Returns:
            各难度级别的课程数量字典
        """
        return await self.repository.get_course_count_by_difficulty(db)
    
    async def handle_file_upload(
        self, 
        file_type: str, 
        file_content: bytes, 
        filename: str
    ) -> str:
        """
        处理文件上传
        
        Args:
            file_type: 文件类型 (video/image)
            file_content: 文件内容
            filename: 文件名
            
        Returns:
            文件URL
        """
        # 验证文件类型
        if file_type not in ["video", "image"]:
            raise ValueError("不支持的文件类型")
        
        # 检查文件大小
        file_size = len(file_content)
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise ValueError("文件大小超过限制")
        
        # 创建上传目录
        upload_dir = os.path.join(settings.UPLOAD_DIR, file_type)
        os.makedirs(upload_dir, exist_ok=True)
        
        # 生成带时间戳的文件名，避免覆盖
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(upload_dir, new_filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # 返回文件URL
        return f"/uploads/{file_type}/{new_filename}" 