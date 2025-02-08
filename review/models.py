from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book  # ✅ 책 모델 임포트

User = get_user_model()

class Review(models.Model):
    """ 사용자가 특정 책에 대해 작성한 리뷰 """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "review"
        unique_together = ('user', 'book')  # ✅ 같은 책에 대한 중복 리뷰 방지

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"


class Like(models.Model):
    """ 특정 리뷰에 대한 좋아요 """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        db_table = "like"
        constraints = [
            models.UniqueConstraint(fields=["user", "review"], name="unique_like")
        ]

    def __str__(self):
        return f"{self.user.username} liked {self.review}"


class Comment(models.Model):
    """ 특정 리뷰에 대한 댓글 """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ 수정 시간 추가

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f"{self.user.username} commented on {self.review}"