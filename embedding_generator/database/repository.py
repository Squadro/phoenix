# database_handler.py
from django.db import transaction, IntegrityError
from embedding_generator.model.image_embedding import ImageEmbedding
from embedding_generator.model.product_variant_information import ProductVariantInformation
from embedding_generator.model.product_image_relation import ProductImageRelation
import logging

logger = logging.getLogger(__name__)


class DatabaseHandler:
    @staticmethod
    def save_embedding(data, embedding):
        try:
            with transaction.atomic():
                # Insert data into ImageEmbedding table
                embedding_obj = ImageEmbedding.objects.create(
                    s3_key=data['s3_key'],
                    embedding=embedding,
                    id=data['image_id']
                )

                # Insert data into ProductVariantInformation table
                variant_obj = ProductVariantInformation.objects.create(
                    id=data['product_variant_id'],
                    variant_erp_code=data.get('product_erp_code', ''),
                    variant_status=data.get('status', 0),
                    variant_product_id=data.get('product_id', None)
                )

                try:
                    # Insert data into ProductImageRelation table
                    relation_obj = ProductImageRelation.objects.create(
                        product_id=data['product_id'],
                        image_id=data['image_id']
                    )
                except IntegrityError as e:
                    # Log the IntegrityError
                    logger.warning(f"IntegrityError: {e}")
                    # Handle IntegrityError (e.g., print a message)
                    pass
        except Exception as e:
            logger.error(f"Error saving embedding to database: {e}")
            raise
