import logging

from embedding_generator.service.embedding_service import EmbeddingService
from similar_image_search.database.repository import SearchRepository

logger = logging.getLogger(__name__)


class SearchService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.search_repository = SearchRepository()
            self.embedding_service = EmbeddingService()

    # Reverse Image Search
    def getSimilarImageSearchProductId(self, image_id, product_id):
        logger.info(
            f"Searching for products having images similar to image with image_id:{image_id}"
        )
        try:
            return self.search_repository.getSearchSimilarProductByImage(
                image_id, product_id
            )
        except Exception as e:
            logger.error(f"Exception occurred {e} ")
            raise e

    def getSimilarImageSearchForTextProductId(self, text):
        logger.info(
            f"Searching for products having images similar to text:{text}"
        )
        try:
            embedding = self.embedding_service.process_text(text)
            return self.search_repository.getSearchSimilarProductByText(
                embedding
            )
        except Exception as e:
            logger.error(f"Exception occurred {e} ")
            raise e

    def updateStatus(self, product_id_status_data, product_variant_id_status_data):
        logger.info(
            f"Updating status for all product variants with those product ids:{product_id_status_data}"
        )
        try:

            self.search_repository.updateStatus(product_id_status_data, product_variant_id_status_data)

        except Exception as e:
            logger.error(f"Exception occurred {e} ")
            raise e

    def discontinueStatusForErpCode(self, erp_codes):
        logger.info(
            f"Updating status for product_variant with ERP Code:{erp_codes}"
        )
        try:

            self.search_repository.updateStatusForErp(erp_codes)

        except Exception as e:
            logger.error(f"Exception occurred {e} ")
            raise e
