from pathlib import Path
import csv
import logging
from apps.products.models import Product
from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class ProductImportService:
    """Serviço responsável por persistir produtos enviados via CSV."""

    @staticmethod
    def save_uploaded_file(file) -> str:
        """Salva o arquivo CSV enviado para o storage e retorna o caminho físico."""
        upload_path = Path("imports") / file.name
        saved_path = default_storage.save(str(upload_path), file)

        return str(settings.MEDIA_ROOT / saved_path)

    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self):
        products = self._read_csv()

        self._save_products(products)

        return len(products)

    def _read_csv(self):
        import csv

        products = []

        with open(self.file_path, newline="", encoding="utf-8-sig") as csvfile:
            sample = csvfile.read(8192)
            csvfile.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
            except csv.Error:
                dialect = csv.excel_tab

            reader = csv.DictReader(csvfile, dialect=dialect, skipinitialspace=True)

            reader.fieldnames = [
                (f.strip().lower().replace("\ufeff", "") if f else f)
                for f in reader.fieldnames
            ]

            required_fields = ["nome", "descricao", "preco", "quantidade_inicial"]

            missing = [f for f in required_fields if f not in reader.fieldnames]

            if missing:
                raise ValueError(
                    f"CSV inválido. Campos faltando: {missing}. "
                    f"Detectado: {reader.fieldnames}"
                )

            for row in reader:
                normalized_row = {
                    (k.strip().lower().replace("\ufeff", "") if k else k): v
                    for k, v in row.items()
                }

                products.append({
                    "name": normalized_row.get("nome"),
                    "description": normalized_row.get("descricao"),
                    "price": float(normalized_row.get("preco")),
                    "quantity": int(normalized_row.get("quantidade_inicial")),
                })

        return products
    
    def _save_products(self, products):
        """
        Persiste os produtos lidos do CSV utilizando bulk_create.
        """

        product_instances = [
            Product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                quantity=product["quantity"],
            )
            for product in products
        ]

        Product.objects.bulk_create(product_instances)