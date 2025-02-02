from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
import requests
from django.conf import settings
from rest_framework.viewsets import ModelViewSet

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    """
    ✅ 리뷰 저장 API (POST)
    - 네이버 API에서 가져온 책의 정보를 기반으로 리뷰 저장
    - 클라이언트에서 `isbn`, `content`, `rating` 값을 전달해야 함
    """
    isbn = request.data.get('isbn')
    content = request.data.get('content')
    rating = request.data.get('rating')

    if not isbn or not content or not rating:
        return Response({'error': '모든 필드를 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

    # 네이버 API에서 책 정보 가져오기
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
            book_info = data["items"][0]  # 첫 번째 검색 결과 사용

            # 리뷰 저장
            review = Review.objects.create(
                user=request.user,
                book_isbn=isbn,
                book_title=book_info['title'],
                book_author=book_info['author'],
                content=content,
                rating=rating
            )

            return Response({
                "message": "리뷰가 저장되었습니다.",
                "review": {
                    "id": review.id,
                    "book_title": review.book_title,
                    "book_author": review.book_author,
                    "content": review.content,
                    "rating": review.rating
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': '책 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': '네이버 API 호출 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_reviews(request):
    """
    ✅ 전체 리뷰 목록 조회 API (GET)
    """
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_book_info(request, isbn):
    """
    ✅ 특정 책 정보 조회 API (GET)
    - 프론트엔드에서 `isbn`을 전달하면 네이버 API에서 해당 책 정보를 가져옴
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
            return Response(data["items"][0])  # 첫 번째 검색 결과 반환
        else:
            return Response({"error": "책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "네이버 API 호출 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ReviewViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Review instances.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer