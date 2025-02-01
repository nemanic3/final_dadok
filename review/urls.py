from django.urls import path
from . import views
from .views import create_review

urlpatterns = [
    path('reviews/form/', views.review_form, name='review_form'),
    path("create/", create_review, name="create_review"),  # 리뷰 저장 API
]
