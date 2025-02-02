from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import UserViewSet
from book.views import BookViewSet
from review.views import ReviewViewSet
from goal.views import GoalViewSet
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('books', BookViewSet, basename='book')
router.register('reviews', ReviewViewSet, basename='review')
router.register('goals', GoalViewSet, basename='goal')

urlpatterns = [
    path('api/', include(router.urls)),  # API 엔드포인트 추가
    path('api/docs/', include_docs_urls(title="DadokDadok API")),
]
