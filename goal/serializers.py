from rest_framework import serializers
from .models import Goal

class GoalSerializer(serializers.ModelSerializer):
    target_books = serializers.IntegerField(
        required=True,  # 필수 입력
        error_messages={"required": "목표 권수를 입력해주세요."}  # 오류 메시지 설정
    )

    user = serializers.PrimaryKeyRelatedField(read_only=True)  # 입력받지 않고 자동 처리

    class Meta:
        model = Goal
        fields = ['id', 'user', 'year', 'target_books', 'is_completed']

    def validate_target_books(self, value):
        """ 목표 권수 유효성 검사 """
        if value <= 0:
            raise serializers.ValidationError("목표 권수는 1권 이상이어야 합니다.")
        return value
