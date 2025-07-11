from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.api.v1 import courses, auth, stats, users, health, prescriptions, challenges, chat, ai_analysis

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置静态文件
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# 注册路由
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["认证"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["用户管理"])
app.include_router(courses.router, prefix=f"{settings.API_V1_STR}/courses", tags=["舞蹈课程"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["健康管理"])
app.include_router(prescriptions.router, prefix=f"{settings.API_V1_STR}/prescriptions", tags=["运动处方"])
app.include_router(challenges.router, prefix=f"{settings.API_V1_STR}/challenges", tags=["打卡挑战"])
app.include_router(chat.router, prefix=f"{settings.API_V1_STR}/chat", tags=["聊天功能"])
app.include_router(ai_analysis.router, prefix=f"{settings.API_V1_STR}/ai", tags=["AI分析"])
app.include_router(stats.router, prefix=f"{settings.API_V1_STR}/stats", tags=["统计数据"])

@app.get("/")
async def root():
    return {"message": "欢迎使用AI舞蹈教练系统API"}