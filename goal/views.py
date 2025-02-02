from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Goal
from .serializers import GoalSerializer

class GoalViewSet(ModelViewSet):
    """
    ✅ 목표 관리 API (JSON 응답)
    - 목록 조회 (GET /goal/)
    - 목표 생성 (POST /goal/)
    - 특정 목표 조회 (GET /goal/{id}/)
    - 목표 수정 (PUT /goal/{id}/)
    - 목표 삭제 (DELETE /goal/{id}/)
    """
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]  # ✅ 로그인한 사용자만 접근 가능

    def perform_create(self, serializer):
        """
        ✅ 목표를 생성할 때 현재 로그인한 사용자를 자동으로 저장
        """
        serializer.save(user=self.request.user)
