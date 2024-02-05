import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from pgvector.django import CosineDistance

from embedding_generator.model import ImageEmbedding
from embedding_generator.model.product_variant_information import (
    ProductVariantInformation,
)

logger = logging.getLogger(__name__)


class SearchRepository:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            # Your initialization logic here, if needed

    def __getSearchEmbedding(self, image_id):
        try:
            return ImageEmbedding.objects.get(image_id=image_id).image_embedding
        except ImageEmbedding.DoesNotExist:
            raise Http404(f"ImageEmbedding with ID {image_id} does not exist.")

    def getSearchSimilarProductByImage(self, image_id, product_id):
        try:
            current_embedding = self.__getSearchEmbedding(image_id)

            # Get the related ProductVariantInformation instances for each similar image
            product_ids = list(
                ProductVariantInformation.objects.annotate(
                    similarity=CosineDistance(
                        "product_variant_images__image_embedding", current_embedding
                    )
                )
                .order_by("-similarity")
                .exclude(product_variant_product_id=product_id)
                .exclude(product_variant_status__in=[1, 2])
                .values_list("product_variant_product_id", flat=True)
                .distinct()[:5]
            )
            return product_ids
        except ObjectDoesNotExist:
            logger.error(f"ImageEmbedding with ID {image_id} does not exist.")
            raise Http404(f"ImageEmbedding with ID {image_id} does not exist.")
        except Exception as e:  # Corrected syntax here
            logger.error(f"An error occurred in getSearchSimilarProduct: {e}")
            raise
