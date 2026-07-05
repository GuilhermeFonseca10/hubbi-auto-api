import pytest
from typing import Any, Dict, Optional
from unittest.mock import patch, MagicMock

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.products.models import Product
from apps.products.services import ProductImportService

User = get_user_model()


def create_admin() -> User:
    """Cria um usuário admin para autenticação nos testes.

    Returns:
        User: instância do usuário com permissões de staff/superuser.
    """
    return User.objects.create_user(
        username="admin",
        email="admin@test.com",
        password="123456",
        is_staff=True,
        is_superuser=True,
    )


def _extract_list(response: Any) -> Optional[list]:
    """Extrai a lista de resultados da resposta da API tratando paginação.

    Alguns endpoints retornam uma lista direta, outros usam a chave `results`.
    """
    data = getattr(response, "data", None)
    if isinstance(data, dict) and "results" in data:
        return data.get("results")
    if isinstance(data, list):
        return data
    return None


@pytest.mark.django_db
def test_list_products():
    """GET /products/ deve retornar a lista de produtos (ou página com resultados)."""
    client = APIClient()

    Product.objects.create(
        name="Filtro de Óleo",
        description="Teste",
        price=10,
        quantity=5,
    )

    url = reverse("product-list")
    response = client.get(url)

    assert response.status_code == 200

    results = _extract_list(response)
    assert results is not None and len(results) > 0


@pytest.mark.django_db
def test_retrieve_product():
    """GET /products/{id}/ deve retornar os dados do produto solicitado."""
    client = APIClient()

    product = Product.objects.create(
        name="Filtro",
        description="Detalhe",
        price=20,
        quantity=5,
    )

    url = reverse("product-detail", args=[product.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.data.get("id") == product.id
    assert response.data.get("name") == "Filtro"


@pytest.mark.django_db
def test_create_product():
    """POST /products/ deve criar um produto quando autenticado como admin."""
    admin = create_admin()

    client = APIClient()
    client.force_authenticate(user=admin)

    payload: Dict[str, Any] = {
        "name": "Pastilha",
        "description": "Freio",
        "price": 100,
        "quantity": 10,
    }

    url = reverse("product-list")

    response = client.post(url, payload, format="json")

    assert response.status_code == 201
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_update_product():
    """PUT /products/{id}/ atualiza completamente o produto."""
    admin = create_admin()

    client = APIClient()
    client.force_authenticate(user=admin)

    product = Product.objects.create(
        name="Filtro",
        description="Teste",
        price=20,
        quantity=5,
    )

    payload: Dict[str, Any] = {
        "name": "Filtro Atualizado",
        "description": "Nova descrição",
        "price": 35,
        "quantity": 12,
    }

    url = reverse("product-detail", args=[product.id])

    response = client.put(url, payload, format="json")

    assert response.status_code == 200

    product.refresh_from_db()

    assert product.name == "Filtro Atualizado"
    assert product.price == 35
    assert product.quantity == 12


@pytest.mark.django_db
def test_delete_product():
    """DELETE /products/{id}/ remove o produto e retorna 204."""
    admin = create_admin()

    client = APIClient()
    client.force_authenticate(user=admin)

    product = Product.objects.create(
        name="Filtro",
        description="Teste",
        price=20,
        quantity=5,
    )

    url = reverse("product-detail", args=[product.id])

    response = client.delete(url)

    assert response.status_code == 204
    assert Product.objects.count() == 0


@pytest.mark.django_db
def test_csv_import(tmp_path):
    """Valida importação CSV via service (fluxo síncrono para cobertura)."""
    file = tmp_path / "products.csv"

    file.write_text(
        "nome,descricao,preco,quantidade_inicial\n"
        "Filtro,desc,10,5\n"
    )

    service = ProductImportService(str(file))
    result = service.execute()

    assert result == 1
    assert Product.objects.count() == 1

    product = Product.objects.first()

    assert product.name == "Filtro"
    assert product.quantity == 5


@pytest.mark.django_db
def test_csv_invalid_non_numeric_price(tmp_path):
    """CSV com preço não numérico deve levantar ValueError."""
    file = tmp_path / "products_invalid.csv"

    file.write_text(
        "nome,descricao,preco,quantidade_inicial\n"
        "Filtro,desc,abc,5\n"
    )

    service = ProductImportService(str(file))

    with pytest.raises(ValueError):
        service.execute()


@pytest.mark.django_db
def test_csv_without_header_raises(tmp_path):
    """CSV sem cabeçalho deve ser considerado inválido (campos faltando)."""
    file = tmp_path / "products_no_header.csv"

    # Sem cabeçalho: primeira linha será tratada como header e faltará os nomes esperados
    file.write_text(
        "Filtro,desc,10,5\n"
    )

    service = ProductImportService(str(file))

    with pytest.raises(ValueError):
        service.execute()


@pytest.mark.django_db
def test_csv_semicolon_delimiter(tmp_path):
    """CSV usando ponto-e-vírgula como delimitador deve ser detectado e importado."""
    file = tmp_path / "products_semicolon.csv"

    file.write_text(
        "nome;descricao;preco;quantidade_inicial\n"
        "Filtro;desc;10;5\n"
    )

    service = ProductImportService(str(file))
    result = service.execute()

    assert result == 1
    assert Product.objects.count() == 1


@pytest.mark.django_db
def test_csv_empty_file_raises(tmp_path):
    """Arquivo CSV vazio deve levantar uma exceção ao tentar ler/parsear."""
    file = tmp_path / "empty.csv"
    file.write_text("")

    service = ProductImportService(str(file))

    with pytest.raises(Exception):
        service.execute()


def test_import_products_task_calls_service():
    """A task Celery `import_products_task` deve instanciar o service e chamar `execute`.

    Usamos mock para evitar leitura de arquivos e execução real.
    """
    from apps.products import tasks

    fake_file = "/tmp/fake.csv"

    mock_service = MagicMock()
    mock_service.execute.return_value = 3

    with patch("apps.products.tasks.ProductImportService", return_value=mock_service) as p:
        # Chama a task sincronicamente
        result = tasks.import_products_task(fake_file)

        # A task não retorna valor, apenas verifica chamadas
        mock_service.execute.assert_called_once()
        p.assert_called_once_with(fake_file)