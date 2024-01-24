import logging

from similar_image_search.database.respository import SearchRepository

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

    # Reverse Image Search
    def getSimilarImageSearchProductId(self, image_id, product_id):
        try:
            return self.search_repository.getSearchSimilarProductByImage(
                image_id, product_id
            )
        except Exception as e:
            logger.error(f"Exception occurred {e} ")
            raise
