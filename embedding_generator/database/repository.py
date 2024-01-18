# database_handler.py
import logging

from django.db import IntegrityError, transaction

from embedding_generator.model.image_embedding import ImageEmbedding
from embedding_generator.model.product_image_relation import ProductImageRelation
from embedding_generator.model.product_variant_information import (
    ProductVariantInformation,
)

logger = logging.getLogger(__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseHandler(metaclass=SingletonMeta):
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

        except IntegrityError as e:
            # Handle duplicate key violation (IntegrityError) by logging a message

            logger.warning(f"Duplicate key violation: {e}")

            pass  # You can choose to ignore or handle it differently

        except Exception as e:
            logger.error(f"Error saving embedding to database: {e}")

            raise
