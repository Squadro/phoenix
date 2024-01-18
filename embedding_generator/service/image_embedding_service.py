# image_embedding_service.py

import logging

import requests

from constant import CLOUDFRONT_URL
from embedding_generator.database.repository import DatabaseHandler
from embedding_generator.processor.image_embedding_processor import EmbeddingProcessor

logger = logging.getLogger(__name__)


class ImageEmbeddingService:
    def __init__(self):
        self.image_processor = EmbeddingProcessor()
        self.database_handler = DatabaseHandler()

    def process_images(self, message):
        try:
            image_url = CLOUDFRONT_URL + message['s3_key']
            embedding = self.image_processor.create_embedding(self.download_image(image_url))
            self.database_handler.save_embedding(message, embedding)
        except Exception as e:
            logger.error(f"Error processing images: {e}")

    @staticmethod
    def download_image(image_url):
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading image: {e}")
            raise
