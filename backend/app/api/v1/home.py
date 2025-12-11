from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional
from datetime import datetime

from ...core.database import get_async_db
from ...core.security import get_current_active_user
from ...schemas.base import DataResponse
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=DataResponse[Dict[str, Any]])
async def get_home_data(
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取首页数据（无需认证，所有用户可访问）
    """
    home_data = {
        "hero": {
            "title": "AI舞蹈教练系统",
            "subtitle": "让AI成为您的私人舞蹈教练",
            "background_image": "/images/home-hero-bg.jpg",
            "featured_courses_count": 8,
            "active_users_count": 1500
        },
        "featured_courses": [
            {
                "id": 1,
                "title": "广场舞入门",
                "category": "square",
                "difficulty": "beginner",
                "duration": 25,
                "cover_url": "/images/course-square-dance.jpg",
                "instructor": "李老师",
                "enrolled_count": 450
            },
            {
                "id": 2,
                "title": "民族舞基础",
                "category": "folk",
                "difficulty": "beginner",
                "duration": 30,
                "cover_url": "/images/course-folk-dance.jpg",
                "instructor": "王老师",
                "enrolled_count": 320
            },
            {
                "id": 3,
                "title": "太极拳进阶",
                "category": "taichi",
                "difficulty": "intermediate",
                "duration": 40,
                "cover_url": "/images/course-taichi.jpg",
                "instructor": "张老师",
                "enrolled_count": 280
            }
        ],
        "stats": {
            "total_courses": 25,
            "total_users": 1500,
            "total_challenges": 12,
            "active_this_week": 450
        },
        "news": [
            {
                "id": 1,
                "title": "系统更新公告",
                "summary": "新增AI动作分析功能，更精准的动作识别",
                "date": "2024-01-15",
                "image": "/images/news-update.jpg"
            },
            {
                "id": 2,
                "title": "新年课程上线",
                "summary": "推出春节特别课程，包括传统舞蹈和现代舞",
                "date": "2024-01-10",
                "image": "/images/news-newyear.jpg"
            }
        ],
        "testimonials": [
            {
                "id": 1,
                "name": "刘女士",
                "age": 55,
                "avatar": "/images/users/default-avatar.png",
                "content": "AI教练帮我纠正了很多动作细节，进步很明显！",
                "rating": 5
            },
            {
                "id": 2,
                "name": "陈先生",
                "age": 42,
                "avatar": "/images/users/default-avatar.png",
                "content": "课程设计很专业，健康管理功能很实用",
                "rating": 5
            }
        ]
    }
    
    return DataResponse(data=home_data, message="获取首页数据成功")

@router.get("/banners", response_model=DataResponse[List[Dict[str, Any]]])
async def get_home_banners():
    """
    获取首页轮播图（无需认证，所有用户可访问）
    """
    banners = [
        {
            "id": 1,
            "title": "新年新课程",
            "subtitle": "春节特别课程火热报名中",
            "image": "/images/banners/newyear.jpg",
            "link": "/courses",
            "order": 1
        },
        {
            "id": 2,
            "title": "AI舞蹈分析",
            "subtitle": "让AI成为您的私人教练",
            "image": "/images/banners/ai-analysis.jpg",
            "link": "/ai-coach",
            "order": 2
        },
        {
            "id": 3,
            "title": "健康管理",
            "subtitle": "科学健身，健康生活",
            "image": "/images/banners/health.jpg",
            "link": "/health",
            "order": 3
        }
    ]
    
    return DataResponse(data=banners, message="获取轮播图成功")

@router.get("/stats", response_model=DataResponse[Dict[str, Any]])
async def get_home_stats(
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取首页统计数据（无需认证，所有用户可访问）
    """
    # 这里可以从数据库获取实时统计数据
    stats = {
        "dailyActiveUsers": 450,
        "weeklyActiveUsers": 1200,
        "monthlyActiveUsers": 4500,
        "totalCourses": 25,
        "totalEnrollments": 8500,
        "totalChallenges": 12,
        "completedChallenges": 340,
        "averageRating": 4.8,
        "growthRate": 15.2,
        "statsToday": {
            "newUsers": 25,
            "newCourses": 1,
            "newChallenges": 2,
            "completedTrainings": 68
        }
    }
    
    return DataResponse(data=stats, message="获取统计数据成功")

@router.get("/news/latest", response_model=DataResponse[List[Dict[str, Any]]])
async def get_latest_news(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取最新新闻列表（无需认证，所有用户可访问）
    """
    # 这里可以从数据库获取新闻数据
    news = [
        {
            "id": 1,
            "title": "系统更新公告",
            "summary": "新增AI动作分析功能，更精准的动作识别和实时反馈",
            "content": "系统已更新到最新版本，新增了多项AI分析功能...",
            "author": "系统管理员",
            "publish_date": "2024-01-15",
            "image": "/images/news/update.jpg",
            "category": "系统更新",
            "views": 1200,
            "is_featured": True
        },
        {
            "id": 2,
            "title": "新年课程上线",
            "summary": "推出春节特别课程，包括传统舞蹈和现代舞",
            "content": "为了庆祝春节，我们推出了多门特色课程...",
            "author": "课程组",
            "publish_date": "2024-01-10",
            "image": "/images/news/newyear.jpg",
            "category": "课程资讯",
            "views": 890,
            "is_featured": False
        },
        {
            "id": 3,
            "title": "用户活动反馈",
            "summary": "2023年度用户活动圆满完成，感谢大家的参与",
            "content": "2023年度用户活动已圆满结束，感谢各位用户的支持...",
            "author": "运营团队",
            "publish_date": "2024-01-05",
            "image": "/images/news/feedback.jpg",
            "category": "用户活动",
            "views": 650,
            "is_featured": False
        }
    ]
    
    # 限制返回数量
    news = news[:limit]
    
    return DataResponse(data=news, message="获取最新新闻成功")