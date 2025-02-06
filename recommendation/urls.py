from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendationViewSet, NaverRecommendationView

router = DefaultRouter()
router.register('', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path('', include(router.urls)),  # ✅ 사용자가 직접 추가하는 추천 API (CRUD)
    path('naver/', NaverRecommendationView.as_view(), name='naver_recommendation'),  # ✅ 네이버 API 기반 추천 기능
]