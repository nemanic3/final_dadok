from django.urls import path
from .views import search_books, get_book_by_isbn

urlpatterns = [
    path('search/', search_books, name='search_books'),
    path('get/<str:isbn>/', get_book_by_isbn, name='get_book_by_isbn'),
    path('search/custom/', search_books, name='custom_book_search'),  # ViewSet 메서드 대신 활용
]
