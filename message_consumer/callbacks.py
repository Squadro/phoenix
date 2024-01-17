import logging
from embedding_generator.task import process_images

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def custom_callback(message):
    logger.info(f"Processing message from Kafka:{message}")
    process_images(message)

