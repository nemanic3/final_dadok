from django.urls import path
from .views import (
    create_review,
    get_my_reviews,
    get_book_reviews,
    update_review,
    delete_review,
    create_comment,
    get_comments,
    delete_comment,
    like_review,
    get_likes_count,
    get_book_info
)

urlpatterns = [
    path("mine/", get_my_reviews, name="get_my_reviews"),  # 사용자 본인의 리뷰 조회
    path("create/", create_review, name="create_review"),  # 리뷰 생성
    path("book/<str:isbn>/reviews/", get_book_reviews, name="get_book_reviews"),  # 특정 책 리뷰 조회
    path("<int:review_id>/update/", update_review, name="update_review"),  # 리뷰 수정
    path("<int:review_id>/delete/", delete_review, name="delete_review"),  # 리뷰 삭제
    path("<int:review_id>/comments/", get_comments, name="get_comments"),  # 특정 리뷰의 댓글 조회
    path("<int:review_id>/comments/create/", create_comment, name="create_comment"),  # 댓글 생성
    path("comments/<int:comment_id>/delete/", delete_comment, name="delete_comment"),  # 댓글 삭제
    path("<int:review_id>/like/", like_review, name="like_review"),  # 좋아요/취소
    path("<int:review_id>/likes/count/", get_likes_count, name="get_likes_count"),  # 좋아요 개수 조회
]
