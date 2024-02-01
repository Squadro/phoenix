import logging

from embedding_generator.service.image_embedding_service import ImageEmbeddingService

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def custom_callback(message):
    logger.info(f"Processing message from Kafka:{message}")
    service = ImageEmbeddingService()
    return service.process_images(message)
