from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, signup, login_view, logout_user, me, delete_user

# DefaultRouter 설정
router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

# 일반 URL 패턴 + Router URL 패턴 통합
urlpatterns = [
    path('signup/', signup, name='signup'),  # ✅ 회원가입 API (POST)
    path('login/', login_view, name='login'),  # ✅ 로그인 API (POST)
    path('logout/', logout_user, name='logout'),  # ✅ 로그아웃 API (POST)
    path('me/', me, name='me'),  # ✅ 현재 로그인한 사용자 정보 (GET)
    path('delete/', delete_user, name='delete_user'),  # ✅ 회원 탈퇴 (DELETE)
    path('', include(router.urls)),  # ✅ ViewSet 라우팅 추가
]
