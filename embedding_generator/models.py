# from django.db import models
# from pgvector.django import VectorField
#
#
# # Create your models here.
#
# class ImageEmbedding1(models.Model):
#     s3_key = models.CharField(max_length=255)
#     embedding = VectorField()
#     id = models.IntegerField(primary_key=True)
#
#     class Meta:
#         managed = False
#         db_table = 'image_embeddings'
#         app_label = "default"
#
#     def __str__(self):
#         return f"ImageEmbedding - {self.s3_key}"
#
#
# class ProductVariantInformation1(models.Model):
#     id = models.BigIntegerField(primary_key=True)
#     variant_erp_code = models.CharField(max_length=255, blank=True, null=True)
#     variant_status = models.IntegerField(blank=True, null=True)
#     variant_product_id = models.BigIntegerField(blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'product_variant_information'
#         app_label = "default"
#
#     def __str__(self):
#         return (f"Product Variant Information - Id=  {self.id} ,  ERP Code = {self.variant_erp_code},"
#                 f"Product Id = {self.variant_product_id}, Status = {self.variant_status} ")
#
#
# class ProductImageRelation1(models.Model):
#     product_id = models.BigIntegerField()
#     image_id = models.BigIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'product_image_relation'
#         app_label = "default"
#         unique_together = (('product_id', 'image_id'),)
#
#     def __str__(self):
#         return f"Product Image Information - Product Id  = {self.product_id}, Image i d = {self.image_id}"
