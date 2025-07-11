from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...models.user import User
from ...models.course import Course
from ...models.challenge import Challenge
from ...models.health import HealthRecord

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """获取仪表盘统计数据"""
    total_users = db.query(User).count()
    total_courses = db.query(Course).count()
    total_challenges = db.query(Challenge).count()
    total_health_records = db.query(HealthRecord).count()

    return {
        "totalUsers": total_users,
        "totalCourses": total_courses,
        "totalChallenges": total_challenges,
        "totalHealthRecords": total_health_records
    }

@router.get("/users")
async def get_user_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    return {"totalUsers": total_users}

@router.get("/courses")
async def get_course_stats(db: Session = Depends(get_db)):
    total_courses = db.query(Course).count()
    return {"totalCourses": total_courses}

@router.get("/challenges")
async def get_challenge_stats(db: Session = Depends(get_db)):
    total_challenges = db.query(Challenge).count()
    return {"totalChallenges": total_challenges} 