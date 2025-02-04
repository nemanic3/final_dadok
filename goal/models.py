from django.core.validators import MinValueValidator
import datetime
from django.db import models
from django.conf import settings

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    year = models.PositiveIntegerField(default=datetime.date.today().year)  # 목표 연도
    target_books = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]  # 1 이상 입력 필수
    )
    is_completed = models.BooleanField(default=False)  # 목표 달성 여부

    class Meta:
        db_table = 'goal'
        constraints = [
            models.UniqueConstraint(fields=['user', 'year'], name='unique_user_goal_year')
        ]  # 한 사용자당 1년에 하나의 목표만 가능

    def __str__(self):
        return f"{self.year}년 목표: {self.target_books}권 읽기"
