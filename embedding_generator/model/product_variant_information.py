from django.contrib.postgres.fields import JSONField
from django.db import models

from embedding_generator.model.image_embedding import ImageEmbedding


class ProductVariantInformation(models.Model):
    product_variant_id = models.BigIntegerField(primary_key=True)
    product_variant_erp_code = models.CharField(max_length=255, blank=True, null=True)
    product_variant_status = models.IntegerField(blank=True, null=True)
    product_variant_product_id = models.BigIntegerField(blank=True, null=True)
    product_variant_description = JSONField(null=True, blank=True)
    product_variant_images = models.ManyToManyField(
        ImageEmbedding, related_name="image_relation", related_query_name="images"
    )

    # class Meta:
    #     db_table = "product_variant_information"
    #     app_label = "default"
    #
    # def __str__(self):
    #     return (
    #         f"Product Variant Information - Id=  {self.product_variant_id} ,  ERP Code = {self.product_variant_erp_code},"
    #         f"Product Id = {self.product_variant_product_id}, Status = {self.product_variant_status} "
    #     )
