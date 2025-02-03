from django.urls import path
from .views import GoalViewSet

goal_list = GoalViewSet.as_view({
    'get': 'list',  # 목록 조회
    'post': 'create',  # 목표 생성
})

goal_detail = GoalViewSet.as_view({
    'get': 'retrieve',  # 특정 목표 조회
    'put': 'update',  # 목표 수정
    'delete': 'destroy',  # 목표 삭제
})

urlpatterns = [
    path('', goal_list, name='goal-list'),  # /goal/에서 목록 조회 및 목표 생성
    path('<int:pk>/', goal_detail, name='goal-detail'),  # /goal/{id}/에서 조회, 수정, 삭제
]
