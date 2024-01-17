from django.db import models

from embedding_generator.model.image_embedding import ImageEmbedding
from embedding_generator.model.product_variant_information import (
    ProductVariantInformation,
)


class ProductImageRelation(models.Model):
    product = models.ForeignKey(
        ProductVariantInformation,
        on_delete=models.CASCADE,
        db_column="product_variant_id",
        related_name="image_relations",
        primary_key=True,
    )
    image = models.ForeignKey(
        ImageEmbedding,
        on_delete=models.CASCADE,
        related_name="product_relations",
        db_column="image_id",
        primary_key=True,
    )

    class Meta:
        managed = False
        db_table = "product_image_relation"
        app_label = "default"
