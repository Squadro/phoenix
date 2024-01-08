from django.db import models
from pgvector.django import VectorField


class ImageEmbedding(models.Model):
    image_id = models.BigIntegerField(primary_key=True)
    s3_key = models.CharField()
    embedding = VectorField()

    product_id = models.BigIntegerField()
    product_variant_id = models.BigIntegerField()
    product_erp_code = models.CharField()
    status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'image_embedding'
        app_label = "default"

