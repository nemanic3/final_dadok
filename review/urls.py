from django.urls import path
from .views import create_review, get_reviews, get_book_info
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

urlpatterns = [
    path("reviews/", get_reviews, name="get_reviews"),  # ✅ 모든 리뷰 조회 API (GET)
    path("reviews/create/", create_review, name="create_review"),  # ✅ 리뷰 저장 API (POST)
    path("reviews/book/<str:isbn>/", get_book_info, name="get_book_info"),  # ✅ 특정 책 정보 조회 API (GET)
]

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = router.urls