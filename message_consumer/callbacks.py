import logging
from embedding_generator.service.image_processing_service import ImageProcessingService

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def custom_callback(message):
    logger.info(f"Processing message from Kafka:{message}")
    service = ImageProcessingService()
    service.process_images(message)

