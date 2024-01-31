# database_handler.py
import logging

from django.db import IntegrityError

from embedding_generator.model.image_embedding import ImageEmbedding
from embedding_generator.model.product_variant_information import (
    ProductVariantInformation,
)

logger = logging.getLogger(__name__)


class EmbeddingRepository:
    def save_embedding(self, data, embedding):
        try:
            image_embedding_object, created = ImageEmbedding.objects.get_or_create(
                image_s3_key=data["s3_key"],
                image_embedding=embedding,
                image_id=data["image_id"],
            )

            (
                variant_obj,
                variant_created,
            ) = ProductVariantInformation.objects.get_or_create(
                product_variant_id=data["product_variant_id"],
                product_variant_erp_code=data.get("product_erp_code", ""),
                product_variant_status=data.get("status", 0),
                product_variant_product_id=data.get("product_id", None),
            )

            variant_obj.product_variant_images.add(image_embedding_object)

        except IntegrityError as e:
            # Handle duplicate key violation (IntegrityError) by logging a message
            logger.warning(f"Duplicate key violation: {e}")
            # You can choose to ignore or handle it differently

        except Exception as e:
            logger.error(f"Error saving embedding to the database: {e}")
            raise
