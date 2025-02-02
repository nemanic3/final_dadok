import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Book  # Book 모델 import
from .serializers import BookSerializer  # BookSerializer import
from rest_framework.decorators import action

@api_view(['GET'])
def search_books(request):
    """
    네이버 API를 이용한 도서 검색
    """
    query = request.GET.get("query", "")
    if not query:
        return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": query, "display": 10}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return Response(data["items"], status=status.HTTP_200_OK)
    else:
        return Response({"error": "네이버 API 호출 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_book_by_isbn(request, isbn):
    """
    리뷰 작성 시 특정 책의 정보를 네이버 API에서 가져옴
    """
    url = settings.NAVER_BOOKS_API_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {"query": isbn, "display": 1}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["items"]:
            return Response(data["items"][0], status=status.HTTP_200_OK)
        else:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "네이버 API 호출 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BookViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Book instances.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.GET.get('query', '')
        if query:
            books = Book.objects.filter(title__icontains=query)  # 제목에 검색어 포함된 책 필터링
            serializer = self.get_serializer(books, many=True)
            return Response(serializer.data)
        return Response({"error": "검색어를 입력하세요."}, status=400)