from rest_framework import serializers
from .models import Recommendation

class RecommendationSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'user_nickname', 'book_title', 'author', 'description', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        """ 동일 사용자의 중복 추천 방지 """
        user = self.context['request'].user
        if Recommendation.objects.filter(user=user, book_title=data['book_title']).exists():
            raise serializers.ValidationError({"error": "이미 추천한 도서입니다."})
        return data