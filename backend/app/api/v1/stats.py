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