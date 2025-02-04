from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # 각 앱의 URL을 명시적으로 포함
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),  # User 관련 엔드포인트
    path('book/', include('book.urls')),  # Book 관련 엔드포인트
    path('review/', include('review.urls')),  # Review 관련 엔드포인트
    path('goal/', include('goal.urls')),  # Goal 관련 엔드포인트
]
