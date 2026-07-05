from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.products.models import Product


class StockIntegrationService:

    @staticmethod
    @transaction.atomic
    def execute(products_data):

        updated = []

        for item in products_data:

            product = Product.objects.filter(
                id=item["id"]
            ).first()

            if not product:
                raise NotFound(
                    f"Produto {item['id']} não encontrado."
                )

            product.quantity = item["quantity"]
            product.save(update_fields=["quantity"])

            updated.append(product)

        return updated