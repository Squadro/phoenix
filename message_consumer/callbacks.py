import logging

from embedding_generator.service.embedding_service import EmbeddingService

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def custom_callback(message):
    logger.info(f"Processing message from Kafka:{message}")
    service = EmbeddingService()
    return service.process_images(message)
