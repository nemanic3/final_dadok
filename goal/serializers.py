from rest_framework import serializers
from .models import Goal
import datetime

class GoalSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = '__all__'

    def validate(self, data):
        """ 시작 날짜가 종료 날짜보다 늦으면 안됨 """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({"error": "시작 날짜는 종료 날짜보다 이전이어야 합니다."})
        return data

    def get_progress(self, obj):
        """ 목표 진행률 계산 """
        today = datetime.date.today()
        total_days = (obj.end_date - obj.start_date).days
        elapsed_days = (today - obj.start_date).days
        if elapsed_days <= 0:
            return 0
        if elapsed_days >= total_days:
            return 100
        return round((elapsed_days / total_days) * 100, 2)
