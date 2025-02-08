from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, GoalProgressView, MonthlyReadingProgressView

router = DefaultRouter()
router.register('goal', GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),
    path('progress/', GoalProgressView.as_view(), name='goal_progress'),  # ✅ 목표 진행률 조회 (그래프용)
    path('monthly-progress/', MonthlyReadingProgressView.as_view(), name='monthly_goal_progress'),  # ✅ 월별 독서량 조회 (그래프용)
]