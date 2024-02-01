# image_embedding_service.py

import logging

import requests

from constant import CLOUDFRONT_URL
from data_processor.service.data_processing_service import DataProcessingService
from embedding_generator.database.repository import EmbeddingRepository
from embedding_generator.processor.image_embedding_processor import EmbeddingProcessor

logger = logging.getLogger(__name__)


class ImageEmbeddingService:
    def __init__(self):
        self.image_processor = EmbeddingProcessor()
        self.database_handler = EmbeddingRepository()
        self.data_processor = DataProcessingService()

    # Message: {'product_variant_id': 98606, 'product_id': 26328, 'image_id': 716028, 's3_key':
    # 'MBqDWNMn2fpgooHPxYgRgRJF', 'status': 0, 'product_erp_code': 'BD-VRM-2023-0214'}
    def process_images(self, message):
        logger.info(
            f"Processing message with ProductVariantId: {message['product_variant_id']} and "
            f"ImageId: {message['image_id']}"
        )
        try:
            message = self.data_processor.process_data(message)
            embedding = None
            if not self.database_handler.checkIfImageEmbeddingExists(
                message["image_id"]
            ):
                logger.info(f"Creating Embedding for ImageId: {message['image_id']}")
                image_url = CLOUDFRONT_URL + message["s3_key"]
                embedding = self.image_processor.create_embedding(
                    self.download_image(image_url)
                )
            self.database_handler.save_embedding(message, embedding)
            return True
        except Exception as e:
            logger.error(f"Error processing images: {e}")
            return False

    @staticmethod
    def download_image(image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image: {e}")
        except Exception as e:
            raise
