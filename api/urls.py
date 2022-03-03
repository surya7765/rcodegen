from api.views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api-auth', PostViewSet, basename='api-auth')
urlpatterns = router.urls
