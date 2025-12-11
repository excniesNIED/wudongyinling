# API v1 路由模块导出
# 该模块用于导出所有 API 路由，供 main.py 统一注册

from . import (
    auth,
    users,
    courses,
    health,
    prescriptions,
    challenges,
    stats,
    ai_analysis,
    chat,
    social,
    about,
    home,
    admin,
    websocket
)

__all__ = [
    'auth',
    'users',
    'courses',
    'health',
    'prescriptions',
    'challenges',
    'stats',
    'ai_analysis',
    'chat',
    'social',
    'about',
    'home',
    'admin',
    'websocket'
]

