from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage


class ProductImportService:

    @staticmethod
    def save_uploaded_file(file) -> str:
        """
        Salva o arquivo enviado e retorna o caminho completo.
        """

        upload_path = Path("imports") / file.name

        saved_path = default_storage.save(str(upload_path), file)

        return str(settings.MEDIA_ROOT / saved_path)