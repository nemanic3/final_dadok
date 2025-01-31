from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('login/', views.login_view, name='login'),  # ✅ 함수명 변경
    path('login_success/', views.login_success, name='login_success'),
    path('logout/', views.logout_user, name='logout'),
    path('mypage/', views.my_page, name='mypage'),
    path('me/', views.me, name='me'),
    path('delete/', views.delete_user, name='delete_user'),
]