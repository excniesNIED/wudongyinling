from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...dependencies import get_async_db
from ...services.social_service import (
    PostService, PostCommentService, 
    HeritageProjectService, HeritageInheritorService
)
from ...core.response import DataResponse, PaginatedResponse, success_response, error_response, paginated_response
from ...core.exceptions import NotFoundException, BusinessException

# 创建服务实例
def get_post_service() -> PostService:
    return PostService()

def get_post_comment_service() -> PostCommentService:
    return PostCommentService()

def get_heritage_project_service() -> HeritageProjectService:
    return HeritageProjectService()

def get_heritage_inheritor_service() -> HeritageInheritorService:
    return HeritageInheritorService()

from ...schemas.base import DataResponse, PaginatedResponse
from ...schemas.social import (
    PostCreate, PostUpdate, PostPublic, PostWithUser,
    PostCommentCreate, PostCommentUpdate, PostCommentPublic, PostCommentWithUser,
    PostLikeCreate, PostLikePublic,
    HeritageProjectCreate, HeritageProjectUpdate, HeritageProjectPublic, HeritageProjectWithInheritor,
    HeritageInheritorCreate, HeritageInheritorUpdate, HeritageInheritorPublic, HeritageInheritorWithProjects
)

router = APIRouter()

# ===================== 动态管理 =====================

