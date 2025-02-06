from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, AnnualGoalView, MonthlyGoalView, GoalProgressView

router = DefaultRouter()
router.register('', GoalViewSet, basename='goal')

urlpatterns = [
    path('', include(router.urls)),  # ✅ 기본 CRUD API
    path('annual/', AnnualGoalView.as_view(), name='annual_goal'),  # ✅ 연간 목표 API
    path('monthly/', MonthlyGoalView.as_view(), name='monthly_goal'),  # ✅ 월간 목표 API
    path('progress/', GoalProgressView.as_view(), name='goal_progress'),  # ✅ 목표 진행률 조회 API
]