from django.urls import path
from .views import GoalListView, GoalCreateView, UserGoalView

urlpatterns = [
    path('', GoalListView.as_view(), name='goal-list'),  # 모든 목표 조회 (GET)
    path('<int:user_id>/create/', GoalCreateView.as_view(), name='goal-create'),  # 특정 사용자의 목표 생성 (POST)
    path('<int:user_id>/detail/', UserGoalView.as_view(), name='user-goal-detail'),  # 특정 사용자의 목표 조회, 수정, 삭제
]
