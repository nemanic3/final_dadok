from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Recommendation
from .serializers import RecommendationSerializer
from .services import get_book_recommendations

class RecommendationViewSet(ModelViewSet):
    """
    사용자가 직접 추가하는 추천 API (CRUD)
    """
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recommendation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NaverRecommendationView(APIView):
    """
    네이버 API를 활용한 추천 도서 리스트 반환
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get("query", "")
        display = request.GET.get("display", 5)  # 기본 5개 반환

        if not query:
            return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recommended_books = get_book_recommendations(query, display=int(display))
            return Response(recommended_books, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)