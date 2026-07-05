from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from apps.products.models import Product


class ProductResource(resources.ModelResource):
    """Resource para importação e exportação de produtos."""

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "quantity",
            "created_at",
            "updated_at",
        )
        export_order = fields


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    """Admin personalizado para o modelo de produto."""

    resource_class = ProductResource
    list_display = (
        "id",
        "name",
        "price",
        "quantity",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description")
    ordering = ("name",)
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Dados do produto",
            {
                "fields": (
                    "name",
                    "description",
                    "price",
                    "quantity",
                )
            },
        ),
        (
            "Metadados",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

