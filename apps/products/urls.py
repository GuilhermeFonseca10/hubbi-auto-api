from rest_framework.routers import DefaultRouter
from .viewset import ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = router.urls