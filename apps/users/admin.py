from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.users.models import User


class UserResource(resources.ModelResource):
    """Resource para importação e exportação de usuários."""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_admin",
            "is_staff",
            "is_superuser",
            "date_joined",
            "last_login",
        )
        export_order = fields


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    """Admin personalizado para o modelo de usuário."""

    resource_class = UserResource
    list_display = (
        "id",
        "username",
        "email",
        "is_admin",
        "is_staff",
        "is_superuser",
        "date_joined",
    )
    search_fields = ("username", "email")
    ordering = ("username",)
    list_filter = (
        "is_admin",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = ("date_joined", "last_login")
    fieldsets = (
        (
            "Informações pessoais",
            {
                "fields": (
                    "username",
                    "email",
                    "is_admin",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "date_joined",
                    "last_login",
                )
            },
        ),
    )
