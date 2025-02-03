from django.urls import path
from .views import create_review, get_my_reviews, get_book_reviews, update_review, delete_review, create_comment, get_comments, delete_comment, get_book_info


urlpatterns = [
    path("mine/", get_my_reviews, name="get_my_reviews"),  # http://127.0.0.1:8000/review/mine/ (모든 리뷰 조회 API)
    path("create/", create_review, name="create_review"),  # http://127.0.0.1:8000/review/create/ (리뷰 저장 API)
    path("book/<str:isbn>/reviews/", get_book_reviews, name="get_book_reviews"),  # http://127.0.0.1:8000/review/book/<isbn>/reviews/ (특정 책 정보 조회 API)
    path("<int:review_id>/update/", update_review, name="update_review"),  # 리뷰 수정
    path("<int:review_id>/delete/", delete_review, name="delete_review"),  # 리뷰 삭제
    path("<int:review_id>/comments/", get_comments, name="get_comments"),  # 특정 리뷰의 댓글 조회
    path("<int:review_id>/comments/create/", create_comment, name="create_comment"),  # 댓글 작성
    path("comments/<int:comment_id>/delete/", delete_comment, name="delete_comment"),  # 댓글 삭제
]
