from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    book = models.ForeignKey("book.Book", on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "review"

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title}"

class Like(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ 수정 시간 추가

    class Meta:
        db_table = "comment"

    def __str__(self):
        return f"{self.user.username} commented on {self.review}"