from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_books, name='search_books'),  # ✅ /books/search/
    path('get/<str:isbn>/', views.get_book_by_isbn, name='get_book_by_isbn'),  # ✅ /books/get/{isbn}/
]