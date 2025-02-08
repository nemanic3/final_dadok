from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .services import get_book_recommendations

class NaverRecommendationView(APIView):
    """
    네이버 API를 활용한 추천 도서 리스트 반환 (책 상세 페이지에서 사용)
    """
    permission_classes = [AllowAny]  # ✅ 인증 없이 접근 가능

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