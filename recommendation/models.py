from django.db import models
from django.conf import settings

class Recommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book_title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default="Unknown Author")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommendation'
        constraints = [
            models.UniqueConstraint(fields=['user', 'book_title'], name="unique_recommendation")
        ]

    def __str__(self):
        return f"{self.user.nickname} 추천 - {self.book_title}"