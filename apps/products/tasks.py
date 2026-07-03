import logging
from celery import shared_task

from apps.products.services import ProductImportService

logger = logging.getLogger(__name__)


@shared_task
def import_products_task(file_path: str) -> None:
    logger.info("Arquivo recebido para importação: %s", file_path)

    service = ProductImportService(file_path)
    products = service.execute()

    logger.info("Produtos extraídos do CSV: %s", products)