@router.get("/posts", response_model=PaginatedResponse[PostPublic])
async def get_posts(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    post_type: Optional[str] = Query(None, description="动态类型"),
    user_role: Optional[str] = Query(None, description="用户角色"),
    is_public: Optional[bool] = Query(None, description="是否公开"),
    is_featured: Optional[bool] = Query(None, description="是否精选"),
    user_id: Optional[int] = Query(None, description="用户ID"),
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    获取动态列表
    """
    posts = await post_service.get_posts_with_user(
        db, skip, limit, post_type, user_role, is_public, is_featured, user_id
    )
    total = await post_service.get_total_count(
        db, post_type, user_role, is_public, is_featured, user_id
    )
    
    return PaginatedResponse(
        data=[PostPublic.model_validate(post) for post in posts],
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/posts/{post_id}", response_model=DataResponse[PostPublic])
async def get_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    获取单个动态详情
    """
    post = await post_service.get(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    return DataResponse(data=post, message="获取成功")


@router.post("/posts", response_model=DataResponse[PostPublic])
async def create_post(
    post_data: PostCreate,
    user_id: int = Query(..., description="用户ID"),  # 临时用query参数，实际应该从token获取
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    创建动态
    """
    post = await post_service.create_post(db, obj_in=post_data, user_id=user_id)
    return DataResponse(data=post, message="动态发布成功")


@router.put("/posts/{post_id}", response_model=DataResponse[PostPublic])
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    更新动态
    """
    post = await post_service.get(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    updated_post = await post_service.update(db, db_obj=post, obj_in=post_data)
    return DataResponse(data=updated_post, message="动态更新成功")


@router.patch("/posts/{post_id}/featured", response_model=DataResponse[PostPublic])
async def toggle_post_featured(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    切换动态精选状态
    """
    post = await post_service.toggle_featured(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    return DataResponse(
        data=post, 
        message=f"动态已{'设为精选' if post.is_featured else '取消精选'}"
    )


@router.patch("/posts/{post_id}/visibility", response_model=DataResponse[PostPublic])
async def toggle_post_visibility(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    切换动态可见性
    """
    post = await post_service.toggle_visibility(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    return DataResponse(
        data=post, 
        message=f"动态已设为{'公开' if post.is_public else '私密'}"
    )


@router.post("/posts/{post_id}/like", response_model=DataResponse)
async def toggle_post_like(
    post_id: int,
    user_id: int = Query(..., description="用户ID"),  # 临时用query参数，实际应该从token获取
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    点赞/取消点赞动态
    """
    is_liked = await post_service.like_post(db, post_id, user_id)
    return DataResponse(
        data={"is_liked": is_liked},
        message="点赞成功" if is_liked else "取消点赞成功"
    )


@router.delete("/posts/{post_id}", response_model=DataResponse)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_async_db),
    post_service: PostService = Depends(get_post_service)
):
    """
    删除动态
    """
    success = await post_service.remove(db, id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="动态不存在")
    
    return DataResponse(message="动态删除成功")


# ===================== 动态评论管理 =====================

@router.get("/posts/{post_id}/comments", response_model=DataResponse[List[PostCommentPublic]])
async def get_post_comments(
    post_id: int,
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(50, ge=1, le=100, description="每页记录数"),
    db: AsyncSession = Depends(get_async_db),
    comment_service: PostCommentService = Depends(get_post_comment_service)
):
    """
    获取动态评论列表
    """
    comments = await comment_service.get_comments_by_post(db, post_id, skip, limit)
    return DataResponse(data=comments, message="获取成功")


@router.post("/posts/comments", response_model=DataResponse[PostCommentPublic])
async def create_comment(
    comment_data: PostCommentCreate,
    user_id: int = Query(..., description="用户ID"),  # 临时用query参数，实际应该从token获取
    db: AsyncSession = Depends(get_async_db),
    comment_service: PostCommentService = Depends(get_post_comment_service)
):
    """
    创建评论
    """
    comment = await comment_service.create_comment(db, obj_in=comment_data, user_id=user_id)
    return DataResponse(data=comment, message="评论发布成功")


@router.delete("/posts/comments/{comment_id}", response_model=DataResponse)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_async_db),
    comment_service: PostCommentService = Depends(get_post_comment_service)
):
    """
    删除评论
    """
    success = await comment_service.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="评论不存在")
    
    return DataResponse(message="评论删除成功")


# ===================== 非遗项目管理 =====================

@router.get("/heritage/projects", response_model=PaginatedResponse[HeritageProjectPublic])
async def get_heritage_projects(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    category: Optional[str] = Query(None, description="项目类别"),
    level: Optional[str] = Query(None, description="保护级别"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    获取非遗项目列表
    """
    projects = await project_service.get_projects_with_inheritor(
        db, skip, limit, category, level, is_active, keyword
    )
    total = await project_service.get_total_count(
        db, keyword, category, level, is_active
    )
    
    return PaginatedResponse(
        data=[HeritageProjectPublic.model_validate(project) for project in projects],
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/heritage/projects/{project_id}", response_model=DataResponse[HeritageProjectPublic])
async def get_heritage_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    获取单个非遗项目详情
    """
    project = await project_service.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="非遗项目不存在")
    
    return DataResponse(data=project, message="获取成功")


@router.post("/heritage/projects", response_model=DataResponse[HeritageProjectPublic])
async def create_heritage_project(
    project_data: HeritageProjectCreate,
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    创建非遗项目
    """
    # 创建非遗项目
    project = await project_service.create(db, obj_in=project_data)
    
    # 自动创建对应的群聊
    try:
        from ...services.chat_service import ChatService
        from ...schemas.chat import ChatRoomCreate
        
        chat_service = ChatService()
        
        # 创建群聊数据
        room_data = ChatRoomCreate(
            name=f"{project.name} - 传承群",
            description=f"欢迎加入{project.name}非遗传承交流群，一起学习和传承这项珍贵的文化遗产！",
            room_type="heritage",
            is_public=True,
            max_members=200,
            creator_id=1,  # 系统创建者
            member_ids=[1],  # 系统用户
            heritage_project_id=project.id  # 关联非遗项目
        )
        
        # 创建群聊
        room = await chat_service.create_room(db, room_in=room_data)
        
        # 更新项目关联群聊ID
        await project_service.update(
            db, 
            db_obj=project, 
            obj_in={"chat_room_id": room.id}
        )
        
    except Exception as e:
        # 群聊创建失败不影响项目创建
        print(f"Failed to create chat room for heritage project {project.id}: {e}")
    
    return DataResponse(data=project, message="非遗项目创建成功")


@router.put("/heritage/projects/{project_id}", response_model=DataResponse[HeritageProjectPublic])
async def update_heritage_project(
    project_id: int,
    project_data: HeritageProjectUpdate,
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    更新非遗项目
    """
    project = await project_service.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="非遗项目不存在")
    
    updated_project = await project_service.update(db, db_obj=project, obj_in=project_data)
    return DataResponse(data=updated_project, message="非遗项目更新成功")


@router.patch("/heritage/projects/{project_id}/status", response_model=DataResponse[HeritageProjectPublic])
async def toggle_heritage_project_status(
    project_id: int,
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    切换非遗项目启用状态
    注意：toggle_status方法内部管理数据库会话
    """
    project = await project_service.toggle_status(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="非遗项目不存在")
    
    return DataResponse(
        data=project,
        message=f"项目已{'启用' if project.status == 'active' else '停用'}"
    )


@router.delete("/heritage/projects/{project_id}", response_model=DataResponse)
async def delete_heritage_project(
    project_id: int,
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    删除非遗项目
    """
    success = await project_service.remove(db, id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="非遗项目不存在")
    
    return DataResponse(message="非遗项目删除成功")


# ===================== 非遗传承人管理 =====================

@router.get("/heritage/inheritors", response_model=PaginatedResponse[HeritageInheritorPublic])
async def get_heritage_inheritors(
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(20, ge=1, le=100, description="每页记录数"),
    gender: Optional[str] = Query(None, description="性别"),
    hometown: Optional[str] = Query(None, description="籍贯"),
    is_active: Optional[bool] = Query(None, description="是否启用"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    db: AsyncSession = Depends(get_async_db),
    inheritor_service: HeritageInheritorService = Depends(get_heritage_inheritor_service)
):
    """
    获取非遗传承人列表
    """
    inheritors = await inheritor_service.get_inheritors_with_projects(
        db, skip, limit, gender, hometown, is_active, keyword
    )
    total = await inheritor_service.get_total_count(
        db, keyword, hometown, gender, is_active
    )
    
    return PaginatedResponse(
        data=[HeritageInheritorPublic.model_validate(inheritor) for inheritor in inheritors],
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/heritage/inheritors/{inheritor_id}", response_model=DataResponse[HeritageInheritorPublic])
async def get_heritage_inheritor(
    inheritor_id: int,
    db: AsyncSession = Depends(get_async_db),
    inheritor_service: HeritageInheritorService = Depends(get_heritage_inheritor_service)
):
    """
    获取单个非遗传承人详情
    """
    inheritor = await inheritor_service.get(db, inheritor_id)
    if not inheritor:
        raise HTTPException(status_code=404, detail="非遗传承人不存在")
    
    return DataResponse(data=inheritor, message="获取成功")


@router.post("/heritage/inheritors", response_model=DataResponse[HeritageInheritorPublic])
async def create_heritage_inheritor(
    inheritor_data: HeritageInheritorCreate,
    db: AsyncSession = Depends(get_async_db),
    inheritor_service: HeritageInheritorService = Depends(get_heritage_inheritor_service)
):
    """
    创建非遗传承人
    """
    inheritor = await inheritor_service.create(db, obj_in=inheritor_data)
    return DataResponse(data=inheritor, message="非遗传承人创建成功")


@router.put("/heritage/inheritors/{inheritor_id}", response_model=DataResponse[HeritageInheritorPublic])
async def update_heritage_inheritor(
    inheritor_id: int,
    inheritor_data: HeritageInheritorUpdate,
    db: AsyncSession = Depends(get_async_db),
    inheritor_service: HeritageInheritorService = Depends(get_heritage_inheritor_service)
):
    """
    更新非遗传承人
    """
    inheritor = await inheritor_service.get(db, inheritor_id)
    if not inheritor:
        raise HTTPException(status_code=404, detail="非遗传承人不存在")
    
    updated_inheritor = await inheritor_service.update(db, db_obj=inheritor, obj_in=inheritor_data)
    return DataResponse(data=updated_inheritor, message="非遗传承人更新成功")


@router.patch("/heritage/inheritors/{inheritor_id}/status", response_model=DataResponse[HeritageInheritorPublic])
async def toggle_heritage_inheritor_status(
    inheritor_id: int,
    inheritor_service: HeritageInheritorService = Depends(get_heritage_inheritor_service)
):
    """
    切换非遗传承人启用状态
    注意：toggle_status方法内部管理数据库会话
    """
    inheritor = await inheritor_service.toggle_status(inheritor_id)
    if not inheritor:
        raise HTTPException(status_code=404, detail="非遗传承人不存在")
    
    return DataResponse(
        data=inheritor,
        message=f"传承人已{'启用' if inheritor.status == 'active' else '停用'}"
    )


@router.delete("/heritage/inheritors/{inheritor_id}", response_model=DataResponse)
async def delete_heritage_inheritor(
    inheritor_id: int,
    db: AsyncSession = Depends(get_async_db),
    inheritor_service: HeritageInheritorService = Depends(get_heritage_inheritor_service)
):
    """
    删除非遗传承人
    """
    success = await inheritor_service.remove(db, id=inheritor_id)
    if not success:
        raise HTTPException(status_code=404, detail="非遗传承人不存在")
    
    return DataResponse(message="非遗传承人删除成功") 


@router.post("/heritage/projects/{project_id}/join", response_model=DataResponse)
async def join_heritage_project(
    project_id: int,
    user_id: int = Query(..., description="用户ID"),  # 临时用query参数
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    加入非遗计划
    """
    # 检查项目是否存在
    project = await project_service.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="非遗项目不存在")
    
    # 自动加入对应群聊
    try:
        from ...services.chat_service import ChatService
        from ...schemas.chat import ChatRoomMemberCreate
        
        chat_service = ChatService()
        
        # 查找项目对应的群聊
        if hasattr(project, 'chat_room_id') and project.chat_room_id:
            # 检查用户是否已经在群聊中
            is_member = await chat_service.is_room_member(db, project.chat_room_id, user_id)
            
            if not is_member:
                # 加入群聊
                member_data = ChatRoomMemberCreate(
                    room_id=project.chat_room_id,
                    user_id=user_id,
                    role="member"
                )
                await chat_service.add_room_member(db, member_data)
                
    except Exception as e:
        # 群聊加入失败不影响计划加入
        print(f"Failed to join chat room for heritage project {project_id}: {e}")
    
    return DataResponse(message=f"成功加入{project.name}非遗传承计划！")


@router.post("/heritage/projects/{project_id}/leave", response_model=DataResponse)
async def leave_heritage_project(
    project_id: int,
    user_id: int = Query(..., description="用户ID"),  # 临时用query参数
    db: AsyncSession = Depends(get_async_db),
    project_service: HeritageProjectService = Depends(get_heritage_project_service)
):
    """
    退出非遗计划
    """
    # 检查项目是否存在
    project = await project_service.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="非遗项目不存在")
    
    # 自动退出对应群聊
    try:
        from ...services.chat_service import ChatService
        
        chat_service = ChatService()
        
        # 查找项目对应的群聊
        if hasattr(project, 'chat_room_id') and project.chat_room_id:
            # 检查用户是否在群聊中
            is_member = await chat_service.is_room_member(db, project.chat_room_id, user_id)
            
            if is_member:
                # 退出群聊
                await chat_service.remove_room_member(db, project.chat_room_id, user_id)
                
    except Exception as e:
        # 群聊退出失败不影响计划退出
        print(f"Failed to leave chat room for heritage project {project_id}: {e}")
    
    return DataResponse(message=f"已退出{project.name}非遗传承计划") 