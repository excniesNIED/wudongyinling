# 导入所有服务
from .user_service import UserService
from .auth_service import AuthService
from .course_service import CourseService
from .health_service import HealthService
from .prescription_service import PrescriptionService
from .challenge_service import ChallengeService
from .chat_service import ChatService
from .ai_service import AIService
from .social_service import (
    PostService,
    PostCommentService,
    PostLikeService,
    HeritageProjectService,
    HeritageInheritorService,
    SocialService
)

# 实例化服务
user_service = UserService()
auth_service = AuthService()
course_service = CourseService()
health_service = HealthService()
prescription_service = PrescriptionService()
challenge_service = ChallengeService()
chat_service = ChatService()
ai_service = AIService()
social_service = SocialService() 