from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Review
from .serializers import ReviewSerializer
import requests
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from .models import Comment
from .serializers import CommentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    """
    ✅ 리뷰 저장 API (POST)
    - 네이버 API에서 가져온 책의 정보를 기반으로 리뷰 저장
    - 클라이언트에서 `isbn`, `content`, `rating` 값을 전달해야 함
    """
    print("create_review 함수 호출됨")  # 디버깅 로그

    isbn = request.data.get('isbn')
    print(f"요청됨 ISBN: {isbn}")
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
@permission_classes([IsAuthenticated])
def get_my_reviews(request):
    """
    ✅ 사용자 본인의 리뷰 목록 조회 API (GET)
    - 책 제목, 지은이, 리뷰 내용, 평점 포함
    """
    reviews = Review.objects.filter(user=request.user)  # 현재 로그인한 사용자의 리뷰만 필터링
    serializer = ReviewSerializer(reviews, many=True)

    # 출력 데이터 수정 (책 제목과 지은이 추가)
    data = [
        {
            "id": review.id,
            "book_title": review.book_title,
            "book_author": review.book_author,
            "content": review.content,
            "rating": review.rating,
        }
        for review in reviews
    ]

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_book_reviews(request, isbn):
    """
    ✅ 특정 책의 리뷰 조회 API (GET)
    - ISBN을 기반으로 해당 책에 대한 최근 5개의 리뷰를 반환
    """
    # 해당 ISBN에 대한 리뷰를 최신 순으로 가져오기
    reviews = Review.objects.filter(book_isbn=isbn).order_by('-created_at')[:5]
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_id):
    """
    ✅ 리뷰 수정 API (PUT)
    - 특정 리뷰를 수정
    """
    try:
        # 리뷰 조회 (현재 사용자 소유인지 확인)
        review = Review.objects.get(id=review_id, user=request.user)
    except Review.DoesNotExist:
        return Response({'error': '리뷰를 찾을 수 없거나 권한이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 데이터 업데이트
    content = request.data.get('content')
    rating = request.data.get('rating')

    if content:
        review.content = content
    if rating:
        review.rating = rating

    review.save()

    return Response({
        "message": "리뷰가 수정되었습니다.",
        "review": {
            "id": review.id,
            "book_title": review.book_title,
            "book_author": review.book_author,
            "content": review.content,
            "rating": review.rating,
        }
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request, review_id):
    """
    ✅ 리뷰 삭제 API (DELETE)
    - 특정 리뷰를 삭제
    """
    try:
        # 리뷰 조회 (현재 사용자 소유인지 확인)
        review = Review.objects.get(id=review_id, user=request.user)
    except Review.DoesNotExist:
        return Response({'error': '리뷰를 찾을 수 없거나 권한이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    review.delete()
    return Response({"message": "리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, review_id):
    """
    ✅ 댓글 작성 API (POST)
    - 특정 리뷰에 댓글 작성
    """
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'error': '리뷰를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    content = request.data.get('content')
    if not content:
        return Response({'error': '댓글 내용을 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)

    comment = Comment.objects.create(
        review=review,
        user=request.user,
        content=content
    )

    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_comments(request, review_id):
    """
    ✅ 특정 리뷰의 댓글 조회 API (GET)
    """
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({'error': '리뷰를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    comments = Comment.objects.filter(review=review).order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    """
    ✅ 댓글 삭제 API (DELETE)
    """
    try:
        comment = Comment.objects.get(id=comment_id, user=request.user)
    except Comment.DoesNotExist:
        return Response({'error': '댓글을 찾을 수 없거나 권한이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response({"message": "댓글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
