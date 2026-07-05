import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient

from apps.products.models import Product


@pytest.mark.django_db
def test_integration_with_valid_api_key_updates_stock(monkeypatch):
    """POST /integrations/ com API Key válida atualiza estoque em lote."""
    monkeypatch.setattr(settings, "API_KEY", "valid-api-key")

    product1 = Product.objects.create(name="P1", description="D1", price=10, quantity=5)
    product2 = Product.objects.create(name="P2", description="D2", price=20, quantity=3)

    client = APIClient()
    client.credentials(HTTP_X_API_KEY="valid-api-key")

    payload = {
        "products": [
            {"id": product1.id, "quantity": 10},
            {"id": product2.id, "quantity": 1},
        ]
    }

    url = reverse("integrations-list")
    response = client.post(url, payload, format="json")

    assert response.status_code == 200
    assert response.data["message"] == "Estoque atualizado com sucesso."

    product1.refresh_from_db()
    product2.refresh_from_db()

    assert product1.quantity == 10
    assert product2.quantity == 1


@pytest.mark.django_db
def test_integration_with_invalid_api_key_returns_403(monkeypatch):
    """POST /integrations/ com API Key inválida retorna 403."""
    monkeypatch.setattr(settings, "API_KEY", "valid-api-key")

    Product.objects.create(name="P1", description="D1", price=10, quantity=5)

    client = APIClient()
    client.credentials(HTTP_X_API_KEY="invalid")

    payload = {"products": [{"id": 1, "quantity": 10}]}

    url = reverse("integrations-list")
    response = client.post(url, payload, format="json")

    assert response.status_code == 403
    assert response.data["detail"] == "API Key inválida."


@pytest.mark.django_db
def test_integration_with_nonexistent_product_returns_404(monkeypatch):
    """POST /integrations/ com produto inexistente retorna 404."""
    monkeypatch.setattr(settings, "API_KEY", "valid-api-key")

    client = APIClient()
    client.credentials(HTTP_X_API_KEY="valid-api-key")

    payload = {"products": [{"id": 9999, "quantity": 10}]}

    url = reverse("integrations-list")
    response = client.post(url, payload, format="json")

    assert response.status_code == 404
    assert "Produto 9999 não encontrado" in response.data["detail"]


@pytest.mark.django_db
def test_integration_partial_update_quantity(monkeypatch):
    """Atualização parcial de estoque deve alterar apenas a quantidade enviada."""
    monkeypatch.setattr(settings, "API_KEY", "valid-api-key")

    product = Product.objects.create(name="P1", description="D1", price=10, quantity=5)

    client = APIClient()
    client.credentials(HTTP_X_API_KEY="valid-api-key")

    payload = {"products": [{"id": product.id, "quantity": 8}]}

    url = reverse("integrations-list")
    response = client.post(url, payload, format="json")

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.quantity == 8
