from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # ✅ 회원가입 API (POST)
    path('login/', views.login_view, name='login'),  # ✅ 로그인 API (POST)
    path('logout/', views.logout_user, name='logout'),  # ✅ 로그아웃 API (POST)
    path('me/', views.me, name='me'),  # ✅ 현재 로그인한 사용자 정보 (GET)
    path('delete/', views.delete_user, name='delete_user'),  # ✅ 회원 탈퇴 (DELETE)
]

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = router.urls