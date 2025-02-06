from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Goal
from .serializers import GoalSerializer

class GoalViewSet(ModelViewSet):
    """
    사용자별 목표 관리 (연간 & 월간)
    """
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AnnualGoalView(APIView):
    """
    연간 목표 조회 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        annual_goals = Goal.objects.filter(user=request.user, goal_type='annual')
        serializer = GoalSerializer(annual_goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MonthlyGoalView(APIView):
    """
    월간 목표 조회 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        monthly_goals = Goal.objects.filter(user=request.user, goal_type='monthly')
        serializer = GoalSerializer(monthly_goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GoalProgressView(APIView):
    """
    목표 진행률 조회 API
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        goals = Goal.objects.filter(user=request.user)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)