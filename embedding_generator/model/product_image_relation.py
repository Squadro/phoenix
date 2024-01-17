from django.db import models


class ProductImageRelation(models.Model):
    product_id = models.BigIntegerField()
    image_id = models.BigIntegerField()

    class Meta:
        db_table = 'product_image_relation'
        app_label = "default"
        unique_together = (('product_id', 'image_id'),)

    def __str__(self):
        return f"Product Image Information - Product Id  = {self.product_id}, Image i d = {self.image_id}"