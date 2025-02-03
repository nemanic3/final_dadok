from django.urls import path
from .views import UserViewSet, signup, login_view, logout_user, me, delete_user

urlpatterns = [
    path('signup/', signup, name='signup'),  # user/signup/
    path('login/', login_view, name='login'),  # user/login/
    path('logout/', logout_user, name='logout'),  # user/logout/
    path('me/', me, name='me'),  # user/me/
    path('delete/', delete_user, name='delete_user'),  # user/delete/
    path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),  # user/
    path('<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),  # user/<id>/
    path('<int:pk>/update/', UserViewSet.as_view({'put': 'update'}), name='user-update'),  # user/<id>/update/
    path('<int:pk>/delete/', UserViewSet.as_view({'delete': 'destroy'}), name='user-delete'),  # user/<id>/delete/
]
