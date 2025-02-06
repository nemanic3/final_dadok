from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Review, Like, Comment
from .serializers import ReviewSerializer, LikeSerializer, CommentSerializer
from book.models import Book  # Book 모델 임포트
from book.services import get_book_by_isbn_from_naver  # 네이버 API 호출 함수 임포트
from rest_framework.serializers import ValidationError

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        isbn = self.request.data.get("isbn")  # 요청 데이터에서 ISBN 가져오기
        if not isbn:
            raise ValidationError({"isbn": "ISBN이 필요합니다."})

        # ISBN으로 책 조회 (DB에서 먼저 확인)
        book = Book.objects.filter(isbn=isbn).first()

        # DB에 없으면 외부 API 호출
        if not book:
            book_data = get_book_by_isbn_from_naver(isbn)
            if not book_data:
                raise ValidationError({"isbn": "해당 ISBN으로 책 정보를 찾을 수 없습니다."})

            # 외부 API 결과를 기반으로 Book 생성
            book = Book.objects.create(
                isbn=isbn,
                title=book_data.get("title", "Unknown Title"),
                author=book_data.get("author", "Unknown Author"),
                publisher=book_data.get("publisher", "Unknown Publisher"),
                published_date=book_data.get("pubdate", ""),
                image_url=book_data.get("image", ""),
            )

        # 리뷰 저장
        serializer.context['book'] = book
        serializer.save(user=self.request.user)


class LikeReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, review=review)

        if not created:
            like.delete()
            return Response({"message": "Like removed", "likes_count": review.likes.count()}, status=status.HTTP_200_OK)

        return Response({"message": "Like added", "likes_count": review.likes.count()}, status=status.HTTP_201_CREATED)

class CommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "user": request.user.id,
            "review": review.id,
            "content": request.data.get("content")
        }
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, review_id):
        comments = Comment.objects.filter(review_id=review_id).order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)