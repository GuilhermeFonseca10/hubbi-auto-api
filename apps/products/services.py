from pathlib import Path
import csv
import logging

from django.conf import settings
from django.core.files.storage import default_storage

logger = logging.getLogger(__name__)


class ProductImportService:

    @staticmethod
    def save_uploaded_file(file) -> str:
        upload_path = Path("imports") / file.name
        saved_path = default_storage.save(str(upload_path), file)

        return str(settings.MEDIA_ROOT / saved_path)

    def __init__(self, file_path: str):
        self.file_path = file_path

    def execute(self):
        return self._read_csv()

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