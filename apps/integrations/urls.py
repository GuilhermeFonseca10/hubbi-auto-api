from rest_framework.routers import DefaultRouter

from apps.integrations.viewset import IntegrationViewSet

router = DefaultRouter()

router.register(
    "",
    IntegrationViewSet,
    basename="integrations",
)

urlpatterns = router.urls