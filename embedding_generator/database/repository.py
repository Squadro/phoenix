# database_handler.py
import logging

from django.db import transaction

from embedding_generator.model.image_embedding import ImageEmbedding
from embedding_generator.model.product_image_relation import ProductImageRelation
from embedding_generator.model.product_variant_information import (
    ProductVariantInformation,
)

logger = logging.getLogger(__name__)


class DatabaseHandler:
    @staticmethod
    def save_embedding(data, embedding):
        try:
            with transaction.atomic():
                # Insert data into ImageEmbedding table
                embedding_obj = ImageEmbedding.objects.create(
                    image_s3_key=data["s3_key"],
                    image_embedding=embedding,
                    image_id=data["image_id"],
                )

                # Insert data into ProductVariantInformation table
                variant_obj = ProductVariantInformation.objects.create(
                    product_variant_id=data["product_variant_id"],
                    product_variant_erp_code=data.get("product_erp_code", ""),
                    product_variant_status=data.get("status", 0),
                    product_variant_product_id=data.get("product_id", None),
                )

                # Insert data into ProductImageRelation table
                ProductImageRelation.objects.create(
                    product=variant_obj, image=embedding_obj
                )

        except Exception as e:
            logger.error(f"Error saving embedding to database: {e}")
            raise
