from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet, LikeReviewView, CommentView, CommentListView,
    RecentReviewView, MyLibraryView, BookReviewsView
)

router = DefaultRouter()
router.register('', ReviewViewSet, basename='review')

urlpatterns = [
    path('<int:review_id>/like/', LikeReviewView.as_view(), name='like_review'),
    path('<int:review_id>/comments/', CommentView.as_view(), name='comment_review'),
    path('<int:review_id>/comments/list/', CommentListView.as_view(), name='list_comments'),

    # ✅ 메인 페이지 - 최신 리뷰 도서 목록
    path('recent-reviews/', RecentReviewView.as_view(), name='recent_reviews'),

    # ✅ 내 서재 - 내가 쓴 리뷰 목록
    path('library/', MyLibraryView.as_view(), name='my_library'),

    # ✅ 특정 책의 최신 리뷰 목록
    path('review/<int:book_id>/', BookReviewsView.as_view(), name='book_reviews'),
]

urlpatterns += router.urls