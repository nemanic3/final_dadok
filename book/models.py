from django.db import models
from user.models import CustomUser

class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, null=True, blank=True)
    published_date = models.CharField(max_length=20, null=True, blank=True)  # 출판 날짜
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)  # ISBN 추가
    publisher = models.CharField(max_length=255, null=True, blank=True)  # 출판사 추가
    image_url = models.URLField(null=True, blank=True)  # 책 표지 이미지
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return f"{self.title} ({self.author})"