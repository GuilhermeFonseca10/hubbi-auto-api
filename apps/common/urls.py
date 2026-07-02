from django.urls import path
from .views import health, celery_test

urlpatterns = [
    path("health/", health),
    path("celery-test/", celery_test),
]