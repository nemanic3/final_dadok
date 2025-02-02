from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r'', BookViewSet, basename='book')  # /book/ API 엔드포인트

urlpatterns = router.urls
