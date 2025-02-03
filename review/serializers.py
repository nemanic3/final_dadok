from rest_framework import serializers
from .models import Review
from .models import Comment

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book_title', 'book_author', 'book_isbn', 'content', 'rating', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'review', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']