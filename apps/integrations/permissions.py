from django.conf import settings
from rest_framework.permissions import BasePermission


class HasApiKey(BasePermission):

    message = "API Key inválida."

    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-Key")

        return api_key == settings.API_KEY