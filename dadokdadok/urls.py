from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from review.views import LikeReviewView
from user.views import home

urlpatterns = [
    # 각 앱의 URL을 명시적으로 포함
    path('api/admin/', admin.site.urls),
    path('api/user/', include('user.urls')),  # User 관련 엔드포인트
    path('api/book/', include('book.urls')),  # Book 관련 엔드포인트
    path('api/review/', include('review.urls')),  # Review 관련 엔드포인트
    path('api/goal/', include('goal.urls')),  # Goal 관련 엔드포인트
    path('api/recommendation/', include('recommendation.urls')),  # recommendation 앱 등록

    # ✅ JWT 로그인 (토큰 발급 및 갱신)
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ 리뷰 좋아요 기능 추가
    path('api/review/<int:review_id>/like/', LikeReviewView.as_view(), name='like_review'),

    # ✅ API 상태 확인 엔드포인트
    path('', home, name='home'),
]
