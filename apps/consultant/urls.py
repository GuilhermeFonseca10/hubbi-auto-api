from rest_framework.routers import DefaultRouter

from apps.consultant.viewset import ConsultantViewSet

router = DefaultRouter()
router.register(
    "",
    ConsultantViewSet,
    basename="consultant",
)

urlpatterns = router.urls