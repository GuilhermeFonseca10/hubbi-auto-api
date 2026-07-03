import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def import_products_task(file_path: str) -> None:
    logger.info("Arquivo recebido para importação: %s", file_path)