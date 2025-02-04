from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Goal
from .serializers import GoalSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class GoalListView(ListAPIView):
    """
    모든 목표 조회 (GET)
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [AllowAny]

class GoalCreateView(CreateAPIView):
    """
    특정 사용자의 목표 생성 (POST)
    """
    serializer_class = GoalSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user_id = self.kwargs.get('user_id')  # URL에서 user_id 가져오기
        user = get_object_or_404(User, id=user_id)  # 해당 user 존재 확인
        serializer.save(user=user)  # user 필드를 자동으로 채워서 저장

class UserGoalView(RetrieveUpdateDestroyAPIView):
    """
    특정 사용자의 목표 조회, 수정, 삭제 (GET, PUT, PATCH, DELETE)
    """
    serializer_class = GoalSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs.get('user_id')  # URL에서 user_id 가져오기
        return get_object_or_404(Goal, user_id=user_id)  # 특정 사용자의 Goal 반환
