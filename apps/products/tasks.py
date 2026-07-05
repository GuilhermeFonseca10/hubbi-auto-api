import logging
from celery import shared_task

from apps.products.services import ProductImportService

logger = logging.getLogger(__name__)


@shared_task
def import_products_task(file_path: str) -> None:
    """Task Celery para processar a importação de produtos via CSV."""
    logger.info("Arquivo recebido para importação: %s", file_path)

    service = ProductImportService(file_path)

    total_products = service.execute()

    logger.info(
        "%s produtos importados com sucesso.",
        total_products,
    )