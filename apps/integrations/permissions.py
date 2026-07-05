from django.conf import settings
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class HasApiKey(BasePermission):

    message = "API Key inválida."

    def has_permission(self, request, view):
        api_key = request.headers.get("X-API-Key")

        if api_key is None:
            return False

        if api_key != settings.API_KEY:
            raise PermissionDenied(self.message)

        return True