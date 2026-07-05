import pytest
from unittest.mock import patch

from apps.consultant.services import ConsultantService
from apps.products.models import Product

pytestmark = pytest.mark.django_db


def test_consultant_valid_response():
    """Quando há produtos, a service deve enviar o prompt e retornar a resposta da IA."""
    Product.objects.create(name="P1", description="D1", price=10, quantity=2)

    service = ConsultantService()

    with patch("apps.consultant.clients.GeminiClient.generate", return_value="Resposta IA") as mock_gen:
        result = service.execute("Qual o produto?")

        mock_gen.assert_called_once()
        assert result["answer"] == "Resposta IA"


@pytest.mark.django_db
def test_consultant_no_products_calls_generate_with_empty_context():
    """Quando não há produtos, ainda chamamos a IA com contexto vazio."""
    service = ConsultantService()

    with patch("apps.consultant.clients.GeminiClient.generate", return_value="Sem produtos") as mock_gen:
        result = service.execute("O que tem?")

        mock_gen.assert_called_once()
        assert result["answer"] == "Sem produtos"


def test_consultant_ia_raises_exception():
    """Se o client da IA lançar erro, a exceção deve propagar (cobertura de erro)."""
    service = ConsultantService()

    with patch("apps.consultant.clients.GeminiClient.generate", side_effect=Exception("IA falhou")):
        with pytest.raises(Exception):
            service.execute("Teste")


def test_consultant_ia_timeout():
    """Simula timeout no client da IA e verifica propagação."""
    service = ConsultantService()

    with patch("apps.consultant.clients.GeminiClient.generate", side_effect=TimeoutError("timeout")):
        with pytest.raises(TimeoutError):
            service.execute("Timeout test")
