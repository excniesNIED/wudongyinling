from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from .base_service import BaseService
from ..repositories.social import (
    PostRepository, PostCommentRepository, PostLikeRepository,
    HeritageProjectRepository, HeritageInheritorRepository
)
from ..schemas.social import (
    PostCreate, PostUpdate, PostPublic, PostWithUser,
    PostCommentCreate, PostCommentUpdate, PostCommentPublic, PostCommentWithUser,
    PostLikeCreate, PostLikePublic,
    HeritageProjectCreate, HeritageProjectUpdate, HeritageProjectPublic, HeritageProjectWithInheritor,
    HeritageInheritorCreate, HeritageInheritorUpdate, HeritageInheritorPublic, HeritageInheritorWithProjects
)
from ..models.social import Post, PostComment, PostLike, HeritageProject, HeritageInheritor
from ..core.database import AsyncSessionLocal


class PostService(BaseService[Post, PostCreate, PostUpdate]):
    """动态服务"""
    
    def __init__(self):
        self.repository = PostRepository()
    
    async def create_post(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: PostCreate, 
        user_id: int
    ) -> Post:
        """创建动态"""
        create_data = obj_in.model_dump()
        create_data['user_id'] = user_id
        
        post = Post(**create_data)
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return post
    
    async def get_posts_with_user(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        post_type: Optional[str] = None,
        user_role: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        user_id: Optional[int] = None
    ) -> List[Post]:
        """获取带用户信息的动态列表"""
        return await self.repository.get_posts_with_user(
            db, skip, limit, post_type, user_role, is_public, is_featured, user_id
        )
    
    async def get_posts_by_user(
        self, 
        db: AsyncSession, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[Post]:
        """获取用户的动态列表"""
        return await self.repository.get_posts_by_user(db, user_id, skip, limit)
    
    async def toggle_featured(self, db: AsyncSession, post_id: int) -> Optional[Post]:
        """切换精选状态"""
        return await self.repository.toggle_featured(db, post_id)
    
    async def toggle_visibility(self, db: AsyncSession, post_id: int) -> Optional[Post]:
        """切换可见性"""
        return await self.repository.toggle_visibility(db, post_id)
    
    async def like_post(self, db: AsyncSession, post_id: int, user_id: int) -> bool:
        """点赞动态"""
        like_repo = PostLikeRepository()
        existing_like = await like_repo.get_like_by_user_and_post(db, user_id, post_id)
        
        if existing_like:
            # 已点赞，取消点赞
            await like_repo.delete_like(db, user_id, post_id)
            await self.repository.decrement_likes_count(db, post_id)
            return False
        else:
            # 未点赞，添加点赞
            await like_repo.create_like(db, user_id, post_id)
            await self.repository.increment_likes_count(db, post_id)
            return True
    
    async def get_total_count(
        self,
        db: AsyncSession,
        post_type: Optional[str] = None,
        user_role: Optional[str] = None,
        is_public: Optional[bool] = None,
        is_featured: Optional[bool] = None,
        user_id: Optional[int] = None
    ) -> int:
        """获取动态总数"""
        return await self.repository.get_total_count(
            db=db,
            post_type=post_type,
            user_role=user_role,
            is_public=is_public,
            is_featured=is_featured,
            user_id=user_id
        )


class PostCommentService(BaseService[PostComment, PostCommentCreate, PostCommentUpdate]):
    """动态评论服务"""
    
    def __init__(self):
        self.repository = PostCommentRepository()
    
    async def create_comment(
        self, 
        db: AsyncSession, 
        *, 
        obj_in: PostCommentCreate, 
        user_id: int
    ) -> PostComment:
        """创建评论"""
        create_data = obj_in.model_dump()
        create_data['user_id'] = user_id
        
        comment = PostComment(**create_data)
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        
        # 增加动态的评论数
        post_repo = PostRepository()
        await post_repo.increment_comments_count(db, obj_in.post_id)
        
        return comment
    
    async def get_comments_by_post(
        self, 
        db: AsyncSession, 
        post_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[PostComment]:
        """获取动态的评论列表"""
        return await self.repository.get_comments_by_post(db, post_id, skip, limit)
    
    async def get_replies_by_comment(
        self, 
        db: AsyncSession, 
        comment_id: int
    ) -> List[PostComment]:
        """获取评论的回复列表"""
        return await self.repository.get_replies_by_comment(db, comment_id)
    
    async def delete_comment(self, db: AsyncSession, comment_id: int) -> bool:
        """删除评论"""
        comment = await self.repository.get(db, comment_id)
        if comment:
            # 减少动态的评论数
            post_repo = PostRepository()
            await post_repo.decrement_comments_count(db, comment.post_id)
            
            # 删除评论
            await self.repository.remove(db, id=comment_id)
            return True
        return False


class HeritageProjectService(BaseService[HeritageProject, HeritageProjectCreate, HeritageProjectUpdate]):
    """非遗项目服务"""
    
    def __init__(self):
        self.repository = HeritageProjectRepository()
    
    async def get_projects_with_inheritor(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = None,
        keyword: Optional[str] = None
    ) -> List[HeritageProject]:
        """获取带传承人信息的项目列表"""
        return await self.repository.get_projects_with_inheritor(
            db=db,
            skip=skip,
            limit=limit,
            category=category,
            level=level,
            is_active=is_active,
            keyword=keyword
        )
    
    async def get_projects_by_inheritor(
        self, 
        db: AsyncSession, 
        inheritor_id: int
    ) -> List[HeritageProject]:
        """获取传承人的项目列表"""
        return await self.repository.get_projects_by_inheritor(db, inheritor_id)
    
    async def toggle_active_status(self, db: AsyncSession, project_id: int) -> Optional[HeritageProject]:
        """切换项目启用状态"""
        return await self.repository.toggle_active_status(db, project_id)
    
    async def get_total_count(
        self,
        db: AsyncSession,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        level: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """获取项目总数"""
        return await self.repository.get_total_count(
            db=db,
            keyword=keyword,
            category=category,
            level=level,
            is_active=is_active
        )

    async def get_projects_with_inheritors(
        self,
        skip: int = 0,
        limit: int = 20,
        keyword: Optional[str] = None,
        category: Optional[str] = None,
        level: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[HeritageProject]:
        """获取项目列表（带传承人）"""
        async with AsyncSessionLocal() as db:
            try:
                return await self.repository.get_projects_with_inheritors(
                    db=db,
                    skip=skip,
                    limit=limit,
                    keyword=keyword,
                    category=category,
                    level=level,
                    status=status
                )
            except Exception as e:
                await db.rollback()
                raise

    async def toggle_status(self, project_id: int) -> Optional[HeritageProject]:
        """切换项目状态"""
        async with AsyncSessionLocal() as db:
            try:
                return await self.repository.toggle_project_status(db=db, project_id=project_id)
            except Exception as e:
                await db.rollback()
                raise


class PostLikeService:
    """动态点赞服务"""
    
    def __init__(self):
        self.repository = PostLikeRepository()
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> List[PostLike]:
        """获取用户的所有点赞"""
        return await self.repository.get_likes_by_user(db, user_id)


class HeritageInheritorService(BaseService[HeritageInheritor, HeritageInheritorCreate, HeritageInheritorUpdate]):
    """传承人服务"""
    
    def __init__(self):
        self.repository = HeritageInheritorRepository()
    
    async def get_inheritors_with_projects(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        gender: Optional[str] = None,
        hometown: Optional[str] = None,
        is_active: Optional[bool] = None,
        keyword: Optional[str] = None
    ) -> List[HeritageInheritor]:
        """获取带项目信息的传承人列表"""
        return await self.repository.get_inheritors_with_projects(
            db=db,
            skip=skip,
            limit=limit,
            keyword=keyword,
            hometown=hometown,
            gender=gender,
            is_active=is_active
        )
    
    async def toggle_active_status(self, db: AsyncSession, inheritor_id: int) -> Optional[HeritageInheritor]:
        """切换传承人启用状态"""
        return await self.repository.toggle_active_status(db, inheritor_id)
    
    async def get_total_count(
        self,
        db: AsyncSession,
        keyword: Optional[str] = None,
        hometown: Optional[str] = None,
        gender: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> int:
        """获取传承人总数"""
        return await self.repository.get_total_count(
            db=db,
            keyword=keyword,
            hometown=hometown,
            gender=gender,
            is_active=is_active
        )

    async def get_inheritors_with_projects(
        self,
        skip: int = 0,
        limit: int = 20,
        keyword: Optional[str] = None,
        hometown: Optional[str] = None,
        gender: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[HeritageInheritor]:
        """获取传承人列表（带项目）"""
        async with AsyncSessionLocal() as db:
            try:
                return await self.repository.get_inheritors_with_projects(
                    db=db,
                    skip=skip,
                    limit=limit,
                    keyword=keyword,
                    hometown=hometown,
                    gender=gender,
                    status=status
                )
            except Exception as e:
                await db.rollback()
                raise

    async def toggle_status(self, inheritor_id: int) -> Optional[HeritageInheritor]:
        """切换传承人状态"""
        async with AsyncSessionLocal() as db:
            try:
                return await self.repository.toggle_inheritor_status(db=db, inheritor_id=inheritor_id)
            except Exception as e:
                await db.rollback()
                raise


class SocialService:
    """
    社交服务主类，包装所有社交相关服务
    """
    
    def __init__(self):
        self.post_service = PostService()
        self.comment_service = PostCommentService()
        self.like_service = PostLikeService()
        self.heritage_project_service = HeritageProjectService()
        self.heritage_inheritor_service = HeritageInheritorService()
        self.repository = self.post_service.repository  # 为了兼容性

    async def get_user_activity_stats(
        self,
        db: AsyncSession,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        获取用户社交活动统计
        
        Args:
            db: 数据库会话
            user_id: 用户ID
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            用户社交活动统计信息
        """
        # 获取用户的动态统计
        user_posts = await self.post_service.repository.get_by_user_id(db, user_id)
        user_comments = await self.comment_service.repository.get_by_user_id(db, user_id)
        user_likes = await self.like_service.repository.get_by_user_id(db, user_id)
        
        # 按日期范围过滤
        if start_date and end_date:
            user_posts = [p for p in user_posts if start_date <= p.created_at.date() <= end_date]
            user_comments = [c for c in user_comments if start_date <= c.created_at.date() <= end_date]
            user_likes = [l for l in user_likes if start_date <= l.created_at.date() <= end_date]
        
        return {
            "totalPosts": len(user_posts),
            "totalComments": len(user_comments),
            "totalLikes": len(user_likes),
            "receivedLikes": sum([p.like_count or 0 for p in user_posts]),
            "period": {
                "startDate": start_date.isoformat() if start_date else None,
                "endDate": end_date.isoformat() if end_date else None
            }
        } 