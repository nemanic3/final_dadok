from django.db import models
from user.models import CustomUser
from django.conf import settings

class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # 작성자
    book_isbn = models.CharField(max_length=20, default="")  # ISBN
    book_title = models.CharField(max_length=200, default="")  # 도서 제목
    book_author = models.CharField(max_length=100, default="")  # 도서 저자
    content = models.TextField(null=True, blank=True)  # 감상문 내용
    rating = models.FloatField(null=True, blank=True)  # 평점
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

    class Meta:
        db_table = 'review'

    def __str__(self):
        return f"{self.user.username}'s review of {self.book_title}"


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE, related_name='comments')  # 어떤 리뷰에 달린 댓글인지
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 댓글 작성자
    content = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간

    class Meta:
        db_table = 'comment'

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review.id}"