from rest_framework import serializers
from .models import Review, Like, Comment
from book.models import Book  # ✅ 책 모델 가져오기

class ReviewSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)
    isbn = serializers.CharField(write_only=True)  # ✅ ISBN 입력받기

    class Meta:
        model = Review
        fields = ['id', 'user_nickname', 'isbn', 'content', 'rating', 'created_at', 'updated_at', 'likes_count', 'comments_count']

    def create(self, validated_data):
        # `isbn` 처리
        isbn = validated_data.pop("isbn", None)
        if not isbn:
            raise serializers.ValidationError({"isbn": "ISBN이 필요합니다."})

        # `perform_create`에서 처리된 `book` 객체 가져오기
        book = self.context['book']

        # 리뷰 생성
        review = Review.objects.create(book=book, **validated_data)
        return review

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'review']


class CommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'user_nickname', 'review', 'content', 'created_at', 'updated_at']